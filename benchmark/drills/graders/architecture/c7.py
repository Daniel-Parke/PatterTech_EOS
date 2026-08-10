#!/usr/bin/env python3
"""Criterion 7: the record carries MADR headings and two or more options.

The drill's second named failure condition is a record with a single
option: the template arrived and the argument did not. So the option
count is what decides this, not the presence of the heading.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from c6 import find_records  # noqa: E402

CID = "c7"

CONSIDERED = re.compile(r"^#{1,6}\s*Considered\s+Options\s*$", re.I | re.M)
OUTCOME = re.compile(r"^#{1,6}\s*Decision\s+Outcome\s*$", re.I | re.M)
HEADING = re.compile(r"^#{1,6}\s", re.M)
ITEM = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)\S", re.M)


def options_under(text, match):
    """List items between the Considered Options heading and the next one."""
    start = match.end()
    following = HEADING.search(text, start)
    section = text[start:following.start() if following else len(text)]
    return ITEM.findall(section)


def main():
    scratch = scratch_dir()
    records = find_records(scratch)
    if not records:
        emit(CID, FAIL, "no decision record to inspect; criterion 6 covers "
                        "that, and this one cannot run without it")

    best = None
    for rel in records:
        text = read(scratch / rel)
        considered = CONSIDERED.search(text)
        outcome = OUTCOME.search(text)
        if not considered or not outcome:
            missing = []
            if not considered:
                missing.append("Considered Options")
            if not outcome:
                missing.append("Decision Outcome")
            best = best or (rel, "missing heading(s): %s" % ", ".join(missing))
            continue
        options = options_under(text, considered)
        if len(options) >= 2:
            emit(CID, PASS,
                 "%s carries both headings and lists %d options"
                 % (rel, len(options)))
        best = (rel, "both headings present but Considered Options lists %d "
                     "option(s); a record with one option is the template "
                     "without the argument" % len(options))

    rel, why = best
    emit(CID, FAIL, "%s: %s" % (rel, why))


if __name__ == "__main__":
    main()
