#!/usr/bin/env python3
"""Criterion 10: no script dependency.

The section's text content with scripting disabled must be
byte-identical to the same text with scripting on. The section is found
by the same content rule in both runs, so a section that only exists
once a script has run is a fail rather than a missing measurement.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_probe,  # noqa: E402
                     require_section, scratch_dir)

CID = "c10"


def first_difference(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, repr(a[max(0, i - 20):i + 20]), repr(b[max(0, i - 20):i + 20])
    return min(len(a), len(b)), repr(a[-40:]), repr(b[-40:])


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    require_section(CID, doc)

    with_js = doc.get("script_section_text")
    without = doc.get("noscript_section_text")
    if without is None:
        emit(CID, FAIL,
             "with scripting disabled no element carries the offering titles, "
             "so the section does not exist without JavaScript")
    if with_js is None:
        emit(CID, FAIL, "the section was not found in the scripted run")

    if with_js != without:
        where, left, right = first_difference(with_js, without)
        emit(CID, FAIL,
             "the section's text differs with scripting off, first at "
             "character %d: scripted %s, unscripted %s"
             % (where, left, right))

    emit(CID, PASS,
         "the section's text is identical with scripting on and off, %d "
         "characters" % len(with_js))


if __name__ == "__main__":
    main()
