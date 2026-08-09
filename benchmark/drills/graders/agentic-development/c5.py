#!/usr/bin/env python3
"""Criterion 5: the single-writer rule, stated about the report.

Two halves, both required. The literal string, because the criterion
names it and the pack asks for it so the rule is checkable at all. And
a clause that puts the rule on the merged report, because the string on
its own can sit anywhere in the file and prove nothing about who writes
the thing several agents would otherwise fight over.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, clauses, emit, require_output,  # noqa: E402
                     split_front_matter)

CID = "c5"

# The criterion names two strings. A space where the pack writes a
# hyphen is the same string said out loud, so both are taken.
LITERAL = re.compile(r"single[-\s]writer|\bone writer\b", re.I)
ARTEFACT = re.compile(r"\breports?\b|roll[-\s]?up|merged file|"
                      r"weekly (?:file|write[-\s]?up)", re.I)
ONE_AGENT = re.compile(
    r"single[-\s]writer|\bone writer\b|\bsingle writer\b|"
    r"\bexactly one (?:agent|worker|process|collector|writer)\b|"
    r"\b(?:one|a single) (?:agent|worker|process|collector|writer)\b", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)

    literal = LITERAL.search(body)
    stated = None
    for clause in clauses(body):
        if ARTEFACT.search(clause) and ONE_AGENT.search(clause):
            stated = clause
            break

    problems = []
    if not literal:
        problems.append("neither `single-writer` nor `one writer` appears")
    if stated is None:
        problems.append("no clause says the merged report is written by "
                        "exactly one agent")
    if problems:
        emit(CID, FAIL, "%s: %s" % (rel, "; ".join(problems)))

    emit(CID, PASS,
         "%s uses %r and puts the rule on the report: %r"
         % (rel, literal.group(0), stated[:120]))


if __name__ == "__main__":
    main()
