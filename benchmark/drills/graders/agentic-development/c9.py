#!/usr/bin/env python3
"""Criterion 9: human approval gates the pull request.

A gate is a relation with a direction and a polarity, and this grader
now checks all three parts rather than the vocabulary they are written
with.

- both ends are present: a human approval and the externally visible
  act it stands in front of;
- the relation between them puts the approval first. `before`, `prior
  to` and `ahead of` want the approval on the left; `after`, `once`,
  `until` and `without` want it on the right; `requires`, `gates` and
  `subject to` read the same either way. So "the pull request is opened
  before any human approval" is refused for saying the order backwards;
- the approval is asserted. "No human approval is required before the
  pull request is opened" has both ends and the right relation word and
  states the opposite of a gate, which is exactly what the old
  bag-of-words check let through. Parity, so the two negations in "no
  pull request is opened without approval" cancel and the gate stands;
- and the requirement is asserted. "Approval before the pull request is
  not needed" negates neither end, only the verb between them, so the
  requirement word is read for polarity as well.

Clauses first, then whole list items, because a record that writes the
gate as two sentences joined by "then" has still written the gate.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, blocks, clauses, emit,  # noqa: E402
                     negated, require_output, section, split_front_matter)

CID = "c9"

APPROVAL = re.compile(r"approv\w*|sign[-\s]?offs?|signed off", re.I)
ACT = re.compile(r"pull requests?|\bPRs?\b|\bMRs?\b|merge requests?", re.I)

# Relations, and where they want the approval to sit.
PRE = re.compile(r"\bbefore\b|\bprior to\b|\bahead of\b|\bprecedes?\b|"
                 r"\bpreceding\b|\bin advance of\b|\bfirst\b", re.I)
POST = re.compile(r"\bafter\b|\bonce\b|\bwhen\b|\buntil\b|\bunless\b|"
                  r"\bwithout\b|\bfollowing\b|\bupon\b|\bpending\b|"
                  r"\bawaits?\b|\bwaits? for\b|\bon receipt of\b", re.I)
SYM = re.compile(r"\brequires?\b|\brequired\b|\bneeds?\b|\bneeded\b|"
                 r"\bgates?\b|\bgated\b|\bblocks?\b|\bblocked\b|"
                 r"\bdepends? on\b|\bdependent on\b|\bconditional on\b|"
                 r"\bcontingent on\b|\bsubject to\b|\bmandat\w*", re.I)


NEAR = 60


def _requirement_denied(clause, spans):
    """Is the requirement verb itself negated?

    "Approval before the pull request is not needed" puts the negation
    on the verb rather than on either end, and no amount of reading the
    two ends catches it. Only requirement words sitting near one of the
    ends are considered, so a stray "needs" elsewhere in a long bullet
    does not decide the criterion.
    """
    for match in SYM.finditer(clause):
        near = any(min(abs(match.start() - s[1]), abs(s[0] - match.end())) <=
                   NEAR for s in spans)
        if near and negated(clause, match.span()):
            return True
    return False


def _last_relation(text):
    """The relation nearest the second end, as (kind, word), or None."""
    best = None
    for kind, pattern in (("pre", PRE), ("post", POST), ("sym", SYM)):
        for match in pattern.finditer(text):
            if best is None or match.start() > best[2]:
                best = (kind, match.group(0), match.start())
    return None if best is None else (best[0], best[1])


def gate_in(clause):
    """(relation, approval-span) when the clause gates the act, else None."""
    approvals = [m.span() for m in APPROVAL.finditer(clause)]
    acts = [m.span() for m in ACT.finditer(clause)]
    partial = None
    for a in approvals:
        for b in acts:
            if a[1] <= b[0]:
                between, order = clause[a[1]:b[0]], "pre"
            elif b[1] <= a[0]:
                between, order = clause[b[1]:a[0]], "post"
            else:
                continue
            relation = _last_relation(between)
            if relation is None:
                continue
            kind, word = relation
            if kind not in (order, "sym"):
                partial = partial or (
                    "the order is written backwards: %r puts the act first"
                    % word)
                continue
            if negated(clause, a):
                partial = partial or (
                    "the approval is denied rather than required")
                continue
            if _requirement_denied(clause, (a, b)):
                partial = partial or (
                    "the requirement itself is denied, so the approval is "
                    "named and not asked for")
                continue
            return word, a
    return partial


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Approval")
    if text is None:
        emit(CID, FAIL, "%s has no level-two `## Approval` section" % rel)

    trouble = None
    near = []
    for unit in list(clauses(text)) + list(blocks(text)):
        found = gate_in(unit)
        if isinstance(found, tuple):
            emit(CID, PASS,
                 "%s gates the pull request on human approval, by %r: %r"
                 % (rel, found[0], unit[:140]))
        if isinstance(found, str) and trouble is None:
            trouble = (found, unit)
        if APPROVAL.search(unit) and ACT.search(unit):
            near.append(unit)

    if trouble is not None:
        emit(CID, FAIL,
             "%s `## Approval` names the approval and the pull request but "
             "%s: %r" % (rel, trouble[0], trouble[1][:140]))
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
