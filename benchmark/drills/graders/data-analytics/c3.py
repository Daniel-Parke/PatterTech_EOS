#!/usr/bin/env python3
"""Criterion 3: the gate is wired to the data, both ways round.

This is the criterion that separates a contract from a gate, and it is
the drill's first named failure condition: criteria 1 and 2 green while
this one is red means the agent wrote a contract and never ran it.

So the pipeline is run twice, each time on a throwaway copy. On the
shipped data it must exit non-zero, because the seeded batch is in
there. With the seeded batch dropped it must exit zero, because a
pipeline that fails on everything is not catching anything.

Where the delivered command cannot start for want of a third-party
library the criterion is left unsettled rather than failed. A pipeline
nobody managed to run has told us nothing about the work.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, copy_tree,  # noqa: E402
                     drop_seeded_batch, emit, find_pipeline,
                     looks_like_missing_dependency, run_pipeline, scratch_dir)

CID = "c3"


def main():
    scratch = scratch_dir()
    argv, description = find_pipeline(scratch)
    if argv is None:
        emit(CID, FAIL,
             "no pipeline command in the delivered tree: none of the usual "
             "entry points exist and no Makefile target was found")

    work, copy = copy_tree(scratch, "drill-data-c3-shipped-")
    try:
        shipped, output = run_pipeline(copy, argv)
        if shipped is None:
            emit(CID, FAIL, "could not run `%s`: %s"
                 % (description, output.strip()[:300]))
        if shipped != 0 and looks_like_missing_dependency(output):
            emit(CID, UNSETTLED,
                 "`%s` cannot start here: %s. The criterion was not settled; "
                 "that is a gap in this environment, not a finding against "
                 "the delivered tree."
                 % (description, " ".join(output.split())[:200]))
        if shipped == 0:
            emit(CID, FAIL,
                 "`%s` exits 0 on the shipped data, so the seeded batch of "
                 "null order totals went straight through" % description)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    work, copy = copy_tree(scratch, "drill-data-c3-dropped-")
    try:
        dropped = drop_seeded_batch(copy)
        if dropped is None:
            emit(CID, FAIL,
                 "raw/events.csv is not where the scenario put it, or has "
                 "lost event_name or order_total, so the harness cannot drop "
                 "the seeded batch")
        if dropped == 0:
            emit(CID, FAIL,
                 "raw/events.csv holds no seeded rows to drop; the export "
                 "was edited, so the red run above cannot be attributed to "
                 "the seeded batch")
        after, output = run_pipeline(copy, argv)
        if after is None:
            emit(CID, FAIL, "could not re-run `%s`: %s"
                 % (description, output.strip()[:300]))
        if after != 0:
            emit(CID, FAIL,
                 "`%s` still exits %d after the %d seeded rows were dropped, "
                 "so the red run is not the seeded batch being caught: %s"
                 % (description, after, dropped,
                    " ".join(output.split())[:250]))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    emit(CID, PASS,
         "`%s` exits %d on the shipped data and 0 once the %d seeded rows "
         "are dropped" % (description, shipped, dropped))


if __name__ == "__main__":
    main()
