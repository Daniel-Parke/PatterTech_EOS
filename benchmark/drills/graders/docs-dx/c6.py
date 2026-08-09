#!/usr/bin/env python3
"""Criterion 6: the change is written down under Unreleased.

Scoped to the section, not to the file. The fixture's `0.3.0` entry
already mentions `--out-dir`, because that is where the rename was
recorded when it happened, so a grader that searched the whole
changelog would pass a tree where nothing new was written at all.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402

CID = "c6"

HEADING = re.compile(r"^##\s+\[?Unreleased", re.I)
NEXT = re.compile(r"^##\s+")
NEEDLE = "--out-dir"


def main():
    scratch = scratch_dir()
    path = scratch / "CHANGELOG.md"
    if not path.is_file():
        emit(CID, FAIL, "no CHANGELOG.md in the tree")

    lines = read(path).splitlines()
    start = None
    for i, line in enumerate(lines):
        if HEADING.match(line):
            start = i + 1
            break
    if start is None:
        emit(CID, FAIL,
             "CHANGELOG.md has no heading matching '## [Unreleased'; the "
             "section the fixture shipped with is gone")

    section = []
    for line in lines[start:]:
        if NEXT.match(line):
            break
        section.append(line)

    for line in section:
        if NEEDLE in line:
            emit(CID, PASS,
                 "the Unreleased section records it: %r" % line.strip()[:120])

    body = [l.strip() for l in section if l.strip()]
    emit(CID, FAIL,
         "the Unreleased section has %d line(s) and none mentions %s: %s"
         % (len(body), NEEDLE,
            "; ".join(body[:3]) if body else "the section is empty"))


if __name__ == "__main__":
    main()
