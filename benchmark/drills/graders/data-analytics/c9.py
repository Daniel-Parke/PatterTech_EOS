#!/usr/bin/env python3
"""Criterion 9: the stopping rule is named, and the interim is not cited.

Two parts, and the second is conditional. The answer has to say which
stopping rule it assumed, fixed horizon or sequential. If it assumed a
fixed horizon, it may not then reach back for the mid-run check as
evidence, because under a fixed horizon that reading does not exist: the
data was looked at once, at the end, by construction.

The fixture makes the temptation real. The lift is significant at the
8 May check and not at the end, so an answer that quietly leans on the
interim reading is claiming something the design it declared cannot
support.

Citing the interim in order to set it aside is the correct move and is
not an offence here: a sentence that names the mid-run check alongside a
negation or a discounting word is doing the right thing out loud.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, answer_files, emit, scratch_dir,  # noqa: E402
                     sentences)

CID = "c9"

FIXED = re.compile(r"(?i)fixed[- ]horizon|fixed[- ]sample|fixed[- ]duration|"
                   r"fixed[- ]n\b|pre[- ]?registered horizon|"
                   r"single (?:look|analysis) at the end|one look at the end")
SEQUENTIAL = re.compile(r"(?i)\bsequential\b|always[- ]valid|group sequential|"
                        r"alpha[- ]spending|msprt|mixture sequential")
NAMED = re.compile(r"(?i)stopping rule|stopping criteri|peek\w*|"
                   r"when to stop|analysis plan|stop(?:ping)? point")

INTERIM = re.compile(r"(?i)\binterim\b|\bmid[- ]?run\b|\bmid[- ]?test\b|"
                     r"\bmid[- ]?point\b|\bpeek\w*|8 May|May 8|2026-05-08|"
                     r"day 8\b|first eight days|first 8 days")
EVIDENCE = re.compile(r"(?i)\bsignificant\w*|\bevidence\b|\bshows?\b|"
                      r"\bproves?\b|\bdemonstrat\w+|\bconfirms?\b|"
                      r"\bsupports?\b|\bp\s*[<=]\s*0?\.|\blift\b|"
                      r"\bwins?\b|\bahead\b|\bbetter\b")
DISCOUNT = re.compile(
    r"(?i)\b(not|no|never|cannot|can't|do not|don't|does not|doesn't|"
    r"did not|didn't|is not|isn't|was not|wasn't|must not|should not|"
    r"discard\w*|ignore\w*|set aside|put aside|disregard\w*|inadmissible|"
    r"does not count|doesn't count|cannot count|invalid|illegitimate|"
    r"would be|only if|had we|if we had|inflate\w*|multiple comparisons|"
    r"peeking|not evidence|no evidence|not usable|unusable)\b")


def main():
    scratch = scratch_dir()
    answers = answer_files(scratch)
    if not answers:
        emit(CID, FAIL,
             "the delivery wrote no answer, so no stopping rule is named")

    rule = None
    where = None
    for relative, text in answers:
        if rule is None and FIXED.search(text):
            rule, where = "fixed horizon", relative
        elif rule is None and SEQUENTIAL.search(text):
            rule, where = "sequential", relative

    if rule is None:
        hinted = any(NAMED.search(t) for _, t in answers)
        emit(CID, FAIL,
             "no delivered answer names the stopping rule it assumed: "
             "nothing says fixed horizon and nothing says sequential%s"
             % ("; the phrase 'stopping rule' appears without a rule "
                "attached to it" if hinted else ""))

    if rule == "sequential":
        emit(CID, PASS,
             "%s names a sequential stopping rule, so the mid-run reading is "
             "part of the design and the interim clause does not apply"
             % where)

    for relative, text in answers:
        for sentence in sentences(text):
            if not INTERIM.search(sentence):
                continue
            if not EVIDENCE.search(sentence):
                continue
            if DISCOUNT.search(sentence):
                continue
            emit(CID, FAIL,
                 "%s assumes a fixed horizon and then cites the mid-run "
                 "check as evidence: %r"
                 % (relative, " ".join(sentence.split())[:160]))

    emit(CID, PASS,
         "%s names a fixed-horizon stopping rule and never cites the mid-run "
         "check as evidence for it" % where)


if __name__ == "__main__":
    main()
