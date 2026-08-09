#!/usr/bin/env python3
"""Criterion 4: three pressures named, each tied to the choice.

Naming is exact and mechanical: the eight pressure names from the card.
The tie is not, and this grader does not pretend otherwise. What it
checks is structural: the clause that names a pressure must also carry
a consequence, either a topology from the card or one of the words a
consequence is written with. That fails the failure the pack names, a
comma-separated list of pressures with nothing attached, and it passes
a clause that says the pressure licensed something. It cannot tell a
sound argument from an unsound one, and a reader still has to.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, clauses, emit, pressures_in,  # noqa: E402
                     require_output, section, split_front_matter,
                     topologies_in)

CID = "c4"
NEEDED = 3

CONSEQUENCE = re.compile(
    r"\blicen[cs]e|\blicens|\bforbid|\brules? out|\bdemand|\bargues? for|"
    r"\bjustif|\bbecause\b|\bso (?:we|the|it|that)\b|\btherefore\b|"
    r"\bwhich is why\b|\bdrives?\b|\bchose\b|\bchosen\b|\bpushed\b|"
    r"\bwe (?:picked|chose|take|accept)\b|\bveto", re.I)


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    text = section(body, "Pressures")
    if text is None:
        emit(CID, FAIL, "%s has no level-two `## Pressures` section" % rel)

    tied, untied = [], []
    for clause in clauses(text):
        found = pressures_in(clause)
        if not found:
            continue
        topologies = topologies_in(clause)
        consequence = CONSEQUENCE.search(clause)
        for name in found:
            if name in tied or name in untied:
                continue
            if topologies or consequence:
                tied.append(name)
            else:
                untied.append(name)

    # A pressure named without a consequence in one clause and with one
    # in another is tied: the record made the argument somewhere.
    untied = [n for n in untied if n not in tied]

    if len(tied) >= NEEDED:
        emit(CID, PASS,
             "%s ties %d pressures to the choice: %s"
             % (rel, len(tied), ", ".join(tied)))

    named = pressures_in(text)
    if not named:
        emit(CID, FAIL,
             "%s `## Pressures` names none of the eight pressures by name"
             % rel)
    emit(CID, FAIL,
         "%s `## Pressures` ties %d of the needed %d pressures to the choice "
         "(tied: %s). Named with nothing attached: %s"
         % (rel, len(tied), NEEDED, ", ".join(tied) or "none",
            ", ".join(untied) or "none"))


if __name__ == "__main__":
    main()
