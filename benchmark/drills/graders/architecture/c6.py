#!/usr/bin/env python3
"""Criterion 6: a decision record exists at a recognised path."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, scratch_dir  # noqa: E402

CID = "c6"

NAME = re.compile(r"^[Aa][Dd][Rr].*-.*\.md$")


def find_records(scratch):
    found = []
    for path in scratch.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(scratch).as_posix()
        if NAME.match(path.name) or "docs/decisions/" in rel:
            found.append(rel)
    return sorted(found)


def main():
    scratch = scratch_dir()
    found = find_records(scratch)
    if found:
        emit(CID, PASS, "decision record(s): %s" % ", ".join(found[:5]))
    emit(CID, FAIL,
         "no decision record: nothing matches ADR*-*.md and nothing sits "
         "under docs/decisions/")


if __name__ == "__main__":
    main()
