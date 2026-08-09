#!/usr/bin/env python3
"""Criterion 6: numeric bounds, with units, for two of the three axes.

Turns, tokens and wall-clock. A number has to sit next to the unit it
bounds, in either order and within a short window, so "we will keep an
eye on turns" does not count and "at most 60 turns" does.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, flatten, require_output,  # noqa: E402
                     section, split_front_matter)

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


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Bounds")
    if text is None:
        emit(CID, FAIL, "%s has no level-two `## Bounds` section" % rel)
    flat = flatten(text)

    found = {}
    for axis, patterns in AXES:
        for pattern in patterns:
            match = pattern.search(flat)
            if match:
                found[axis] = " ".join(match.group(0).split())
                break

    if len(found) >= NEEDED:
        emit(CID, PASS,
             "%s bounds %d axes: %s" % (rel, len(found),
                                        "; ".join("%s (%s)" % (a, v)
                                                  for a, v in found.items())))
    missing = [a for a, _ in AXES if a not in found]
    emit(CID, FAIL,
         "%s `## Bounds` gives a number with units for %d of the needed %d "
         "axes (%s). No numeric limit found for: %s"
         % (rel, len(found), NEEDED,
            ", ".join(found) or "none", ", ".join(missing)))


if __name__ == "__main__":
    main()
