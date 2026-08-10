#!/usr/bin/env python3
"""Criterion 4: flush left.

Computed `text-align` of the section header and of every heading in the
section is `left` or `start`. Anything else, `center` above all, fails.
Centring is reserved for monuments and an ordinary section is not one.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, require_probe,  # noqa: E402
                     require_section, scratch_dir)

CID = "c4"
ALLOWED = {"left", "start"}


def main():
    scratch = scratch_dir()
    doc = require_probe(CID, scratch)
    page = require_section(CID, doc)

    subjects = [e for e in page["elements"] if e.get("isHeader")]
    if not subjects:
        emit(CID, FAIL,
             "the services section has no header element and no element with "
             "data-role=\"title\", so it carries no section mark to measure")
    subjects += [e for e in page["elements"] if e.get("isHeading")]
    if len(subjects) < 2:
        emit(CID, FAIL,
             "the services section carries no heading, so it has no real "
             "heading structure to measure")

    bad = [e for e in subjects if (e.get("textAlign") or "") not in ALLOWED]
    if bad:
        emit(CID, FAIL,
             "%d of %d measured element(s) are not flush left: %s"
             % (len(bad), len(subjects),
                ", ".join("%s is %s" % (e["path"], e.get("textAlign"))
                          for e in bad[:4])))

    centred = [e for e in page["elements"]
               if (e.get("textAlign") or "") == "center"]
    emit(CID, PASS,
         "the section header and %d heading(s) compute to left or start, and "
         "%d element(s) in the section are centred"
         % (len(subjects) - 1, len(centred)))


if __name__ == "__main__":
    main()
