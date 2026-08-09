#!/usr/bin/env python3
"""Criterion 8: comms and fix are separate fields, even when one person.

`comms_owner` and `fix_owner` must both be present and non-empty on the
incident record. Equal values pass: a two-person team on a Wednesday
morning has the same name in both, and the criterion is about the two
jobs being named separately, not about two people doing them. A single
`owner` field collapsing the pair is the failure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, get, has_key, is_empty,  # noqa: E402
                     load_incident, scratch_dir, text_of)

CID = "c8"


def main():
    scratch = scratch_dir()
    doc, err = load_incident(scratch)
    if err:
        emit(CID, FAIL, err)

    problems = []
    for field in ("comms_owner", "fix_owner"):
        if not has_key(doc, field):
            problems.append("no %s field" % field)
        elif is_empty(get(doc, field)):
            problems.append("%s is empty" % field)
    if problems:
        collapsed = [k for k in doc if k.lower() in ("owner", "incident_owner",
                                                     "lead", "owners")]
        if collapsed:
            problems.append("the record carries %s instead"
                            % ", ".join(collapsed))
        emit(CID, FAIL, "incident-0001.json: %s" % "; ".join(problems))

    comms = text_of(get(doc, "comms_owner")).strip()
    fix = text_of(get(doc, "fix_owner")).strip()
    same = " (the same person holds both, which the criterion allows)" \
        if comms.lower() == fix.lower() else ""
    emit(CID, PASS,
         "comms_owner is %r and fix_owner is %r, two separate non-empty "
         "fields%s" % (comms[:40], fix[:40], same))


if __name__ == "__main__":
    main()
