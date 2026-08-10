#!/usr/bin/env python3
"""Criterion 5: a privacy notice carrying the twelve markers.

Ten checklist items and both complaint routes, to the controller and to
the Commissioner, as the fixture's own checklist defines them in
docs/compliance/notice-checklist.md. Whether the notice is any good
stays a person's job; whether it says the things it has to say does not.

The checklist itself is excluded from the candidates. It lists every
marker verbatim, so a grader that read it would pass a tree where
nothing was written.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (CHECKLIST_REL, COMPLAINT_ROUTES, FAIL,  # noqa: E402
                     NOTICE_MARKERS, PASS, TEXT_SUFFIXES, emit, flat, read,
                     rel, scratch_dir, walk)

CID = "c5"

HEADING = re.compile(r"(?:^|\n)\s*(?:#{1,6}|<h[1-6][^>]*>)\s*[^\n]*privacy",
                     re.I)
ALL_MARKERS = NOTICE_MARKERS + COMPLAINT_ROUTES


def candidates(scratch):
    """Files that read as a published notice rather than as a note."""
    for path in walk(scratch, suffixes=TEXT_SUFFIXES):
        name = rel(scratch, path)
        if name == CHECKLIST_REL:
            continue
        text = read(path)
        if "privacy" in path.name.lower() or HEADING.search(text):
            yield name, text


def missing_from(text):
    body = flat(text)
    return [m for m in ALL_MARKERS if flat(m) not in body]


def main():
    scratch = scratch_dir()
    near = []
    for name, text in candidates(scratch):
        missing = missing_from(text)
        if not missing:
            emit(CID, PASS,
                 "%s carries all %d markers, both complaint routes included"
                 % (name, len(ALL_MARKERS)))
        near.append("%s is short of %d of %d: %s"
                    % (name, len(missing), len(ALL_MARKERS),
                       ", ".join(missing[:6])))

    if near:
        emit(CID, FAIL, "; ".join(near[:3]))
    emit(CID, FAIL,
         "no privacy notice in the tree: no file is named for one and none "
         "carries a privacy heading, so the form collects addresses behind "
         "nothing")


if __name__ == "__main__":
    main()
