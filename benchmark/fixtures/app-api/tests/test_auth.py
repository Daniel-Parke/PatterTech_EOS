"""Unit tests for accounts and tokens against a temp database."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import auth, db

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = db.connect(str(Path(self.tmp.name) / "test.db"))
        db.apply_migrations(self.conn, str(FIXTURE_ROOT / "migrations"))
        auth.clear_tokens()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()
        auth.clear_tokens()

    def test_hash_password_is_sha256_hex(self):
        digest = auth.hash_password("alice-pass")
        self.assertEqual(len(digest), 64)
        self.assertEqual(
            digest,
            "9b90e524e94995ee4aeae2ee3c428a53405d1e8db147f44facc46797d0caf4c3",
        )

    def test_create_user_returns_id_and_persists(self):
        user_id = auth.create_user(self.conn, "alice@example.com", "alice-pass")
        row = self.conn.execute(
            "SELECT email, role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        self.assertEqual(row["email"], "alice@example.com")
        self.assertEqual(row["role"], "user")

    def test_issue_token_good_credentials(self):
        user_id = auth.create_user(self.conn, "alice@example.com", "alice-pass")
        token = auth.issue_token(self.conn, "alice@example.com", "alice-pass")
        self.assertIsNotNone(token)
        claims = auth.check_token(token)
        self.assertEqual(claims["user_id"], user_id)
        self.assertEqual(claims["email"], "alice@example.com")
        self.assertEqual(claims["role"], "user")

    def test_issue_token_bad_password(self):
        auth.create_user(self.conn, "alice@example.com", "alice-pass")
        self.assertIsNone(auth.issue_token(self.conn, "alice@example.com", "wrong"))

    def test_issue_token_unknown_email(self):
        self.assertIsNone(auth.issue_token(self.conn, "nobody@example.com", "x"))

    def test_check_token_unknown(self):
        self.assertIsNone(auth.check_token("not-a-real-token"))
        self.assertIsNone(auth.check_token(None))

    def test_revoke_token(self):
        auth.create_user(self.conn, "alice@example.com", "alice-pass")
        token = auth.issue_token(self.conn, "alice@example.com", "alice-pass")
        auth.revoke_token(token)
        self.assertIsNone(auth.check_token(token))

    def test_admin_role_round_trips(self):
        auth.create_user(self.conn, "admin@example.com", "admin-pass", role="admin")
        token = auth.issue_token(self.conn, "admin@example.com", "admin-pass")
        self.assertEqual(auth.check_token(token)["role"], "admin")


if __name__ == "__main__":
    unittest.main()
