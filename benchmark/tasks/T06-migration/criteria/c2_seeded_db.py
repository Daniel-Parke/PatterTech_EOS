#!/usr/bin/env python3
"""A populated 001+002 database must gain the column with backfill and no data loss.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_seeded_db"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_seeded_db.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _load_app_module(scratch, name):
    import importlib
    sys.path.insert(0, str(scratch))
    for mod in [m for m in list(sys.modules)
                if m == "app" or m.startswith("app.")]:
        del sys.modules[mod]
    return importlib.import_module(name)


def main():
    import shutil
    import tempfile
    scratch = scratch_dir()
    migrations = scratch / "migrations"
    try:
        db = _load_app_module(scratch, "app.db")
    except Exception as exc:
        emit(False, "could not import app.db: %s" % exc)
    with tempfile.TemporaryDirectory() as tmp:
        legacy_dir = Path(tmp) / "legacy"
        legacy_dir.mkdir()
        for sql in sorted(migrations.glob("*.sql")):
            if sql.name.startswith(("001", "002")):
                shutil.copyfile(str(sql), str(legacy_dir / sql.name))
        conn = db.connect(str(Path(tmp) / "seeded.db"))
        db.apply_migrations(conn, str(legacy_dir))
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("old-a@example.com", "x"))
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("old-b@example.com", "x"))
        conn.execute(
            "INSERT INTO quotes (user_id, kwh, tariff_code, customer_type, "
            "price_pence) VALUES (1, 100, 'STD', 'domestic', 3003)")
        conn.commit()
        try:
            db.apply_migrations(conn, str(migrations))
            db.apply_migrations(conn, str(migrations))
        except Exception as exc:
            emit(False, "apply_migrations failed on the seeded db: %s" % exc)
        cols = {row["name"] for row in
                conn.execute("PRAGMA table_info(users)")}
        if "marketing_opt_in" not in cols:
            emit(False, "users.marketing_opt_in missing after migrating "
                        "the seeded db")
        rows = conn.execute(
            "SELECT email, marketing_opt_in FROM users ORDER BY email"
        ).fetchall()
        emails = [row["email"] for row in rows]
        if emails != ["old-a@example.com", "old-b@example.com"]:
            emit(False, "user rows lost or altered: %s" % emails)
        bad = [row["email"] for row in rows if row["marketing_opt_in"] != 0]
        if bad:
            emit(False, "existing rows not backfilled to 0: %s"
                 % ", ".join(bad))
        quotes = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
        conn.close()
    if quotes != 1:
        emit(False, "quote rows lost during migration: %d remain" % quotes)
    emit(True, "seeded database migrated cleanly: column added, backfill "
               "0, no data loss, re-run is a no-op")


if __name__ == "__main__":
    main()
