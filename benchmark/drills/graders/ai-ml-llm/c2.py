#!/usr/bin/env python3
"""Criterion 2: accuracy, n and a spread. A bare accuracy fails.

The whole point of the criterion is the third field. An accuracy with
no interval and no standard error is a number that cannot be argued
with, which is the failure mode the drill is aimed at, so "accuracy is
present" is never enough here.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_keys,  # noqa: E402
                     is_accuracy_key, is_interval_key, is_n_key, numeric,
                     require_report, scratch_dir)

CID = "c2"


def main():
    scratch = scratch_dir()
    run = require_report(CID, scratch)
    report = run.report

    accuracy = [(p, v) for p, _, v in find_keys(report, is_accuracy_key)
                if numeric(v) is not None]
    counts = [(p, v) for p, _, v in find_keys(report, is_n_key)
              if numeric(v) is not None and numeric(v) >= 1]
    spread = [(p, k, v) for p, k, v in find_keys(report, is_interval_key)]

    missing = []
    if not accuracy:
        missing.append("no numeric accuracy field")
    if not counts:
        missing.append("no item count (n)")
    if not spread:
        missing.append(
            "no interval or standard error beside it, so the accuracy is "
            "reported as though the sample had no width")

    if missing:
        emit(CID, FAIL, "%s: %s" % (run.rel, "; ".join(missing)))

    emit(CID, PASS,
         "%s reports %s=%s, %s=%s and %s"
         % (run.rel, accuracy[0][0], accuracy[0][1], counts[0][0],
            counts[0][1], spread[0][0]))


if __name__ == "__main__":
    main()
