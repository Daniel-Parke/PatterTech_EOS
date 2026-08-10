#!/usr/bin/env python3
"""Criterion 1: the decision record names the network copyleft term.

Two facts have to be in one file: the exact identifier, and the reason
it bites here. A venture that hosts and distributes nothing is only
caught by the network clause, so a record that names the component
without naming remote interaction has not made the decision the drill
is about; it has copied an identifier across.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (COPYLEFT_ID, FAIL, PASS, decision_records,  # noqa: E402
                     emit, flat, scratch_dir)

CID = "c1"

TRIGGERS = ("network", "section 13", "remote")


def main():
    scratch = scratch_dir()
    records = decision_records(scratch)
    if not records:
        emit(CID, FAIL,
             "no decision record in the tree: nothing is named "
             "LICENCE_DECISION.md, or anything else carrying the words "
             "licence and decision")

    near = []
    for name, text in records:
        body = flat(text)
        has_id = COPYLEFT_ID.lower() in body
        hit = next((t for t in TRIGGERS if t in body), None)
        if has_id and hit:
            emit(CID, PASS,
                 "%s names %s and says why it fires here (%r)"
                 % (name, COPYLEFT_ID, hit))
        if has_id:
            near.append("%s names %s but none of %s, so it does not say why "
                        "a term that triggers on distribution matters to a "
                        "venture that distributes nothing"
                        % (name, COPYLEFT_ID, ", ".join(TRIGGERS)))
        elif hit:
            near.append("%s mentions %r but never names %s"
                        % (name, hit, COPYLEFT_ID))
        else:
            near.append("%s names neither %s nor any of %s"
                        % (name, COPYLEFT_ID, ", ".join(TRIGGERS)))

    emit(CID, FAIL, "; ".join(near[:3]))


if __name__ == "__main__":
    main()
