#!/usr/bin/env python3
"""Criterion 6: the compatibility window is real.

The expand step is the last migration before the first destructive one.
A database is taken up to exactly that point, seeded, and the test
suite the repository already had is run against it, restored from the
fixture first so that "unchanged" is a fact rather than a promise.

If the suite only passes because it was edited, this fails, and that is
the intent: the window exists so that the old code keeps working while
the new schema is already in place.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, apply_migrations,  # noqa: E402
                     baseline_migration_names, copy_tree, emit,
                     is_destructive, migration_files, require_baseline, run,
                     scratch_dir)

CID = "c6"


def main():
    scratch = scratch_dir()
    baseline = require_baseline(CID)

    shipped = baseline_migration_names(CID)
    files = migration_files(scratch)
    if not files:
        emit(CID, FAIL, "no migrations to apply")

    destructive = [i for i, p in enumerate(files) if is_destructive(p)]
    if not destructive:
        emit(CID, FAIL,
             "no migration drops anything, so there is no contract step and "
             "no compatibility window to prove; the column is still there")

    cut = destructive[0]
    expand = files[:cut]
    new_in_expand = [p.name for p in expand if p.name not in shipped]
    if not new_in_expand:
        emit(CID, FAIL,
             "%s is the first destructive migration and nothing new comes "
             "before it, so the drop lands in the same deploy as the change"
             % files[cut].name)

    work, copy = copy_tree(scratch, "drill-devops-c6-")
    try:
        # The suite is the one the repository shipped with, whatever the
        # delivered tree now has in tests/.
        delivered_tests = copy / "tests"
        if delivered_tests.exists():
            shutil.rmtree(delivered_tests)
        shutil.copytree(baseline / "tests", delivered_tests)

        db_file = work / "expand.db"
        prefix = [copy / p.relative_to(scratch) for p in expand]
        ok, why = apply_migrations(db_file, prefix)
        if not ok:
            emit(CID, FAIL,
                 "the migrations up to and including %s do not apply: %s"
                 % (expand[-1].name, why))

        code, output = run([sys.executable,
                            str(baseline / "scripts" / "seed.py")], copy,
                           env={"APP_DB": str(db_file)})
        if code != 0:
            emit(CID, FAIL,
                 "the standing rows will not seed after %s, so the expand "
                 "step is not backwards compatible: %s"
                 % (expand[-1].name, " ".join(output.split())[:200]))

        code, output = run([sys.executable, "-m", "unittest", "discover",
                            "-s", "tests", "-t", "."], copy,
                           env={"APP_DB": str(db_file)})
        tail = " ".join(output.split())[-260:]
        if code != 0:
            emit(CID, FAIL,
                 "the pre-existing test suite fails against the schema at "
                 "%s, so the old code does not survive the expand step: %s"
                 % (expand[-1].name, tail))

        emit(CID, PASS,
             "migrations up to %s applied (%s is the first destructive one), "
             "and the unchanged test suite passes against it: %s"
             % (expand[-1].name, files[cut].name, tail[-120:]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
