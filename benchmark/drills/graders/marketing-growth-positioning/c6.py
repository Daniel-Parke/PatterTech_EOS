#!/usr/bin/env python3
"""Criterion 6: no superlative and no category-leadership claim.

The spec names four. The list here is those four and their near
relatives, because "industry-leading" and "leading" are the same move
and a criterion that catches one and not the other is a spelling test.

Quoted customer words and fenced code are not scanned. A document that
quotes a ticket verbatim should not fail on the customer's adjectives,
and the tickets in this repository do contain them.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, one_line, scratch_dir,  # noqa: E402
                     sentences, the_doc)

CID = "c6"

BANNED = (
    r"best[- ]in[- ]class", r"world[- ]class", r"best[- ]of[- ]breed",
    r"(?:industry|market|category|sector)[- ]leading",
    r"(?<!\w)leading(?!\s+(?:to|up|edge))",
    r"revolutionary", r"revolutionise\w*", r"game[- ]chang\w*",
    r"cutting[- ]edge", r"state[- ]of[- ]the[- ]art", r"bleeding[- ]edge",
    r"next[- ]generation", r"unrivalled", r"unrivaled", r"unmatched",
    r"unparalleled", r"second to none", r"number one", r"#1",
    r"the (?:best|fastest|easiest|simplest|most powerful|most advanced)",
    r"most advanced", r"most powerful", r"market leader", r"category leader",
    r"category king", r"premier", r"the only real", r"gold standard",
)
PATTERN = re.compile("|".join("(?:%s)" % b for b in BANNED), re.I)


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)

    clean = []
    for where, text in docs:
        offences = []
        for sentence in sentences(text):
            for match in PATTERN.finditer(sentence):
                offences.append((match.group(0), sentence))
        if offences:
            phrase, sentence = offences[0]
            emit(CID, FAIL,
                 "%s uses %d superlative or category-leadership claim(s). "
                 "First: %r in %r"
                 % (where, len(offences), phrase, one_line(sentence, 140)))
        clean.append(where)

    emit(CID, PASS,
         "%s carries no superlative and no category-leadership claim"
         % ", ".join(clean))


if __name__ == "__main__":
    main()
