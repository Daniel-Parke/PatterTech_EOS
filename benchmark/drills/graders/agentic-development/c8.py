#!/usr/bin/env python3
"""Criterion 8: the validator on the extraction, and nothing on the prose.

Three things, all in the Verification section unless stated otherwise:

- the schema validator is placed on the extraction output;
- the report prose is said to have no external oracle;
- no evaluator-optimizer loop is claimed for that prose.

The third is checked across the whole file rather than the section,
because a loop claimed anywhere is still claimed. It is read as a
prohibition: where the string appears it has to appear inside a clause
that rules it out. Where it never appears, nothing was claimed and the
criterion is satisfied on that point, which the reason says plainly
rather than reporting a check that did not happen as a pass.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, clauses, emit, require_output,  # noqa: E402
                     section, split_front_matter)

CID = "c8"

SCHEMA = re.compile(r"schema|validator", re.I)
EXTRACTION = re.compile(r"extract", re.I)
ORACLE = re.compile(r"\boracle", re.I)
PROSE = re.compile(r"\bprose\b|\breports?\b|narrative|write[-\s]?up|"
                   r"roll[-\s]?up", re.I)
NO_ORACLE = re.compile(
    r"\bno\b|\bnot\b|\bnone\b|\bnothing\b|\bwithout\b|\blacks?\b|\babsent\b|"
    r"\bdoes not\b|\bhas no\b|\bis no\b", re.I)
EVOPT = re.compile(r"evaluator[-\s]?optimi[sz]er", re.I)
RULED_OUT = re.compile(
    r"\bno\b|\bnot\b|\bnever\b|\bwithout\b|\brules? out\b|\bruled out\b|"
    r"\bforbid|\bcannot\b|\bcan not\b|\bdo(?:es)? not\b|\bavoid|\bunclaimed\b|"
    r"\bwould be\b|\bis wrong\b|\bnothing to\b", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Verification")
    if text is None:
        emit(CID, FAIL,
             "%s has no level-two `## Verification` section" % rel)

    validator = oracle = None
    for clause in clauses(text):
        if validator is None and SCHEMA.search(clause) and \
                EXTRACTION.search(clause):
            validator = clause
        if oracle is None and ORACLE.search(clause) and \
                PROSE.search(clause) and NO_ORACLE.search(clause):
            oracle = clause

    claimed = [c for c in clauses(body)
               if EVOPT.search(c) and not RULED_OUT.search(c)]

    problems = []
    if validator is None:
        problems.append("no clause puts the schema validator on the "
                        "extraction output")
    if oracle is None:
        problems.append("no clause says the report prose has no external "
                        "oracle")
    if claimed:
        problems.append("an evaluator-optimizer loop is claimed rather than "
                        "ruled out: %r" % claimed[0][:110])
    if problems:
        emit(CID, FAIL, "%s: %s" % (rel, "; ".join(problems)))

    loop = ("the evaluator-optimizer loop is explicitly ruled out"
            if EVOPT.search(body)
            else "no evaluator-optimizer loop is claimed anywhere in the file")
    emit(CID, PASS,
         "%s places the validator (%r) and states the prose has no oracle "
         "(%r); %s" % (rel, validator[:90], oracle[:90], loop))


if __name__ == "__main__":
    main()
