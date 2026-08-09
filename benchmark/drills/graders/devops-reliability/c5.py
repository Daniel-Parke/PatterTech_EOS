#!/usr/bin/env python3
"""Criterion 5: the data survives the move, value for value.

The order matters, so it is spelled out:

1. A fresh database gets the migrations the fixture shipped with.
2. The fixture's own seed script puts the standing rows in.
3. The delivered migrations are applied on top, to that populated
   database.
4. The email addresses are read back out of `contacts`.

Seeding before the new migrations run is the whole point. A migration
set that creates `contacts` and leaves the backfill to a script, or to
the application, moves no existing row and fails here, which is what
the criterion asks.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, apply_migrations, emit,  # noqa: E402
                     baseline_migration_names, columns_of, migration_files,
                     non_sql_migrations, query, require_baseline, run,
                     scratch_dir, table_names)

CID = "c5"


def email_column(db_file, table, wanted):
    """The column in `table` that holds the addresses, if any."""
    columns = columns_of(db_file, table)
    named = [name for name, _ in columns
             if "email" in name.lower() or "address" in name.lower()]
    for name in named + [name for name, _ in columns]:
        try:
            rows = query(db_file, 'SELECT "%s" FROM "%s"' % (name, table))
        except Exception:
            continue
        values = {row[0] for row in rows}
        if values == wanted:
            return name, len(rows), values
    if named:
        rows = query(db_file, 'SELECT "%s" FROM "%s"' % (named[0], table))
        return named[0], len(rows), {row[0] for row in rows}
    return None, 0, set()


def main():
    scratch = scratch_dir()
    baseline = require_baseline(CID)

    shipped = baseline_migration_names(CID)
    delivered = migration_files(scratch)
    added = [p for p in delivered if p.name not in shipped]
    if not added:
        others = non_sql_migrations(scratch)
        emit(CID, FAIL,
             "no migration beyond the %d the fixture shipped, so nothing "
             "moves the email addresses anywhere%s"
             % (len(shipped),
                "; %s are not .sql" % ", ".join(others) if others else ""))

    work = Path(tempfile.mkdtemp(prefix="drill-devops-c5-"))
    try:
        db_file = work / "app.db"

        ok, why = apply_migrations(db_file, migration_files(baseline))
        if not ok:
            emit(CID, FAIL, "the fixture's own migrations did not apply: %s"
                            % why)

        code, output = run([sys.executable,
                            str(baseline / "scripts" / "seed.py")], work,
                           env={"APP_DB": str(db_file)})
        if code != 0:
            emit(CID, FAIL, "could not seed the database: %s"
                            % " ".join(output.split())[:200])

        before = {row[0] for row in
                  query(db_file, "SELECT email_address FROM users")}
        if not before:
            emit(CID, FAIL, "the seeded database holds no email addresses")

        ok, why = apply_migrations(db_file, added)
        if not ok:
            emit(CID, FAIL,
                 "the delivered migrations do not apply to a populated "
                 "database: %s" % why)

        tables = table_names(db_file)
        if "contacts" not in tables:
            emit(CID, FAIL,
                 "no `contacts` table after every migration ran; tables are "
                 "%s" % ", ".join(sorted(t for t in tables
                                         if not t.startswith("sqlite_"))))

        column, count, values = email_column(db_file, "contacts", before)
        if column is None:
            emit(CID, FAIL,
                 "`contacts` exists but no column in it holds the seeded "
                 "addresses; columns are %s"
                 % ", ".join(n for n, _ in columns_of(db_file, "contacts")))
        if count != len(before):
            emit(CID, FAIL,
                 "%d row(s) in contacts against %d seeded users: the "
                 "backfill did not move every row"
                 % (count, len(before)))
        if values != before:
            missing = sorted(before - values)[:3]
            extra = sorted(values - before)[:3]
            emit(CID, FAIL,
                 "the addresses in contacts.%s are not the seeded set "
                 "(missing %s; unexpected %s)"
                 % (column, ", ".join(missing) or "none",
                    ", ".join(extra) or "none"))

        emit(CID, PASS,
             "%d migrations applied in order to a seeded database, and all "
             "%d addresses read back identically through contacts.%s"
             % (len(delivered), count, column))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
