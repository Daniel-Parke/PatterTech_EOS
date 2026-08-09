#!/usr/bin/env python3
"""Criterion 1: three or more migrations, expand and contract apart.

Two things, both decidable from the files. There have to be at least
three forward migrations, and no single file may add to a subject and
drop the same subject.

Two tables count as one subject when the file itself ties them
together: a rename, or a backfill that reads one and writes the other.
Otherwise the rename dance, and "create contacts, copy the addresses
across, drop the old column", would both walk past a check that only
compares table names, and both of them are expand and contract in one
deploy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, migration_files,  # noqa: E402
                     non_sql_migrations, read, same_subject, scratch_dir,
                     sql_subjects)

CID = "c1"


def main():
    scratch = scratch_dir()
    files = migration_files(scratch)
    others = non_sql_migrations(scratch)

    if len(files) < 3:
        extra = ("; %s look like migrations but are not .sql, which this "
                 "project's runner does not apply" % ", ".join(others)
                 if others else "")
        emit(CID, FAIL,
             "%d forward migration file(s) under migrations/: %s. The change "
             "needs at least three, so that expand, backfill and contract "
             "are separate deploys%s"
             % (len(files), ", ".join(p.name for p in files) or "none", extra))

    offenders = []
    for path in files:
        additive, destructive, links = sql_subjects(read(path))
        shared = same_subject(additive, destructive, links)
        if shared:
            offenders.append(
                "%s both adds to and drops %s (%s and %s in one file)"
                % (path.name, " and ".join(shared),
                   ", ".join(sorted(set(additive.values()))),
                   ", ".join(sorted(set(destructive.values())))))

    if offenders:
        emit(CID, FAIL, "; ".join(offenders))

    destructive_files = [p.name for p in files if sql_subjects(read(p))[1]]
    emit(CID, PASS,
         "%d forward migrations, and no file mixes an additive statement "
         "with a drop on the same subject (drops live in %s)"
         % (len(files), ", ".join(destructive_files) or "no file"))


if __name__ == "__main__":
    main()
