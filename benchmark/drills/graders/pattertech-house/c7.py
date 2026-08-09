#!/usr/bin/env python3
"""Criterion 7: the contrast floor.

Measured from rendered colour, not from the token file: for every
element in the section carrying its own text, the computed foreground
composited onto its resolved backdrop must reach WCAG 2 contrast of
4.5:1, and body-tier text must reach 7:1.

The spec does not define body tier, so this grader states the reading
it uses rather than guessing at intent: body tier is the same reading
matter criterion 8 names, text at or below 1.1rem running longer than
forty characters. Display sizes, mono annotations and short labels are
held to 4.5:1 only. A different reading of body tier would move which
elements face the 7:1 floor; the 4.5:1 half is exact either way.

Where text sits over a background image the backdrop has no single
colour and no ratio can be computed. That is reported as unsettled
rather than as a pass or a fail.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, contrast, emit, over,  # noqa: E402
                     require_probe, require_section, scratch_dir)

CID = "c7"
FLOOR = 4.5
BODY_FLOOR = 7.0
BODY_MAX_REM = 1.1
READING_CHARS = 40


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    page = require_section(CID, doc)
    root_px = page.get("rootFontPx") or 16.0
    limit = BODY_MAX_REM * root_px

    carriers = [e for e in page["elements"]
                if (e.get("ownText") or "").strip() and e.get("visible")]
    if not carriers:
        emit(CID, FAIL,
             "no visible text in the services section, so there is nothing "
             "to measure")

    on_image = [e for e in carriers if e.get("bgImage")]
    if on_image:
        emit(CID, UNSETTLED,
             "%d text-carrying element(s) sit over a background image, which "
             "has no single resolved colour, so the ratio was not computed: "
             "%s" % (len(on_image), ", ".join(e["path"] for e in on_image[:3])))

    worst = None
    failures = []
    for element in carriers:
        text = (element.get("ownText") or "").strip()
        fg = over(element.get("color") or [0, 0, 0, 1], element.get("bg"))
        ratio = contrast(fg, element.get("bg"))
        body = (element.get("fontSizePx") or 0) <= limit and \
            len(text) > READING_CHARS
        need = BODY_FLOOR if body else FLOOR
        if worst is None or ratio < worst[0]:
            worst = (ratio, element["path"], need)
        if ratio + 0.005 < need:
            failures.append("%s is %.2f:1, needs %.1f:1"
                            % (element["path"], ratio, need))

    if failures:
        emit(CID, FAIL,
             "%d of %d text-carrying element(s) are under the contrast floor: "
             "%s" % (len(failures), len(carriers), "; ".join(failures[:4])))

    emit(CID, PASS,
         "%d text-carrying element(s) measured from rendered colour; the "
         "tightest is %s at %.2f:1 against a floor of %.1f:1"
         % (len(carriers), worst[1], worst[0], worst[2]))


if __name__ == "__main__":
    main()
