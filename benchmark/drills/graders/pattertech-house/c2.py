#!/usr/bin/env python3
"""Criterion 2: the lead times are not stat cards.

Read from computed style rather than from the stylesheet: no element in
the section carrying a numeric value may have both a four-sided border
and a box-shadow. That pair is the stat card, which the house does not
have; it has a plaque for the numbers an argument turns on and a ledger
meta column for everything else.

An element carries a numeric value when its whole text holds a digit
and runs to forty characters or fewer, so a value and its label count
and a paragraph that happens to mention a number does not. Nesting the
digit in an inner span does not get a bordered, shadowed wrapper off:
the wrapper's own text is short and numeric too.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_probe,  # noqa: E402
                     require_section, scratch_dir)

CID = "c2"
DIGIT = re.compile(r"\d")
VALUE_CHARS = 40


def carries_value(element):
    text = (element.get("text") or "").strip()
    return bool(text) and len(text) <= VALUE_CHARS and bool(DIGIT.search(text))


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    page = require_section(CID, doc)

    numeric = [e for e in page["elements"] if carries_value(e)]
    if not numeric:
        emit(CID, FAIL,
             "no element in the services section carries a numeric value, so "
             "the lead times the brief asked for are not on the page")

    bad = [e for e in numeric
           if e.get("borderAllFour") and (e.get("boxShadow") or "none") != "none"]
    if bad:
        emit(CID, FAIL,
             "%d element(s) carrying a numeric value have both a four-sided "
             "border and a box-shadow, which is a stat card: %s"
             % (len(bad), "; ".join("%s (%s)" % (e["path"], e.get("text"))
                                    for e in bad[:4])))

    emit(CID, PASS,
         "%d element(s) carry a numeric value and none has both a four-sided "
         "border and a box-shadow" % len(numeric))


if __name__ == "__main__":
    main()
