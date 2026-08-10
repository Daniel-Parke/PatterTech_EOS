#!/usr/bin/env python3
"""A fresh database migrated 001 to 003 must carry the column.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_fresh_db"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_fresh_db.py <scratch-dir>")
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
    import tempfile
    scratch = scratch_dir()
    migrations = scratch / "migrations"
    if len(sorted(migrations.glob("*.sql"))) < 3:
        emit(False, "no third migration file under migrations/")
    try:
        db = _load_app_module(scratch, "app.db")
    except Exception as exc:
        emit(False, "could not import app.db: %s" % exc)
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(str(Path(tmp) / "fresh.db"))
        try:
            db.apply_migrations(conn, str(migrations))
        except Exception as exc:
            emit(False, "apply_migrations failed on a fresh db: %s" % exc)
        cols = {row["name"] for row in
                conn.execute("PRAGMA table_info(users)")}
        if "marketing_opt_in" not in cols:
            emit(False, "users.marketing_opt_in missing after a fresh "
                        "migration run")
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("fresh@example.com", "x"))
        conn.commit()
        value = conn.execute(
            "SELECT marketing_opt_in FROM users WHERE email = ?",
            ("fresh@example.com",)).fetchone()[0]
        conn.close()
    if value != 0:
        emit(False, "new row defaulted marketing_opt_in to %r, want 0"
             % value)
    emit(True, "fresh database has users.marketing_opt_in defaulting to 0")


if __name__ == "__main__":
    main()
