#!/usr/bin/env python3
"""Criterion 1: triage.json parses and holds exactly 40 records.

One record per inbox item, no duplicates and no extras. Ids are read
punctuation-blind, so `17`, `"0017"` and `"item-17"` are the same item;
what is graded is coverage of the seeded inbox, not a numbering style.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, ITEM_COUNT, PASS, emit, find_artefact,  # noqa: E402
                     load_json, normalise_id, rel, scratch_dir,
                     triage_records)

CID = "c1"


def main():
    scratch = scratch_dir()
    path = find_artefact(scratch, "triage.json")
    if path is None:
        emit(CID, FAIL, "no triage.json: the run produced nothing to grade")
    where = rel(scratch, path)
    doc, err = load_json(path)
    if err:
        emit(CID, FAIL, "%s %s" % (where, err))

    records, note = triage_records(doc)
    if not records:
        emit(CID, FAIL, "%s parses but %s" % (where, note))

    seen, unreadable, duplicates = {}, [], []
    for raw, _record in records:
        num = normalise_id(raw)
        if num is None:
            unreadable.append(repr(raw))
            continue
        if num in seen:
            duplicates.append(num)
        seen[num] = seen.get(num, 0) + 1

    expected = set(range(1, ITEM_COUNT + 1))
    missing = sorted(expected - set(seen))
    extra = sorted(set(seen) - expected)

    problems = []
    if len(records) != ITEM_COUNT:
        problems.append("%d records, expected %d" % (len(records), ITEM_COUNT))
    if unreadable:
        problems.append("%d record(s) carry no readable item id (%s)"
                        % (len(unreadable), ", ".join(unreadable[:4])))
    if duplicates:
        problems.append("duplicate item ids: %s"
                        % ", ".join(str(d) for d in sorted(set(duplicates))))
    if missing:
        problems.append("no record for item(s) %s"
                        % ", ".join(str(m) for m in missing[:8]))
    if extra:
        problems.append("record(s) for item(s) not in the inbox: %s"
                        % ", ".join(str(e) for e in extra[:8]))
    if problems:
        emit(CID, FAIL, "%s: %s" % (where, "; ".join(problems)))

    emit(CID, PASS,
         "%s parses (%s) and holds exactly %d records, one per inbox item"
         % (where, note, ITEM_COUNT))


if __name__ == "__main__":
    main()
