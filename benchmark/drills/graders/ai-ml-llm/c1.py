#!/usr/bin/env python3
"""Criterion 1: the eval runs headlessly, exits 0, and is written down.

Headlessly means no arguments, no prompts, no network setup: the
grader runs `python <entry>` in a copy of the tree and nothing else.
"Recorded path" is read as the path being findable without guessing,
so the run also has to be named somewhere a reader would look, in the
docs, in an automation file, or in the report the run itself prints.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DOC_SUFFIXES, FAIL, PASS, emit, flat_text,  # noqa: E402
                     read, rel, require_run, scratch_dir, walk)

CID = "c1"


def recorded_in(scratch, run):
    """Files that name the entry point, other than the entry point itself."""
    names = {run.rel, Path(run.rel).name, Path(run.rel).stem}
    hits = []
    for path in walk(scratch, DOC_SUFFIXES):
        if rel(scratch, path) == run.rel:
            continue
        text = read(path)
        if any(name in text for name in names if name):
            hits.append(rel(scratch, path))
    if run.report is not None and any(
            name in flat_text(run.report) for name in names if name):
        hits.append("the report the run prints")
    return hits


def main():
    scratch = scratch_dir()
    run = require_run(CID, scratch)

    where = recorded_in(scratch, run)
    if not where:
        emit(CID, FAIL,
             "%s runs and exits 0, but nothing in the tree names it: no "
             "README, automation file or report records where the eval "
             "lives, so finding it means guessing" % run.rel)
    emit(CID, PASS,
         "%s exits 0 in %.1fs with no arguments, and is recorded in %s"
         % (run.rel, run.seconds, ", ".join(where[:3])))


if __name__ == "__main__":
    main()
