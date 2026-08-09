#!/usr/bin/env python3
"""Criterion 8: no glow on reading matter.

Every element whose computed font size is at or below 1.1rem and whose
own text runs longer than forty characters must compute
`text-shadow: none`. Radiance is for monuments; a paragraph is not one.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_probe,  # noqa: E402
                     require_section, scratch_dir)

CID = "c8"
BODY_MAX_REM = 1.1
READING_CHARS = 40


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    page = require_section(CID, doc)
    root_px = page.get("rootFontPx") or 16.0
    limit = BODY_MAX_REM * root_px

    reading = [e for e in page["elements"]
               if (e.get("fontSizePx") or 0) <= limit
               and len((e.get("ownText") or "").strip()) > READING_CHARS]
    if not reading:
        emit(CID, FAIL,
             "the services section carries no reading matter: no element at "
             "or below %.1fpx holds more than %d characters, so the four "
             "one-line descriptions the brief asked for are not there"
             % (limit, READING_CHARS))

    glowing = [e for e in reading if (e.get("textShadow") or "none") != "none"]
    if glowing:
        emit(CID, FAIL,
             "%d of %d reading-matter element(s) carry a text shadow: %s"
             % (len(glowing), len(reading),
                "; ".join("%s has %s" % (e["path"], e["textShadow"])
                          for e in glowing[:3])))

    emit(CID, PASS,
         "%d reading-matter element(s) at or below %.1fpx, all with "
         "text-shadow: none" % (len(reading), limit))


if __name__ == "__main__":
    main()
