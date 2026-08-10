#!/usr/bin/env python3
"""Criterion 7: resumption named, and resumed side effects idempotent.

The card gives two mechanisms and the criterion accepts either, so the
check is that one of them is named rather than that resumption is
promised. The second half is the one that carries the risk: code before
the interrupt runs again on resume, so a record that says a run resumes
without saying the replayed writes are idempotent has described the
easy half.

Both halves are read per clause and for polarity. "There is no
checkpoint at the join barrier" names the mechanism and rules it out;
"resumed side effects are not idempotent" says the exact thing this
criterion exists to catch. Neither is an answer, and the flat search
this grader used to run could not tell them from one.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, asserts, clauses, emit,  # noqa: E402
                     require_output, section, split_front_matter)

CID = "c7"

MECHANISMS = [
    ("checkpoint", re.compile(r"\bcheckpoint\w*", re.I)),
    ("event log", re.compile(r"event[-\s]logs?|append[-\s]only (?:event )?"
                             r"(?:log|history)|event[-\s]driven resumable|"
                             r"\breplay\w*", re.I)),
]
IDEMPOTENT = re.compile(r"idempoten\w*", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Resumability")
    if text is None:
        emit(CID, FAIL,
             "%s has no level-two `## Resumability` section" % rel)
    parts = clauses(text)

    named, refused = [], []
    for name, pattern in MECHANISMS:
        if any(asserts(clause, pattern) is not None for clause in parts):
            named.append(name)
        elif pattern.search(text):
            refused.append(name)
    idempotent = any(asserts(clause, IDEMPOTENT) is not None
                     for clause in parts)

    problems = []
    if not named:
        if refused:
            problems.append("names %s only to rule it out, so no resumption "
                            "mechanism is chosen" % " and ".join(refused))
        else:
            problems.append("names neither checkpoint nor event-log "
                            "resumption")
    if not idempotent:
        if IDEMPOTENT.search(text):
            problems.append("says the resumed side effects are *not* "
                            "idempotent")
        else:
            problems.append("never says the resumed side effects are "
                            "idempotent")
    if problems:
        emit(CID, FAIL, "%s `## Resumability`: %s" % (rel,
                                                      "; ".join(problems)))
    emit(CID, PASS,
         "%s resumes by %s and states that resumed side effects are "
         "idempotent" % (rel, " and ".join(named)))


if __name__ == "__main__":
    main()
