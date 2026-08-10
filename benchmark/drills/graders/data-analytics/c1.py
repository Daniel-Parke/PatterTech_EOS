#!/usr/bin/env python3
"""Criterion 1: a contract or expectation file exists and parses.

The drill names three shapes: an ODCS `*.odcs.yaml`, a dbt `schema.yml`
carrying `contract: enforced`, or a Great Expectations suite JSON. A
file that only looks like one is not enough; it has to load, because the
criterion is what stands between a contract and a paragraph about one.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, contract_files, emit, scratch_dir  # noqa: E402

CID = "c1"


def main():
    scratch = scratch_dir()
    found, near = contract_files(scratch)
    if found:
        relative, kind, _ = found[0]
        emit(CID, PASS,
             "%s is a %s and parses%s"
             % (relative, kind,
                ("; %d contract file(s) in all" % len(found))
                if len(found) > 1 else ""))
    if near:
        emit(CID, FAIL,
             "no contract or expectation file loads: %s"
             % "; ".join("%s (%s)" % (r, why) for r, why in near[:4]))
    emit(CID, FAIL,
         "no contract or expectation file in the delivered tree: nothing "
         "matches *.odcs.yaml, a dbt schema.yml with contract: enforced, or "
         "a Great Expectations suite JSON")


if __name__ == "__main__":
    main()
