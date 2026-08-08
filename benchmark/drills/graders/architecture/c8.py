#!/usr/bin/env python3
"""Criterion 8: the record names the tool and states the allowed direction.

Direction is checked as an ordered claim rather than as two package
names in the same file, because "billing may read the catalogue" and
"the catalogue may read billing" contain identical words.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402
from c6 import find_records  # noqa: E402

CID = "c8"

TOOLS = ("import-linter", "import linter", "importlinter", "lint-imports")

# billing ... <reaching verb> ... catalogue, in that order, within one
# sentence. Whitespace is collapsed before matching: prose wraps, and a
# criterion that turns on where a line break landed measures the author's
# editor rather than the argument.
DIRECTION = re.compile(
    r"billing[^.]{0,80}?\b(?:may|can|is allowed to|reads?|imports?|"
    r"depends? on|uses?)\b[^.]{0,80}?catalogue", re.I)
# The reverse claim, which is the thing the prompt forbids.
REVERSE = re.compile(
    r"catalogue[^.]{0,80}?\b(?:may|can|is allowed to|reads?|imports?|"
    r"depends? on|uses?)\b[^.]{0,80}?billing", re.I)
# Applied to the matched span alone, not the surrounding sentence: a
# correct record usually states the permission and the prohibition
# together, so "the catalogue must never import billing" sits inches
# from the claim being read and would negate it from a wider window.
NEGATED = re.compile(r"\b(?:never|not|no|must not|cannot|forbidden)\b", re.I)


def flatten(text):
    return re.sub(r"\s+", " ", text)


def main():
    scratch = scratch_dir()
    records = find_records(scratch)
    if not records:
        emit(CID, FAIL, "no decision record to inspect")

    saw_tool = saw_direction = False
    for rel in records:
        text = flatten(read(scratch / rel))
        tool = next((t for t in TOOLS if t.lower() in text.lower()), None)
        if tool:
            saw_tool = True
        direction = None
        for match in DIRECTION.finditer(text):
            if not NEGATED.search(match.group(0)):
                direction = match.group(0)[:90]
                break
        if direction:
            saw_direction = True
        if tool and direction:
            emit(CID, PASS,
                 "%s names %s and states the direction: %r"
                 % (rel, tool, direction))

    missing = []
    if not saw_tool:
        missing.append("no enforcement tool named")
    if not saw_direction:
        reversed_only = any(REVERSE.search(read(scratch / r))
                            for r in records)
        missing.append(
            "the allowed direction is stated backwards, catalogue to billing"
            if reversed_only else
            "no statement that billing may read the catalogue")
    emit(CID, FAIL, "; ".join(missing))


if __name__ == "__main__":
    main()
