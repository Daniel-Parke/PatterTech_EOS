#!/usr/bin/env python3
"""Criterion 7: the obligations file names four duties.

VAT, Making Tax Digital, cooling-off and a renewal reminder. A text
check, deliberately: the criterion asks whether the price carried its
duties across into a file someone will read, not whether the prose about
them is any good.

Whitespace is collapsed before matching, because a duty that wrapped
across a line break is still named, and a criterion that turns on where
the wrap landed measures the author's editor.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, OBLIGATIONS, PASS, emit, flatten,  # noqa: E402
                     read, scratch_dir)

CID = "c7"

DUTIES = (
    ("VAT", re.compile(r"\bVAT\b|\bvalue[\s-]added tax\b", re.I)),
    ("Making Tax Digital",
     re.compile(r"\bmaking\s+tax\s+digital\b", re.I)),
    ("cooling-off", re.compile(r"\bcooling[\s-]?off\b", re.I)),
    ("renewal reminder",
     re.compile(r"\brenewal\s+reminder|\breminder[^.]{0,60}\brenew|"
                r"\brenew\w*[^.]{0,60}\bremind", re.I)),
)


def main():
    scratch = scratch_dir()
    path = scratch / OBLIGATIONS
    if not path.is_file():
        emit(CID, FAIL, "no %s in the delivered tree" % OBLIGATIONS)

    text = flatten(read(path))
    if not text.strip():
        emit(CID, FAIL, "%s is empty" % OBLIGATIONS)

    missing = [name for name, pattern in DUTIES if not pattern.search(text)]
    if missing:
        emit(CID, FAIL,
             "%s does not name %s" % (OBLIGATIONS, ", ".join(missing)))

    emit(CID, PASS,
         "%s names VAT, Making Tax Digital, cooling-off and the renewal "
         "reminder" % OBLIGATIONS)


if __name__ == "__main__":
    main()
