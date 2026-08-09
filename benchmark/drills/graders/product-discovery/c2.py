#!/usr/bin/env python3
"""Criterion 2: the problem is not the requested feature under a heading.

`## Problem` exists and its body does not contain the name of the
feature the note asked for, case-insensitively. A problem section that
names the solution has restated the request and closed the question
before anyone looked at it.

The feature name is a fixed input of the drill rather than something
this grader infers from `request.md`, and `_common.require_feature_name`
checks it still occurs there before anything is graded. The bare token
is tested as well as the full phrase: a record that swaps the phrase for
the distinctive word has not reframed anything.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, FEATURE_TERMS, PASS, RECORD, clip,  # noqa: E402
                     emit, record_text, require_feature_name, scratch_dir,
                     section, sections)

CID = "c2"


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)
    feature = require_feature_name(CID)

    body = section(text, "Problem")
    if body is None:
        headings = [h for h in sections(text)]
        emit(CID, FAIL,
             "%s has no section headed exactly `## Problem`; its level-two "
             "headings are %s"
             % (RECORD, ", ".join(repr(h) for h in headings) or "none"))
    if not body.strip():
        emit(CID, FAIL, "`## Problem` in %s is empty" % RECORD)

    low = body.lower()
    for term in (feature,) + FEATURE_TERMS:
        at = low.find(term.lower())
        if at != -1:
            emit(CID, FAIL,
                 "`## Problem` names the requested feature: %r appears in "
                 "%r, so the section restates the solution rather than what "
                 "a person cannot do"
                 % (term, clip(body[max(0, at - 60):at + 80], 140)))

    emit(CID, PASS,
         "`## Problem` runs to %d characters and names neither %r nor %s, "
         "so the record framed a problem rather than the request"
         % (len(body.strip()), feature,
            ", ".join(repr(t) for t in FEATURE_TERMS)))


if __name__ == "__main__":
    main()
