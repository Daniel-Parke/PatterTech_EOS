#!/usr/bin/env python3
"""Criterion 6: numeric bounds, with units, for two of the three axes.

Turns, tokens and wall-clock. A number has to sit next to the unit it
bounds, in either order and within a short window, so "we will keep an
eye on turns" does not count and "at most 60 turns" does.

Two further things the number alone does not settle, both read per
clause rather than over the flattened section:

- the clause has to be bounding, not reporting. "The run took 6 turns"
  is a measurement; "at most 6 turns" is a limit. A short labelled row,
  `turns: 6`, is read as a limit because in a Bounds section that is
  what a labelled row is.
- the number has to be asserted. "There is no cap of 6 turns" and "no
  ceiling of 200k tokens" carry every token this grader looks for and
  set no bound at all, so a negated figure is refused and said out loud.

`no more than 60 turns` is a bound and not a denial, which the shared
cue reader knows: comparative idioms after a negation are excluded
there rather than special-cased here.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, clauses, emit, negated,  # noqa: E402
                     require_output, section, split_front_matter)

CID = "c6"
NEEDED = 2

NUM = r"\d[\d,._]*\s*[kKmM]?"
TIME = (r"seconds?|secs?|minutes?|mins?\b|hours?|hrs?\b")

AXES = [
    ("turns", [
        re.compile(r"(%s)\s*(?:agent\s+|tool\s+)?(?:turns?|tool calls?)\b"
                   % NUM, re.I),
        re.compile(r"\b(?:turns?|tool calls?)\b[^.\n]{0,24}?(%s)\b" % NUM,
                   re.I),
    ]),
    ("tokens", [
        re.compile(r"(%s)\s*tokens?\b" % NUM, re.I),
        re.compile(r"\btokens?\b[^.\n]{0,24}?(%s)\b" % NUM, re.I),
    ]),
    ("wall-clock", [
        re.compile(r"(%s)\s*(?:%s)" % (NUM, TIME), re.I),
    ]),
]

# The vocabulary a limit is written with, as against a measurement.
LIMIT = re.compile(
    r"\bat most\b|\bno more than\b|\bnot? (?:to )?exceed\b|\bup to\b|"
    r"\bmax(?:imum)?\b|\bcaps?\b|\bcapped\b|\bceilings?\b|\blimits?\b|"
    r"\blimited\b|\bbudgets?\b|\bbounds?\b|\bbounded\b|\bstops?\b|"
    r"\bhalts?\b|\baborts?\b|\bkills?\b|\bkilled\b|\btrips?\b|"
    r"\bthresholds?\b|\bwithin\b|\bunder\b|\bbelow\b|\bfewer than\b|"
    r"\bless than\b|<=|≤", re.I)
# `turns: 6`, `| tokens | 12000 |`: a labelled figure counts as a limit
# only where the row or the table's header says it is one. A table
# headed `| Axis | Last night | Note |` is a measurement table, and
# reading its rows as bounds is how "6, observed" becomes a cap.
LABELLED = re.compile(r"^\s*[-*|]?\s*[\w\s()/-]{0,32}[:|]\s*[^|]*\d", re.I)
# How far a limit word may sit from the figure it bounds. Far enough for
# "wall-clock stop at 45 minutes", short enough that "the 45 minutes it
# took last week is reported here, and nothing halts the run" does not
# borrow a limit word from the other half of the sentence.
NEAR = 30


def _distance(a, b):
    if a[0] < b[1] and b[0] < a[1]:
        return 0
    return b[0] - a[1] if a[1] <= b[0] else a[0] - b[1]


def header_says_limit(text):
    """Does a table header in the section call its figures limits?"""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and not set(line) <= set("|- :") \
                and LIMIT.search(line) and not re.search(r"\d", line):
            return True
    return False


def bounding(clause, span, header=False):
    """Is the figure at `span` presented as a limit rather than a count?"""
    if header and LABELLED.match(clause):
        return True
    for match in LIMIT.finditer(clause):
        if _distance(match.span(), span) > NEAR:
            continue
        if negated(clause, match.span()):
            continue
        return True
    return False


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Bounds")
    if text is None:
        emit(CID, FAIL, "%s has no level-two `## Bounds` section" % rel)

    found = {}
    refused = {}
    header = header_says_limit(text)
    for clause in clauses(text):
        for axis, patterns in AXES:
            if axis in found:
                continue
            for pattern in patterns:
                match = pattern.search(clause)
                if not match:
                    continue
                figure = " ".join(match.group(0).split())
                if negated(clause, match.span()):
                    refused.setdefault(axis, "denied: %r" % figure)
                elif not bounding(clause, match.span(), header):
                    refused.setdefault(axis, "reported, not bounded: %r"
                                       % figure)
                else:
                    found[axis] = figure
                break

    if len(found) >= NEEDED:
        emit(CID, PASS,
             "%s bounds %d axes: %s" % (rel, len(found),
                                        "; ".join("%s (%s)" % (a, v)
                                                  for a, v in found.items())))
    missing = [a for a, _ in AXES if a not in found]
    detail = "; ".join("%s %s" % (a, why) for a, why in refused.items())
    emit(CID, FAIL,
         "%s `## Bounds` sets a number with units for %d of the needed %d "
         "axes (%s). No limit set for: %s%s"
         % (rel, len(found), NEEDED,
            ", ".join(found) or "none", ", ".join(missing),
            ". " + detail if detail else ""))


if __name__ == "__main__":
    main()
