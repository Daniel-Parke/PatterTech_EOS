#!/usr/bin/env python3
"""Criterion 9: human approval gates the pull request.

The clause has to name the approval, name the act, and put one before
the other. Approval mentioned in the same section as a pull request is
not a gate; "a human approves the report before the pull request is
opened" is.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, clauses, emit, require_output,  # noqa: E402
                     section, split_front_matter)

CID = "c9"

APPROVAL = re.compile(r"approv|sign[-\s]?off|signed off", re.I)
ACT = re.compile(r"pull request|\bPR\b|\bMR\b|merge request", re.I)
GATE = re.compile(
    r"\bbefore\b|\bprior to\b|\bahead of\b|\buntil\b|\bgates?\b|\bgated\b|"
    r"\bblocks?\b|\bblocked\b|\bnever\b|\bnot\b|\bno\b|\bonly (?:after|once|"
    r"when)\b|\brequire", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Approval")
    if text is None:
        emit(CID, FAIL, "%s has no level-two `## Approval` section" % rel)

    near = []
    for clause in clauses(text):
        has_approval = APPROVAL.search(clause)
        has_act = ACT.search(clause)
        has_gate = GATE.search(clause)
        if has_approval and has_act and has_gate:
            emit(CID, PASS,
                 "%s gates the pull request on human approval: %r"
                 % (rel, clause[:140]))
        if has_approval and has_act:
            near.append(clause)

    if near:
        emit(CID, FAIL,
             "%s `## Approval` mentions approval and the pull request in the "
             "same clause but never orders one before the other: %r"
             % (rel, near[0][:140]))
    emit(CID, FAIL,
         "%s `## Approval` has no clause naming both a human approval and the "
         "pull request it gates" % rel)


if __name__ == "__main__":
    main()
