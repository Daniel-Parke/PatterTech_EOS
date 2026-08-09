#!/usr/bin/env python3
"""Criterion 3: no house pack reference and no house token in the source.

Two scans. The path reference is checked over every file in the tree,
because a lock-book line or a comment citing `packs/pattertech-house/`
is the tell that the house pack was consulted on a brief that never
adopted it. The vocabulary scan runs over source only.

The vocabulary is the house keyword list in `packs/pattertech-house/
PACK.md`, minus ledger, panel and plate number, which are ordinary
English a clinical tool may use innocently. The four custom properties
are the ones the house pack's own exemplar names. A shorter list that
never fires falsely is worth more here than a long one that convicts a
correct surface.

A tree with no delivered surface fails rather than passes. Absence of
house tokens in a repository with no stylesheet and no markup is not
evidence that the pluralism contract held; it is evidence that nothing
was built, and reporting it as a pass would score an empty directory.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, read, rel, scratch_dir,  # noqa: E402
                     source_files, walk)

CID = "c3"

HOUSE_PATH = "packs/pattertech-house"

HOUSE_WORDS = ["plaque", "colophon", "section[- ]mark", "kicker", "conduit",
               "bloom", "ignite", "andon", "cherenkov", "reticle"]
HOUSE_PROPS = ["--rule-bright", "--ignite-peak", "--ignite-duration",
               "--conduit-duty"]

WORD_RE = re.compile(r"\b(%s)\b" % "|".join(HOUSE_WORDS), re.I)
PROP_RE = re.compile("|".join(re.escape(p) for p in HOUSE_PROPS), re.I)


def main():
    scratch = scratch_dir()

    hits = []
    for path in walk(scratch):
        if HOUSE_PATH in read(path).replace("\\", "/"):
            hits.append(rel(scratch, path))
    if hits:
        emit(CID, FAIL,
             "%d file(s) reference %s/, a pack this brief never adopted: %s"
             % (len(hits), HOUSE_PATH, ", ".join(hits[:5])))

    sources = source_files(scratch)
    if not sources:
        emit(CID, FAIL,
             "no delivered surface to inspect: no stylesheet, markup or "
             "script in the tree, so the absence of house tokens says "
             "nothing about the work")

    for path in sources:
        text = read(path)
        prop = PROP_RE.search(text)
        if prop:
            emit(CID, FAIL,
                 "%s uses the house token %s"
                 % (rel(scratch, path), prop.group(0)))
        word = WORD_RE.search(text)
        if word:
            line = text[:word.start()].count("\n") + 1
            emit(CID, FAIL,
                 "%s line %d uses the house vocabulary word %r"
                 % (rel(scratch, path), line, word.group(0)))

    emit(CID, PASS,
         "%d source file(s) carry no house token or house vocabulary, and no "
         "file in the tree references %s/" % (len(sources), HOUSE_PATH))


if __name__ == "__main__":
    main()
