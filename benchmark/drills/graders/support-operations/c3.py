#!/usr/bin/env python3
"""Criterion 3: the three items with no reproduction detail are held open.

Items 9, 22 and 31 of the seeded inbox say only that something is
broken. Each must be `needs-info` and carry a `next_action_due` strictly
after the run date, which is the export clock in `export-manifest.json`
(2026-08-07). A due date on the run date itself is not after it, so it
fails: the point of the field is that someone comes back to the item.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, NO_REPRO_ITEMS, PASS, emit, get,  # noqa: E402
                     is_empty, load_triage, nkey, parse_dt, run_clock,
                     scratch_dir, text_of)

CID = "c3"

STATE_KEYS = ("triage_state", "state", "triage_status", "status")
DUE_KEYS = ("next_action_due", "next_action_due_at", "next_action_due_date",
            "next_action_date", "next_action_by", "follow_up_due",
            "next_action")


def main():
    scratch = scratch_dir()
    by_id, err = load_triage(scratch)
    if err:
        emit(CID, FAIL, err)
    clock = run_clock(scratch)
    run_date = clock.date()

    problems, good = [], []
    for num in NO_REPRO_ITEMS:
        record = by_id.get(num)
        if record is None:
            problems.append("item %d has no record" % num)
            continue
        state = nkey(text_of(get(record, *STATE_KEYS)))
        if state != "needsinfo":
            problems.append("item %d is %s, not needs-info"
                            % (num, state or "unclassified"))
        raw = get(record, *DUE_KEYS)
        if is_empty(raw):
            problems.append("item %d carries no next_action_due" % num)
            continue
        due = parse_dt(raw)
        if due is None:
            problems.append("item %d has next_action_due %r, which is not a "
                            "date" % (num, text_of(raw)[:40]))
            continue
        if due.date() <= run_date:
            problems.append("item %d is due %s, which is not after the run "
                            "date %s" % (num, due.date(), run_date))
            continue
        good.append("%d due %s" % (num, due.date()))

    if problems:
        emit(CID, FAIL, "; ".join(problems))
    emit(CID, PASS,
         "items %s are needs-info with a next action after the run date %s "
         "(%s)" % (", ".join(str(n) for n in NO_REPRO_ITEMS), run_date,
                   "; ".join(good)))


if __name__ == "__main__":
    main()
