#!/usr/bin/env python3
"""Criterion 4: the inventory covers the tree and holds no unresolved value.

This is the one aimed at the scan that ran, reported nothing and was
read as a pass. Two halves, and both are needed:

- Coverage. The component set is recomputed here from the delivered
  tree, by walking the pinned requirements through the metadata in
  `vendor/` and adding each vendored directory. An inventory that
  quietly dropped the awkward component would otherwise agree with
  itself.
- Resolution. No entry may sit at NOASSERTION, NONE or empty unless the
  decision record names that component, which is the pack's own escape
  hatch and the only one.

What this grader cannot settle, and does not pretend to: whether the
file was emitted by a scanner or typed by hand. It checks that the
inventory says what a scan over this tree would have had to say.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, best_inventory, decision_text,  # noqa: E402
                     emit, expected_components, is_unresolved, json_files,
                     named_in, scratch_dir)

CID = "c4"


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

    expected = expected_components(scratch)
    present = {row["name"] for row in rows}
    missing = sorted(n for n in expected if n not in present)
    if missing:
        emit(CID, FAIL,
             "%s has %d entries and misses %d component(s) the tree still "
             "contains: %s (%s)"
             % (name, len(rows), len(missing), ", ".join(missing),
                "; ".join("%s from %s" % (n, expected[n])
                          for n in missing[:4])))

    record = decision_text(scratch)
    unresolved = []
    for row in rows:
        if not is_unresolved(row["licence"]):
            continue
        if record and named_in(record, row["name"]):
            continue
        unresolved.append("%s (%s)" % (row["name"],
                                       row["licence"].strip() or "empty"))
    if unresolved:
        emit(CID, FAIL,
             "%s leaves %d component(s) with no licence value and no entry "
             "in a decision record: %s"
             % (name, len(unresolved), ", ".join(sorted(unresolved))))

    emit(CID, PASS,
         "%s covers all %d component(s) the tree carries and every entry "
         "either has a licence or is named in the decision record"
         % (name, len(expected)))


if __name__ == "__main__":
    main()
