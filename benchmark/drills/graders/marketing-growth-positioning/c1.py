#!/usr/bin/env python3
"""Criterion 1: a positioning document exists at a single recorded path.

Two questions in one sentence, and both are checked. A tree with no
document fails. So does a tree with the position spread over three
files, because "a single recorded path" is the part that makes the
document findable by the next person.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, positioning_docs, scratch_dir  # noqa: E402

CID = "c1"


def main():
    scratch = scratch_dir()
    docs = positioning_docs(scratch)
    if not docs:
        emit(CID, FAIL,
             "no positioning document: every text file in the tree is one "
             "the fixture shipped, and no new file names or states a "
             "position")
    if len(docs) > 1:
        emit(CID, FAIL,
             "the position is spread over %d files (%s), so there is no "
             "single recorded path for it"
             % (len(docs), ", ".join(where for where, _ in docs)))
    where, text = docs[0]
    emit(CID, PASS,
         "positioning document at %s, %d characters" % (where, len(text)))


if __name__ == "__main__":
    main()
