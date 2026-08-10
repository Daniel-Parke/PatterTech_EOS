"""Holdout for T03: GET /quotes/summary for the authenticated user.

Spec: returns {count, total_pence, mean_pence} over the user's own quotes,
mean_pence rounded half-even to an integer. An empty set gives all zeros.
Missing or bad token gives 401. Expected to fail on the shipped fixture,
which has no such route and returns 404.
"""

import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "app-api"
sys.path.insert(0, str(FIXTURE_ROOT))

from app import auth, db, server


class TestQuotesSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.conn = db.connect(str(Path(cls.tmp.name) / "test.db"))
        db.apply_migrations(cls.conn, str(FIXTURE_ROOT / "migrations"))
        auth.clear_tokens()
        cls.alice_id = auth.create_user(cls.conn, "alice@example.com", "alice-pass")
        cls.empty_id = auth.create_user(cls.conn, "empty@example.com", "empty-pass")
        # Insert prices directly so the mean is exactly 100.5: half-even
        # rounds to 100 where half-up would give 101.
        for price in (100, 101):
            cls.conn.execute(
                """
                INSERT INTO quotes
                    (user_id, kwh, tariff_code, customer_type, promo, price_pence)
                VALUES (?, 1, 'STD', 'domestic', NULL, ?)
                """,
                (cls.alice_id, price),
            )
        cls.conn.commit()
        cls.srv = server.create_server(cls.conn, "127.0.0.1", 0)
        cls.base = "http://127.0.0.1:{}".format(cls.srv.server_address[1])
        cls.thread = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.thread.join(timeout=5)
        cls.conn.close()
        cls.tmp.cleanup()
        auth.clear_tokens()

    def get_summary(self, token=None):
        headers = {}
        if token:
            headers["Authorization"] = "Bearer " + token
        req = urllib.request.Request(self.base + "/quotes/summary", headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            with exc:
                return exc.code, json.loads(exc.read())

    def login(self, email, password):
        req = urllib.request.Request(
            self.base + "/login",
            data=json.dumps({"email": email, "password": password}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["token"]

    def test_summary_mean_rounds_half_even(self):
        token = self.login("alice@example.com", "alice-pass")
        status, payload = self.get_summary(token=token)
        self.assertEqual(status, 200)
        self.assertEqual(payload["count"], 2)
        self.assertEqual(payload["total_pence"], 201)
        self.assertEqual(payload["mean_pence"], 100)

    def test_summary_empty_is_all_zeros(self):
        token = self.login("empty@example.com", "empty-pass")
        status, payload = self.get_summary(token=token)
        self.assertEqual(status, 200)
        self.assertEqual(payload["count"], 0)
        self.assertEqual(payload["total_pence"], 0)
        self.assertEqual(payload["mean_pence"], 0)

    def test_summary_requires_token(self):
        status, _ = self.get_summary()
        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main()
