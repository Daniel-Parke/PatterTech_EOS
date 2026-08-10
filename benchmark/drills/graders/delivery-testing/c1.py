#!/usr/bin/env python3
"""Criterion 1: `pytest -q` exits zero on a clean checkout of the tree.

Graded over repeated runs rather than one. The scenario ships a test
that reads the wall clock and goes red about one run in four, so a
single invocation grades a coin toss: three times out of four the
untouched fixture would be recorded as a green suite. "Exits zero" is a
property of the suite, and a suite that exits zero only sometimes does
not have it. This grader stops at the first non-zero exit, so a broken
tree is reported quickly.

The run happens on a throwaway copy, so grading never leaves caches or
byte code behind in the delivered tree.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tree, emit, require_pytest,  # noqa: E402
                     run_pytest, scratch_dir, tail)

CID = "c1"
RUNS = 20


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    work, copy = copy_tree(scratch, "drill-dt-c1-")
    try:
        for attempt in range(1, RUNS + 1):
            code, output = run_pytest(copy)
            if code is None:
                emit(CID, FAIL,
                     "could not run pytest: %s" % tail(output))
            if code == 5:
                emit(CID, FAIL,
                     "pytest collected no tests at all, so an exit code of "
                     "zero would mean nothing")
            if code != 0:
                emit(CID, FAIL,
                     "pytest -q exits %d on run %d of %d: %s"
                     % (code, attempt, RUNS, tail(output)))
        emit(CID, PASS,
             "pytest -q exits 0 on %d consecutive runs of the delivered tree"
             % RUNS)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
