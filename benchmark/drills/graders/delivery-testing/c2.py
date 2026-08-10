#!/usr/bin/env python3
"""Criterion 2: the hidden pricing oracle passes.

The oracle is never shipped in the scenario. It is written into
`.drill/oracle/` inside a throwaway copy of the delivered tree, which
is where the frozen spec says it lives, and run there. Only the oracle
file is selected, so a red test elsewhere in the agent's suite cannot
be mistaken for the pricing fault still being present, and criterion 1
keeps the rest of the suite honest.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, ORACLE_TEST_NAME, PASS, copy_tree,  # noqa: E402
                     emit, install_oracle, require_pytest, run_pytest,
                     scratch_dir, tail)

CID = "c2"


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    if not (scratch / "pricing.py").is_file():
        emit(CID, FAIL, "no pricing.py in the delivered tree")

    work, copy = copy_tree(scratch, "drill-dt-c2-")
    try:
        written, why = install_oracle(copy, ORACLE_TEST_NAME)
        if written is None:
            emit(CID, FAIL, why)
        target = ".drill/oracle/" + ORACLE_TEST_NAME
        code, output = run_pytest(copy, target)
        if code is None:
            emit(CID, FAIL,
                 "could not run the oracle suite: %s" % tail(output))
        if code == 5:
            emit(CID, FAIL,
                 "the oracle suite collected nothing, so it settled nothing")
        if code == 0:
            emit(CID, PASS,
                 "the hidden pricing oracle at %s passes against the "
                 "delivered pricing module" % target)
        emit(CID, FAIL,
             "the hidden pricing oracle fails (exit %d), so the pricing "
             "fault is still there: %s" % (code, tail(output, 320)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
