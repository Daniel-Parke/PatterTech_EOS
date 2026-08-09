#!/usr/bin/env python3
"""Criterion 8: thirty days is stated as the commercial default term.

The number and the thing it applies to have to sit in the same sentence.
A file with "30" somewhere and "payment terms" somewhere else has not
stated a term, and a grader matching them separately would pass a file
that says the trial is 30 days.

Numerals, per the pack's own C-08. A file that spells it "thirty days"
is told so in the reason rather than left to guess.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, OBLIGATIONS, PASS, emit, flatten,  # noqa: E402
                     read, scratch_dir)

CID = "c8"

DAYS = re.compile(r"\b30\s*(?:calendar\s+|working\s+|business\s+)?days?\b",
                  re.I)
WORDED = re.compile(r"\bthirty\s*(?:calendar\s+|working\s+|business\s+)?"
                    r"days?\b", re.I)
SUBJECT = re.compile(r"\bpayment\b|\binvoice|\bpay(?:able|ment)?\b|"
                     r"\bcommercial\s+(?:default|term)|\bterms?\b", re.I)
# A term is a default, not a trial length or a cooling-off window.
NOT_A_TERM = re.compile(r"\btrial\b|\bcooling[\s-]?off\b|\brefund\b|"
                        r"\bcancellation\s+period\b", re.I)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.;:])\s+|\n", text)
            if s.strip()]


def main():
    scratch = scratch_dir()
    path = scratch / OBLIGATIONS
    if not path.is_file():
        emit(CID, FAIL, "no %s in the delivered tree" % OBLIGATIONS)

    text = flatten(read(path))
    hits = []
    for sentence in sentences(text):
        if not DAYS.search(sentence):
            continue
        if NOT_A_TERM.search(sentence) and not SUBJECT.search(sentence):
            continue
        if SUBJECT.search(sentence):
            hits.append(sentence)

    if hits:
        emit(CID, PASS,
             "%s states the commercial default: %r"
             % (OBLIGATIONS, hits[0][:140]))

    if WORDED.search(text):
        emit(CID, FAIL,
             "%s spells the term out in words rather than numerals; the "
             "check reads 30, so a reader scanning for the number finds it"
             % OBLIGATIONS)
    if DAYS.search(text):
        emit(CID, FAIL,
             "%s mentions 30 days but not in a sentence about payment, an "
             "invoice or a term" % OBLIGATIONS)
    emit(CID, FAIL,
         "%s does not state 30 days as the commercial default payment term"
         % OBLIGATIONS)


if __name__ == "__main__":
    main()
