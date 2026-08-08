#!/usr/bin/env python3
"""Criterion 3: lint-imports exits 0 on the delivered tree."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_lint, run_lint,  # noqa: E402
                     scratch_dir)

CID = "c3"


def main():
    scratch = scratch_dir()
    require_lint(CID)
    code, output = run_lint(scratch)
    if code is None:
        emit(CID, FAIL, "could not run lint-imports: %s" % output.strip()[:300])
    if code == 0:
        emit(CID, PASS, "lint-imports exits 0 on the delivered tree")
    emit(CID, FAIL,
         "lint-imports exits %d on the delivered tree: %s"
         % (code, " ".join(output.split())[:300]))


if __name__ == "__main__":
    main()
