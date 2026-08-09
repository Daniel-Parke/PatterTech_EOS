#!/usr/bin/env python3
"""Criterion 2: the recorded philosophy's triggers match this brief.

The brief is fixed and frozen with the drill: expert pharmacists who
cannot go elsewhere, nine fields read at a glance, a ten-year-old
display under fluorescent light, print-adjacent output. Two of the
eight philosophies in GD-UIUX-001 carry triggers that fit a dense
expert tool, B (dense enterprise) and F (data-heavy dashboard), and the
grader accepts either.

The rest are refused for a stated reason rather than by taste. A is
plain language, one thing per page and generous targets, which is the
opposite of the density the client asked for in writing. C, D, E and G
answer briefs this is not: discretionary attention, reading at length,
a paid entry point, a platform store. H is an axis applied over one of
A to G rather than an answer to the density question on its own.

That mapping from this brief to that pair is a human judgement, made
once against a frozen brief and written down here, not a judgement the
script makes afresh on each run. It is the one place in this set where
a defensible alternative reading could lose, and the reason string says
which philosophy was rejected and why.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PHILOSOPHIES, emit, philosophies_in,  # noqa: E402
                     records, rel, runner_up_letters, scratch_dir)

CID = "c2"

FITS = {"B", "F"}

WHY_NOT = {
    "A": "content-first public service is one thing per page with generous "
         "targets, which contradicts the density the client asked for in "
         "writing",
    "C": "expressive consumer styling answers a discretionary-attention "
         "brief, and this tool is the one the trust bought",
    "D": "editorial answers reading at length, not nine fields checked "
         "dozens of times a shift",
    "E": "conversion-led answers a paid entry point with a money number, "
         "which this is not",
    "G": "mobile-native platform conformance answers a store build, and "
         "this runs on a ward desktop",
    "H": "restrained minimal is an axis applied over one of A to G, so on "
         "its own it does not answer the density question",
}


def main():
    scratch = scratch_dir()
    found = records(scratch)
    if not found:
        emit(CID, FAIL,
             "no philosophy record to read; criterion 1 covers that, and "
             "this one cannot run without it")

    best = None
    for path, text, chosen, runners in found:
        where = rel(scratch, path)
        letters = set()
        for _, value in chosen:
            letters |= philosophies_in(value)
        if len(letters) != 1:
            best = best or (where, "the record does not name exactly one "
                                   "philosophy, so its fit cannot be judged")
            continue
        letter = sorted(letters)[0]
        runner_letters = runner_up_letters(text, letter)
        if letter not in FITS:
            best = (where,
                    "names %s %s, whose triggers do not fit this brief: %s. "
                    "The brief fits B dense enterprise or F data-heavy "
                    "dashboard"
                    % (letter, PHILOSOPHIES[letter][0],
                       WHY_NOT.get(letter, "it answers a different brief")))
            continue
        if not runner_letters:
            best = (where,
                    "names %s %s, which fits, but names no runner-up; the "
                    "criterion asks for the philosophy given up as well as "
                    "the one taken"
                    % (letter, PHILOSOPHIES[letter][0]))
            continue
        emit(CID, PASS,
             "%s takes %s %s, whose triggers fit an expert tool read at "
             "density, and names %s as the runner-up"
             % (where, letter, PHILOSOPHIES[letter][0],
                ", ".join("%s %s" % (l, PHILOSOPHIES[l][0])
                          for l in sorted(runner_letters))))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
