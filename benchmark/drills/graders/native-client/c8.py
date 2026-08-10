#!/usr/bin/env python3
"""Criterion 8: three cited ids in the decisions file, and every one of
them resolves.

The ledger is the estate's evidence register plus the fragment files the
packs hold, both read out of the repository this grader ships inside
rather than out of the tree being graded. A venture cannot make an id
resolve by writing it down twice.

Three is the floor and resolution is the test, so a file citing four ids
of which one is invented fails. The count is easy to reach; the truth of
the citations is not, and that is what this criterion is for.

Where the ledger cannot be found the criterion is unsettled rather than
failed. Nothing was looked at, and reporting that as a fail invents a
finding about work nobody read.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISIONS, EV, FAIL, FRAG, LEDGER, PASS,  # noqa: E402
                     UNSETTLED, emit, find_named, read, rel,
                     resolvable_ids, scratch_dir)

CID = "c8"

MINIMUM = 3


def main():
    scratch = scratch_dir()

    found = find_named(scratch, DECISIONS)
    if not found:
        emit(CID, FAIL, "no %s in the delivered tree" % DECISIONS)
    path = found[0]
    where = rel(scratch, path)

    text = read(path)
    cited = sorted(set(EV.findall(text)) | set(FRAG.findall(text)))
    if len(cited) < MINIMUM:
        emit(CID, FAIL,
             "%s cites %d id(s) (%s); the floor is %d"
             % (where, len(cited), ", ".join(cited) or "none", MINIMUM))

    resolvable, sources = resolvable_ids()
    if not resolvable:
        emit(CID, UNSETTLED,
             "no evidence ledger at %s and no pack fragment files, so the "
             "%d id(s) cited in %s were not resolved against anything"
             % (LEDGER, len(cited), where))

    unresolved = [i for i in cited if i not in resolvable]
    if unresolved:
        emit(CID, FAIL,
             "%s cites %s, which resolve nowhere in %s or the %d pack "
             "fragment file(s); a citation that resolves nowhere is a "
             "number of citations, not evidence"
             % (where, ", ".join(unresolved[:6]), LEDGER,
                max(len(sources) - 1, 0)))

    emit(CID, PASS,
         "%s cites %d id(s) and every one resolves: %s"
         % (where, len(cited), ", ".join(cited[:8])))


if __name__ == "__main__":
    main()
