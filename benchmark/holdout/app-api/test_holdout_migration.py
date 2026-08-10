"""Holdout for T06: migration 003 adds users.marketing_opt_in.

Simulates a database that already ran 001 and 002, then applies the real
migrations directory. After the task lands 003_marketing_opt_in.sql, the
column must exist, legacy rows must read 0, and new inserts must default
to 0. Expected to fail on the shipped fixture, which has no 003.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "app-api"
sys.path.insert(0, str(FIXTURE_ROOT))

from app import db


class TestMarketingOptInMigration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmp.name)
        # Copy only the first two migrations, keeping their filenames so
        # schema_migrations records match the real directory.
        self.legacy_migrations = tmp_path / "migrations"
        self.legacy_migrations.mkdir()
        for name in ("001_init.sql", "002_indexes.sql"):
            shutil.copy(FIXTURE_ROOT / "migrations" / name, self.legacy_migrations / name)
        self.conn = db.connect(str(tmp_path / "test.db"))
        db.apply_migrations(self.conn, str(self.legacy_migrations))
        self.conn.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
            ("legacy@example.com", "0" * 64, "user"),
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def user_columns(self):
        rows = self.conn.execute("PRAGMA table_info(users)").fetchall()
        return {row["name"] for row in rows}

    def test_migration_003_adds_marketing_opt_in(self):
        db.apply_migrations(self.conn, str(FIXTURE_ROOT / "migrations"))
        self.assertIn("marketing_opt_in", self.user_columns())

    def test_legacy_row_reads_zero(self):
        db.apply_migrations(self.conn, str(FIXTURE_ROOT / "migrations"))
        row = self.conn.execute(
            "SELECT marketing_opt_in FROM users WHERE email = ?",
            ("legacy@example.com",),
        ).fetchone()
        self.assertEqual(row["marketing_opt_in"], 0)

    def test_new_insert_defaults_to_zero(self):
        db.apply_migrations(self.conn, str(FIXTURE_ROOT / "migrations"))
        self.conn.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
            ("new@example.com", "1" * 64, "user"),
        )
        self.conn.commit()
        row = self.conn.execute(
            "SELECT marketing_opt_in FROM users WHERE email = ?",
            ("new@example.com",),
        ).fetchone()
        self.assertEqual(row["marketing_opt_in"], 0)


if __name__ == "__main__":
    unittest.main()
