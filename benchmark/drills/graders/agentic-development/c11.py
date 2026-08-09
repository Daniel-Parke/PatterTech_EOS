#!/usr/bin/env python3
"""Criterion 11: voice and length.

No em-dash, no exclamation mark, British spellings, 120 lines or fewer.

Three of those four are exact. The spelling half is a blacklist and
nothing more: it catches the American forms a record like this actually
reaches for, and it cannot certify that everything else on the page is
British. A clean result here means no listed Americanism was found, and
the reason says so in those words rather than claiming more.

The canonical topology name evaluator-optimizer is removed before the
scan. The pack tells an agent to use that exact string, so flagging its
z would fail a record for obeying the pack.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_output,  # noqa: E402
                     strip_code)

CID = "c11"
MAX_LINES = 120

EM_DASH = "—"
# The house pattern: a bang closing a word, not one inside code.
BANG = re.compile(r"[A-Za-z]![\s\"')\]]|[A-Za-z]!$", re.M)

# -ize and -yze, which British spelling writes with an s. The stem
# length keeps size and prize out, and the allowed set holds the words
# that are spelled that way in both.
IZE = re.compile(r"\b(\w{4,}(?:iz|yz)(?:e|es|ed|ing|ation|ations|er|ers))\b",
                 re.I)
IZE_ALLOWED = {"capsize", "capsizes", "capsized", "capsizing", "downsize",
               "downsized", "downsizes", "downsizing", "resize", "resized",
               "resizes", "resizing", "oversize", "oversized"}

# The rest, as pairs, so the reason can say what was wanted instead.
WORDS = [
    (r"behaviors?\b", "behaviour"),
    (r"colors?\b", "colour"),
    (r"favor(?:s|ed|ing)?\b", "favour"),
    (r"honor(?:s|ed|ing)?\b", "honour"),
    (r"labor(?:s|ed|ing)?\b", "labour"),
    (r"defense\b", "defence"),
    (r"offense\b", "offence"),
    (r"centers?\b|centered\b|centering\b", "centre"),
    (r"catalogs?\b", "catalogue"),
    (r"fulfillment\b", "fulfilment"),
    (r"artifacts?\b", "artefact"),
    (r"modeling\b|modeled\b", "modelling"),
    (r"labeling\b|labeled\b", "labelling"),
    (r"canceled\b|canceling\b", "cancelled"),
    (r"traveled\b|traveling\b", "travelled"),
    (r"localization\b|localize(?:d|s)?\b", "localisation"),
]


def americanisms(text):
    text = re.sub(r"evaluator[-\s]?optimi[sz]er", " ", text, flags=re.I)
    found = []
    for match in IZE.finditer(text):
        word = match.group(1)
        if word.lower() not in IZE_ALLOWED:
            found.append("%s (British: %sise...)" % (word, word[:-3]))
    for pattern, british in WORDS:
        match = re.search(pattern, text, re.I)
        if match:
            found.append("%s (British: %s)" % (match.group(0), british))
    return found


def main():
    _, rel, raw, _prose = require_output(CID)
    lines = raw.splitlines()
    prose = strip_code(raw)

    problems = []
    if len(lines) > MAX_LINES:
        problems.append("%d lines, and the limit is %d"
                        % (len(lines), MAX_LINES))
    if EM_DASH in prose:
        problems.append("em-dash found")
    bang = BANG.search(prose)
    if bang:
        problems.append("exclamation mark in prose: %r"
                        % bang.group(0).strip())
    spellings = americanisms(prose)
    if spellings:
        problems.append("American spelling: %s" % ", ".join(spellings[:4]))

    if problems:
        emit(CID, FAIL, "%s: %s" % (rel, "; ".join(problems)))
    emit(CID, PASS,
         "%s is %d lines, has no em-dash and no exclamation mark, and no "
         "listed Americanism was found in it" % (rel, len(lines)))


if __name__ == "__main__":
    main()
