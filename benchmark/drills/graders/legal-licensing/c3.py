#!/usr/bin/env python3
"""Criterion 3: the choice expression was resolved to one identifier.

`MIT OR GPL-2.0-only` is a decision the project has to make. Copying it
into the inventory looks like an answer and is not one: which set of
obligations applies stays undetermined. So the entry for the
dual-licensed component has to read as exactly one identifier.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DUAL_LICENSED, FAIL, PASS, best_inventory,  # noqa: E402
                     emit, json_files, normalise_name, scratch_dir)

CID = "c3"

ACCEPTED = re.compile(r"^(MIT|GPL-2\.0-only)$")


def main():
    scratch = scratch_dir()
    name, rows = best_inventory(scratch)
    if rows is None:
        found = json_files(scratch)
        emit(CID, FAIL,
             "no inventory in the tree that parses into components; %s"
             % ("read %d JSON file(s) and none held a component list: %s"
                % (len(found), ", ".join(found[:5])) if found
                else "there is no JSON file to read"))

    wanted = normalise_name(DUAL_LICENSED)
    entries = [row for row in rows if row["name"] == wanted]
    if not entries:
        emit(CID, FAIL,
             "%s parses with %d component(s) but has no entry for %s, the "
             "one component whose licence is a choice; a scan that lost it "
             "cannot have resolved it"
             % (name, len(rows), DUAL_LICENSED))

    for row in entries:
        value = (row["licence"] or "").strip()
        if ACCEPTED.match(value):
            emit(CID, PASS,
                 "%s records %s as %s, one identifier rather than the raw "
                 "expression" % (name, DUAL_LICENSED, value))

    value = (entries[0]["licence"] or "").strip()
    if not value:
        emit(CID, FAIL,
             "%s carries an empty licence for %s" % (name, DUAL_LICENSED))
    if re.search(r"\bOR\b", value, re.I):
        emit(CID, FAIL,
             "%s still carries the raw choice %r for %s: the expression was "
             "copied across, not decided" % (name, value, DUAL_LICENSED))
    emit(CID, FAIL,
         "%s records %s as %r, which is neither MIT nor GPL-2.0-only, the "
         "two the component actually offers" % (name, DUAL_LICENSED, value))


if __name__ == "__main__":
    main()
