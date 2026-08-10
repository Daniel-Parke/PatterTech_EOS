#!/usr/bin/env python3
"""Criterion 3: section furniture in the fixed order.

A static parse. Inside the section header, the elements carrying a
`data-role` run index, rule, kicker, title, in that order. A further
role, the optional muted lead, may follow the title; none of the four
may be missing, reordered, or interrupted by another role.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, FURNITURE, PASS, emit, find_section,  # noqa: E402
                     parse_html, read, require_page, scratch_dir,
                     section_header, service_titles)

CID = "c3"


def main():
    scratch = scratch_dir()
    page = require_page(CID, scratch)
    titles = service_titles(scratch)
    root = parse_html(read(page))
    section = find_section(root, titles)
    if section is None:
        emit(CID, FAIL,
             "no element carries all the offering titles, so the services "
             "section and its header were never built")

    header = section_header(section)
    if header is None:
        emit(CID, FAIL,
             "the section at %s has no header and no element with "
             "data-role=\"title\", so it carries no section mark"
             % section.path())

    roles = [n.attrs["data-role"].strip() for n in header.elements()
             if n.attrs.get("data-role")]
    if not roles:
        emit(CID, FAIL,
             "the section header at %s carries no data-role attributes, so "
             "the furniture order cannot be read" % header.path())

    wanted = list(FURNITURE)
    if roles[:4] != wanted:
        missing = [r for r in wanted if r not in roles]
        detail = ("missing %s" % ", ".join(missing)) if missing else "out of order"
        emit(CID, FAIL,
             "the section header runs %s; expected %s (%s)"
             % (" then ".join(roles) or "nothing", " then ".join(wanted), detail))

    late = [r for r in roles[4:] if r in wanted]
    if late:
        emit(CID, FAIL,
             "the section header repeats furniture after the title: %s"
             % ", ".join(late))

    emit(CID, PASS,
         "the section header at %s runs %s"
         % (header.path(), " then ".join(roles)))


if __name__ == "__main__":
    main()
