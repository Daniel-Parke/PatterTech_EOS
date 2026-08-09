#!/usr/bin/env python3
"""Criterion 7: resumption named, and resumed side effects idempotent.

The card gives two mechanisms and the criterion accepts either, so the
check is that one of them is named rather than that resumption is
promised. The second half is the one that carries the risk: code before
the interrupt runs again on resume, so a record that says a run resumes
without saying the replayed writes are idempotent has described the
easy half.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, flatten, require_output,  # noqa: E402
                     section, split_front_matter)

CID = "c7"

MECHANISMS = [
    ("checkpoint", re.compile(r"\bcheckpoint", re.I)),
    ("event log", re.compile(r"event[-\s]log|append[-\s]only (?:event )?"
                             r"(?:log|history)|event[-\s]driven resumable|"
                             r"\breplay", re.I)),
]
IDEMPOTENT = re.compile(r"idempoten", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Resumability")
    if text is None:
        emit(CID, FAIL,
             "%s has no level-two `## Resumability` section" % rel)
    flat = flatten(text)

    named = [name for name, pattern in MECHANISMS if pattern.search(flat)]
    idempotent = IDEMPOTENT.search(flat)

    problems = []
    if not named:
        problems.append("names neither checkpoint nor event-log resumption")
    if not idempotent:
        problems.append("never says the resumed side effects are idempotent")
    if problems:
        emit(CID, FAIL, "%s `## Resumability`: %s" % (rel,
                                                      "; ".join(problems)))
    emit(CID, PASS,
         "%s resumes by %s and states that resumed side effects are "
         "idempotent" % (rel, " and ".join(named)))


if __name__ == "__main__":
    main()
