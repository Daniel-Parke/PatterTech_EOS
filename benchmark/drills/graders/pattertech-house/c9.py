#!/usr/bin/env python3
"""Criterion 9: no horizontal scroll.

At 375, 768 and 1280 the document's scroll width must not exceed the
window's inner width.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_probe,  # noqa: E402
                     require_section, scratch_dir)

CID = "c9"
WANTED = (375, 768, 1280)


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    require_section(CID, doc)

    rows = {row["width"]: row for row in doc.get("widths") or []}
    missing = [w for w in WANTED if w not in rows]
    if missing:
        emit(CID, FAIL,
             "the page was not measured at %s"
             % ", ".join(str(w) for w in missing))

    over = [rows[w] for w in WANTED
            if rows[w]["scrollWidth"] > rows[w]["innerWidth"]]
    if over:
        emit(CID, FAIL,
             "the page scrolls sideways at %s"
             % "; ".join("%dpx (scrollWidth %d against innerWidth %d)"
                         % (r["width"], r["scrollWidth"], r["innerWidth"])
                         for r in over))

    emit(CID, PASS,
         "no horizontal scroll at %s"
         % ", ".join("%dpx (%d <= %d)" % (w, rows[w]["scrollWidth"],
                                          rows[w]["innerWidth"])
                     for w in WANTED))


if __name__ == "__main__":
    main()
