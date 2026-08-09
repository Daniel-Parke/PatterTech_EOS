#!/usr/bin/env python3
"""Criterion 1: the record reaches a verdict, in the three-word grammar.

`## Decision`, spelled exactly, and the first non-blank line under it is
`BUILD`, `TEST` or `KILL` on its own. The point of the fixed grammar is
that KILL stays sayable: a record that hedges in a paragraph has not
decided anything, and a reader cannot tell a refusal from a deferral.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISIONS, FAIL, PASS, RECORD, clip,  # noqa: E402
                     emit, first_non_blank, record_text, scratch_dir,
                     section, sections)

CID = "c1"


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)

    body = section(text, "Decision")
    if body is None:
        headings = [h for h in sections(text)]
        emit(CID, FAIL,
             "%s has no section headed exactly `## Decision`; its level-two "
             "headings are %s"
             % (RECORD, ", ".join(repr(h) for h in headings) or "none"))

    line = first_non_blank(body)
    if not line:
        emit(CID, FAIL, "`## Decision` in %s is empty" % RECORD)
    if line not in DECISIONS:
        emit(CID, FAIL,
             "the first non-blank line under `## Decision` is %r, and the "
             "grammar is one of %s on a line of its own"
             % (clip(line, 120), ", ".join(DECISIONS)))

    emit(CID, PASS,
         "`## Decision` opens with %s, so the record reached a verdict in "
         "the fixed grammar" % line)


if __name__ == "__main__":
    main()
