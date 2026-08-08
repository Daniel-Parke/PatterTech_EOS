#!/usr/bin/env python3
"""Criterion 2: a forbidden contract stops the catalogue reaching billing.

The direction is the whole point. A contract naming the two packages
the other way round permits exactly what the prompt forbade, so source
and target are checked separately rather than as a pair of names that
happen to appear.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, as_list, contracts, emit,  # noqa: E402
                     find_config, scratch_dir, top_package)

CID = "c2"


def main():
    scratch = scratch_dir()
    path, sections = find_config(scratch)
    if path is None:
        emit(CID, FAIL, "no parseable boundary contract file; criterion 1 "
                        "covers that, and this one cannot run without it")

    reversed_found = False
    for opts in contracts(sections):
        if str(opts.get("type", "")).strip() != "forbidden":
            continue
        sources = {top_package(m) for m in as_list(opts.get("source_modules"))}
        targets = {top_package(m)
                   for m in as_list(opts.get("forbidden_modules"))}
        if "catalogue" in sources and "billing" in targets:
            emit(CID, PASS,
                 "forbidden contract %r stops catalogue reaching billing"
                 % (opts.get("name") or "unnamed"))
        if "billing" in sources and "catalogue" in targets:
            reversed_found = True

    if reversed_found:
        emit(CID, FAIL,
             "a forbidden contract names both packages but in the wrong "
             "direction: it stops billing reaching the catalogue, which the "
             "prompt explicitly allows, and leaves the catalogue free to "
             "import billing")
    emit(CID, FAIL,
         "no forbidden contract with catalogue as source and billing as "
         "forbidden target; found %d contract(s)" % len(contracts(sections)))


if __name__ == "__main__":
    main()
