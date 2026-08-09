#!/usr/bin/env python3
"""Criterion 10: a review trigger naming an event, not a date alone.

"Review annually" is a diary entry. The criterion asks for the thing
that would make the document wrong, so the trigger has to be
conditional and it has to name something in particular. A conditional
with nothing in it, "revisit if anything changes", is the same diary
entry wearing an if, and is reported as such.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, _blocks, _items_from, emit,  # noqa: E402
                     content_words, flatten, one_line, scratch_dir,
                     sentences, the_doc)

CID = "c10"

CONTEXT = re.compile(
    r"\breview\b|\brevisit\b|\bre-?open\b|\binvalidat\w*\b|\breconsider\w*\b|"
    r"\bretire this\b|\bthis stops being true\b|\bexpir\w*\b|\btrigger\b",
    re.I)

EVENT = re.compile(
    r"\bif\b|\bwhen\b|\bonce\b|\bas soon as\b|\bwhenever\b|\bshould \w+\b|"
    r"\bon the day\b|\bthe moment\b|\bin the event\b|\bupon\b|"
    r"\bthe first time\b", re.I)

VAGUE = re.compile(
    r"\b(?:anything|something|things|circumstances|the market|conditions)\s+"
    r"(?:change|changes|move|moves|shift|shifts)\b|"
    r"\bif needed\b|\bas required\b|\bif necessary\b|\bwhen appropriate\b",
    re.I)

DATE_ONLY = re.compile(
    r"\bannual\w*\b|\bquarterly\b|\bmonthly\b|\bevery \d+ (?:months?|weeks?|"
    r"years?)\b|\bin \d+ months?\b|\b(?:19|20)\d{2}-\d{2}-\d{2}\b|"
    r"\bq[1-4]\b|\bnext (?:year|quarter)\b", re.I)


def units_of(text):
    """Sentences and list items, so a trigger written either way is read."""
    found = list(sentences(text))
    for _, lines in _blocks(text):
        found.extend(flatten(i) for i in _items_from(lines))
    seen, out = set(), []
    for unit in found:
        key = unit.lower()
        if unit and key not in seen:
            seen.add(key)
            out.append(unit)
    return out


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)

    best = None
    for where, text in docs:
        candidates = [u for u in units_of(text) if CONTEXT.search(u)]
        if not candidates:
            best = best or (
                where,
                "no review trigger at all: nothing says when this document "
                "should be reviewed, revisited or treated as invalid")
            continue

        dated = None
        vague = None
        for unit in candidates:
            if not EVENT.search(unit):
                if DATE_ONLY.search(unit) and dated is None:
                    dated = unit
                continue
            if VAGUE.search(unit):
                vague = vague or unit
                continue
            after = unit[EVENT.search(unit).start():]
            if len(content_words(after)) < 3:
                vague = vague or unit
                continue
            emit(CID, PASS,
                 "%s carries a review trigger naming an event: %r"
                 % (where, one_line(unit, 170)))

        if vague is not None:
            best = best or (
                where,
                "the review trigger is a condition with nothing in it: %r"
                % one_line(vague, 150))
            continue
        if dated is not None:
            best = best or (
                where,
                "the review trigger is a date or an interval and names no "
                "event: %r" % one_line(dated, 150))
            continue
        best = best or (
            where,
            "a review is mentioned but nothing says what would invalidate "
            "the document: %r" % one_line(candidates[0], 150))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
