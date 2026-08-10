#!/usr/bin/env python3
"""Criterion 6: reduced motion.

Two halves, and both must hold. The CSS the page loads carries a
`@media (prefers-reduced-motion: reduce)` block, and under emulation
every element on the page returns computed `animation-play-state:
paused` or `animation-name: none`. Element pseudos count, because the
house puts most of its light on `::before` and `::after`, and a kill
switch that misses them is not a kill switch.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_css, emit, reduced_motion_blocks,  # noqa: E402
                     require_probe, require_section, scratch_dir)

CID = "c6"


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    page = require_section(CID, doc)
    _ = page

    blocks = reduced_motion_blocks(all_css(scratch))
    if not blocks:
        emit(CID, FAIL,
             "the CSS the page loads has no @media "
             "(prefers-reduced-motion: reduce) block")

    reduced = doc.get("reduced") or {}
    if not reduced.get("matches"):
        emit(CID, FAIL,
             "the reduced-motion emulation did not take, so the criterion "
             "was not measured")
    bad = reduced.get("violations") or []
    if bad:
        emit(CID, FAIL,
             "%d element(s) still animate under reduced motion, first: %s"
             % (len(bad), "; ".join(
                 "%s runs %s (%s)" % (b["path"], b["animationName"],
                                      b["playState"]) for b in bad[:4])))

    emit(CID, PASS,
         "%d reduced-motion block(s) in the CSS, and all %d element and "
         "pseudo-element styles measured under emulation return a paused or "
         "absent animation" % (len(blocks), reduced.get("checked", 0)))


if __name__ == "__main__":
    main()
