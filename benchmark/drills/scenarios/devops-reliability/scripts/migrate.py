#!/usr/bin/env python3
"""Apply the SQL migrations in migrations/ to the app database.

    python scripts/migrate.py [--to 0003] [--list]

Files are applied in ordinal order and recorded in `schema_migrations`,
so a second run is a no-op. Nothing here undoes anything: the scripts in
migrations/rollback/ are run by hand.
"""

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "migrations"
ORDINAL = re.compile(r"^(\d+)")


def db_path():
    return Path(os.environ.get("APP_DB") or ROOT / "var" / "app.db")


def migrations():
    found = []
    for path in sorted(MIGRATIONS.glob("*.sql")):
        match = ORDINAL.match(path.name)
        if match is None:
            sys.exit("migration filename has no ordinal: %s" % path.name)
        found.append((int(match.group(1)), path))
    return sorted(found)


def applied(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations ("
                 "  name TEXT PRIMARY KEY,"
                 "  applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
                 ")")
    return {row[0] for row in conn.execute(
        "SELECT name FROM schema_migrations")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", help="stop after this ordinal")
    parser.add_argument("--list", action="store_true",
                        help="print what would run and stop")
    args = parser.parse_args(argv)

    stop = int(args.to) if args.to else None
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    try:
        done = applied(conn)
        ran = 0
        for ordinal, migration in migrations():
            if stop is not None and ordinal > stop:
                break
            if migration.name in done:
                continue
            if args.list:
                print("would apply %s" % migration.name)
                continue
            sql = migration.read_text(encoding="utf-8")
            with conn:
                conn.executescript(sql)
                conn.execute("INSERT INTO schema_migrations (name) "
                             "VALUES (?)", (migration.name,))
            print("applied %s" % migration.name)
            ran += 1
        if not ran and not args.list:
            print("nothing to apply")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
