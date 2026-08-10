"""Holdout for T07: /admin/reports must check the role, not just the token.

Expected to fail on the shipped fixture, which returns 200 to any valid
token regardless of role.
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


class TestAdminRoleCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.conn = db.connect(str(Path(cls.tmp.name) / "test.db"))
        db.apply_migrations(cls.conn, str(FIXTURE_ROOT / "migrations"))
        auth.clear_tokens()
        auth.create_user(cls.conn, "admin@example.com", "admin-pass", role="admin")
        auth.create_user(cls.conn, "alice@example.com", "alice-pass")
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

    def get_reports(self, token=None):
        headers = {}
        if token:
            headers["Authorization"] = "Bearer " + token
        req = urllib.request.Request(self.base + "/admin/reports", headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            with exc:
                return exc.code

    def login(self, email, password):
        req = urllib.request.Request(
            self.base + "/login",
            data=json.dumps({"email": email, "password": password}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["token"]

    def test_non_admin_token_gets_403(self):
        token = self.login("alice@example.com", "alice-pass")
        self.assertEqual(self.get_reports(token=token), 403)

    def test_admin_token_still_200(self):
        token = self.login("admin@example.com", "admin-pass")
        self.assertEqual(self.get_reports(token=token), 200)

    def test_no_token_still_401(self):
        self.assertEqual(self.get_reports(), 401)


if __name__ == "__main__":
    unittest.main()
