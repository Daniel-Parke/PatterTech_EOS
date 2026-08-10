#!/usr/bin/env python3
"""Criterion 6: pytest exits 0 with at least three tests collected.

Run in the delivered tree with the tree itself on the path, so a
package that was never installed still imports. Nothing is passed that
would select a subset: this is the whole suite, as the drill says.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, collected_count, emit,  # noqa: E402
                     require_pytest, run_pytest, scratch_dir)

CID = "c6"
NEEDED = 3


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    code, output = run_pytest(scratch)
    if code is None:
        emit(CID, FAIL, "could not run pytest: %s" % output.strip()[:300])
    count = collected_count(output)
    tail = " ".join(output.split())[-260:]

    if code == 5:
        emit(CID, FAIL, "pytest collected no tests at all")
    if code != 0:
        emit(CID, FAIL,
             "pytest exits %d with %s test(s) collected: %s"
             % (code, "an unreadable number of" if count is None else count,
                tail))
    if count is None:
        emit(CID, FAIL,
             "pytest exits 0 but the run reports no collected count: %s"
             % tail)
    if count < NEEDED:
        emit(CID, FAIL,
             "pytest exits 0 but collected %d test(s), fewer than the %d the "
             "criterion asks for" % (count, NEEDED))
    emit(CID, PASS, "pytest exits 0 with %d tests collected" % count)


if __name__ == "__main__":
    main()
