#!/usr/bin/env python3
"""Criterion 1: the four offerings are one ledger, not four panels.

A static parse of the built markup. Exactly one element in the page
carries `data-container="ledger"`, it sits in the services section, and
nothing inside that section carries `data-container="panel"`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_section, parse_html,  # noqa: E402
                     read, require_page, scratch_dir, service_titles)

CID = "c1"


def main():
    scratch = scratch_dir()
    page = require_page(CID, scratch)
    titles = service_titles(scratch)
    if len(titles) < 2:
        emit(CID, FAIL,
             "fixtures/services.json does not list the offerings, so the "
             "section cannot be located")

    root = parse_html(read(page))
    section = find_section(root, titles)
    if section is None:
        emit(CID, FAIL,
             "no element carries all %d offering titles, so the services "
             "section was never built" % len(titles))

    ledgers = [n for n in root.elements()
               if n.attrs.get("data-container") == "ledger"]
    if not ledgers:
        emit(CID, FAIL,
             "no element carries data-container=\"ledger\"; four parallel "
             "facts were not built as a ruled list")
    if len(ledgers) != 1:
        emit(CID, FAIL,
             "%d elements carry data-container=\"ledger\", expected exactly "
             "one: %s" % (len(ledgers), ", ".join(n.path() for n in ledgers)))

    ledger = ledgers[0]
    inside = ledger is section or section in list(ledger.ancestors())
    if not inside:
        emit(CID, FAIL,
             "the one ledger at %s is not inside the services section at %s"
             % (ledger.path(), section.path()))

    panels = [n for n in section.elements()
              if n.attrs.get("data-container") == "panel"]
    if panels:
        emit(CID, FAIL,
             "%d panel(s) inside the services section: %s. Four parallel "
             "facts must not become four boxes"
             % (len(panels), ", ".join(n.path() for n in panels)))

    emit(CID, PASS,
         "one ledger at %s inside the section, and no panel in it"
         % ledger.path())


if __name__ == "__main__":
    main()
