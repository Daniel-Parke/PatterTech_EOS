#!/usr/bin/env python3
"""Criterion 4: two runs on the same tree agree to the byte on accuracy and n.

Each run happens on its own fresh copy of the delivered tree, so the
second run cannot inherit a cache the first one warmed. Comparison is
on the serialised values rather than on floats compared numerically:
the criterion says byte-identical, and 0.7083333333333334 against
0.708333 is a difference a reader would have to reconcile.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_keys, flat_text,  # noqa: E402
                     is_accuracy_key, is_n_key, require_report, run_entry,
                     scratch_dir)

CID = "c4"


def signature(report):
    pairs = []
    for path, _, value in find_keys(report, is_accuracy_key):
        pairs.append((path, flat_text(value)))
    for path, _, value in find_keys(report, is_n_key):
        pairs.append((path, flat_text(value)))
    return sorted(pairs)


def main():
    scratch = scratch_dir()
    first = require_report(CID, scratch)

    second = run_entry(scratch, first.entry)
    if second.rc != 0 or second.report is None:
        emit(CID, FAIL,
             "%s exits 0 and reports on the first run but %s on the second, "
             "so the eval is not repeatable"
             % (first.rel,
                "exits %s" % second.rc if second.rc else "prints no report"))

    left, right = signature(first.report), signature(second.report)
    if not left:
        emit(CID, FAIL,
             "%s reports neither an accuracy nor an n, so there is nothing "
             "to compare between runs" % first.rel)
    if left != right:
        differing = [l for l, r in zip(left, right) if l != r] or [
            "the reports carry different fields"]
        emit(CID, FAIL,
             "%s gives different numbers on two runs of the same tree: %s"
             % (first.rel, differing[:3]))

    emit(CID, PASS,
         "two runs of %s on fresh copies give identical %s"
         % (first.rel, ", ".join("%s=%s" % pair for pair in left[:4])))


if __name__ == "__main__":
    main()
