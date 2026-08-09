#!/usr/bin/env python3
"""Criterion 9: a position considered and rejected, with the reason.

The record of the road not taken is what separates a position from a
description. Two shapes are accepted, because both are honest:

- a sentence that says a position was rejected and why, in one breath;
- a section headed for rejected positions, where the heading carries
  the rejection and each entry carries its reason.

A list of rejected positions with no reasons fails, and says so. A
reason with no rejection is not this criterion.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, _blocks, _items_from, emit,  # noqa: E402
                     flatten, one_line, scratch_dir, sentences, the_doc)

CID = "c9"

REJECT = re.compile(
    r"\breject\w*\b|\bruled out\b|\bdiscard\w*\b|\bset aside\b|"
    r"\bturned down\b|\bdecided against\b|\bchose not to\b|"
    r"\bdid not take\b|\bnot taken\b|\bconsidered and (?:dropped|rejected)\b|"
    r"\bwe passed on\b|\bwe dropped\b|\bwe avoided\b", re.I)

SUBJECT = re.compile(
    r"\bposition\w*\b|\bframing\b|\bframe\b|\bangle\b|\bpitch\b|\bstory\b|"
    r"\bmessag\w*\b|\bcalling it\b|\bcalling ourselves\b|\bas the\b|"
    r"\bnarrativ\w*\b|\bclaim\b", re.I)

REASON = re.compile(
    r"\bbecause\b|\bsince\b|\bthe reason\b|\breason:\b|\bwhy not\b|"
    r"\bit would\b|\bthat would\b|\bwe would\b|\bwhich would\b|"
    r"\bleaves\b|\bfails\b|\binvites\b|\bcannot\b|\bcan't\b|\bdoes not\b|"
    r"\bno evidence\b|\bthe tickets\b|\bmeans we\b|\bputs us\b|"
    r"\bwe would lose\b|\bcompet\w* on price\b|\bwe do not\b", re.I)

HEADING = re.compile(
    r"reject|not taken|ruled out|discard|considered|alternative position|"
    r"positions? (?:we )?(?:considered|looked at)|roads? not taken|"
    r"other framings?", re.I)


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)

    best = None
    for where, text in docs:
        for sentence in sentences(text):
            if REJECT.search(sentence) and SUBJECT.search(sentence) \
                    and REASON.search(sentence):
                emit(CID, PASS,
                     "%s records a rejected position with its reason: %r"
                     % (where, one_line(sentence, 170)))

        found_section = False
        for heading, lines in _blocks(text):
            if not heading or not HEADING.search(heading):
                continue
            found_section = True
            items = [flatten(i) for i in _items_from(lines)]
            body = [s for s in sentences("\n".join(lines))]
            units = items or body
            if not units:
                best = best or (where,
                                "section %r is empty" % one_line(heading, 60))
                continue
            with_reason = [u for u in units if REASON.search(u)]
            if with_reason:
                emit(CID, PASS,
                     "%s: under %r, %d of %d entries carry a reason. First: "
                     "%r" % (where, one_line(heading, 60), len(with_reason),
                             len(units), one_line(with_reason[0], 150)))
            best = best or (
                where,
                "section %r lists %d rejected position(s) and gives a reason "
                "for none of them. First: %r"
                % (one_line(heading, 60), len(units),
                   one_line(units[0], 130)))

        if not found_section:
            rejected = next((s for s in sentences(text)
                             if REJECT.search(s)), None)
            if rejected is not None:
                best = best or (
                    where,
                    "something is rejected but not as a position with a "
                    "reason: %r" % one_line(rejected, 150))
            else:
                best = best or (
                    where,
                    "no position was recorded as considered and rejected: no "
                    "section for rejected positions and no sentence saying "
                    "one was ruled out")

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
