"""End to end tests: boot the real server on an ephemeral port."""

import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import auth, billing, db, server

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


class TestQuoteAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.conn = db.connect(str(Path(cls.tmp.name) / "test.db"))
        db.apply_migrations(cls.conn, str(FIXTURE_ROOT / "migrations"))
        auth.clear_tokens()
        cls.admin_id = auth.create_user(
            cls.conn, "admin@example.com", "admin-pass", role="admin"
        )
        cls.alice_id = auth.create_user(cls.conn, "alice@example.com", "alice-pass")
        cls.bob_id = auth.create_user(cls.conn, "bob@example.com", "bob-pass")
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

    def request(self, method, path, body=None, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            self.base + path, data=data, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            with exc:
                return exc.code, json.loads(exc.read())

    def login(self, email, password):
        status, payload = self.request(
            "POST", "/login", {"email": email, "password": password}
        )
        self.assertEqual(status, 200)
        return payload["token"]

    def test_login_ok(self):
        status, payload = self.request(
            "POST", "/login", {"email": "alice@example.com", "password": "alice-pass"}
        )
        self.assertEqual(status, 200)
        self.assertIn("token", payload)

    def test_login_bad_credentials(self):
        status, _ = self.request(
            "POST", "/login", {"email": "alice@example.com", "password": "wrong"}
        )
        self.assertEqual(status, 401)

    def test_login_bad_body(self):
        status, _ = self.request("POST", "/login", {"email": "alice@example.com"})
        self.assertEqual(status, 400)

    def test_quotes_requires_token(self):
        status, _ = self.request("GET", "/quotes")
        self.assertEqual(status, 401)

    def test_create_and_list_own_quotes(self):
        token = self.login("alice@example.com", "alice-pass")
        body = {"kwh": 100, "tariff_code": "STD", "customer_type": "domestic"}
        status, payload = self.request("POST", "/quotes", body, token=token)
        self.assertEqual(status, 201)
        quote = payload["quote"]
        self.assertEqual(
            quote["price_pence"], billing.price_pence(100, "STD", "domestic", None)
        )
        status, payload = self.request("GET", "/quotes", token=token)
        self.assertEqual(status, 200)
        listed = payload["quotes"]
        self.assertTrue(all(q["user_id"] == self.alice_id for q in listed))
        self.assertIn(quote["id"], [q["id"] for q in listed])

    def test_create_quote_rejects_bad_tariff(self):
        token = self.login("alice@example.com", "alice-pass")
        body = {"kwh": 100, "tariff_code": "MEGA", "customer_type": "domestic"}
        status, _ = self.request("POST", "/quotes", body, token=token)
        self.assertEqual(status, 400)

    def test_admin_reports_ok_for_admin(self):
        token = self.login("admin@example.com", "admin-pass")
        status, payload = self.request("GET", "/admin/reports", token=token)
        self.assertEqual(status, 200)
        report = payload["report"]
        self.assertIn("count", report)
        self.assertIn("total_pence", report)
        self.assertIn("by_tariff", report)

    def test_admin_reports_requires_token(self):
        status, _ = self.request("GET", "/admin/reports")
        self.assertEqual(status, 401)

    def test_unknown_path_404(self):
        status, _ = self.request("GET", "/nope")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
