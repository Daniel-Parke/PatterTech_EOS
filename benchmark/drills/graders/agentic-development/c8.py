#!/usr/bin/env python3
"""Criterion 8: the validator on the extraction, and nothing on the prose.

Three things, all in the Verification section unless stated otherwise:

- the schema validator is placed on the extraction output;
- the report prose is said to have no external oracle;
- no evaluator-optimizer loop is claimed for that prose.

This is the one criterion that wants both polarities, so it asks for
each of them by name. The first is an assertion: a clause that says the
validator does *not* hold truth for the extraction has placed nothing.
The second is a denial: the record has to say the prose has no oracle,
and "the prose does not lack an oracle" is the opposite claim written
with the same words, which parity catches. The third is a prohibition
checked across the whole file rather than the section, because a loop
claimed anywhere is still claimed: where the string appears, every
appearance has to be negated. Where it never appears, nothing was
claimed and the criterion is satisfied on that point, which the reason
says plainly rather than reporting a check that did not happen as a
pass.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, asserts, clauses, denies,  # noqa: E402
                     emit, require_output, section, split_front_matter)

CID = "c8"

SCHEMA = re.compile(r"schema|validator", re.I)
EXTRACTION = re.compile(r"extract\w*", re.I)
ORACLE = re.compile(r"\boracle\w*", re.I)
PROSE = re.compile(r"\bprose\b|\breports?\b|narrative|write[-\s]?up|"
                   r"roll[-\s]?up", re.I)
EVOPT = re.compile(r"evaluator[-\s]?optimi[sz]er", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Verification")
    if text is None:
        emit(CID, FAIL,
             "%s has no level-two `## Verification` section" % rel)

    validator = oracle = None
    validator_denied = oracle_claimed = None
    for clause in clauses(text):
        if SCHEMA.search(clause) and EXTRACTION.search(clause):
            if (asserts(clause, SCHEMA) is not None
                    and asserts(clause, EXTRACTION) is not None):
                validator = validator or clause
            else:
                validator_denied = validator_denied or clause
        if ORACLE.search(clause) and PROSE.search(clause):
            if denies(clause, ORACLE) is not None:
                oracle = oracle or clause
            else:
                oracle_claimed = oracle_claimed or clause

    claimed = [c for c in clauses(body) if asserts(c, EVOPT) is not None]

    problems = []
    if validator is None:
        if validator_denied is not None:
            problems.append("the clause about the schema validator denies "
                            "that it holds truth for the extraction: %r"
                            % validator_denied[:110])
        else:
            problems.append("no clause puts the schema validator on the "
                            "extraction output")
    if oracle is None:
        if oracle_claimed is not None:
            problems.append("the clause about the prose claims an oracle "
                            "rather than saying there is none: %r"
                            % oracle_claimed[:110])
        else:
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
