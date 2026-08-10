#!/usr/bin/env python3
"""Criterion 4: both billing complaints are acknowledged and never timed out.

Items 12 and 35 are the two billing complaints in the seeded inbox. Each
needs `acknowledged_at` set, and neither may carry an auto-close timer
field anywhere in its record. The helpdesk in the fixture closes a
conversation 72 hours after the last customer reply; carrying that timer
onto a complaint is how a complaint closes itself unanswered.

An auto-close field is recognised by its name, anywhere in the record
including nested: `auto_close`, `autoCloseAt`, `close_timer`,
`closes_in`, `auto_resolve`. A record that keeps the timer under a name
none of those match is not caught, which is a limit of a name-based
check and is stated rather than papered over.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BILLING_ITEMS, FAIL, PASS, deep_keys, emit,  # noqa: E402
                     get, is_empty, load_triage, nkey, scratch_dir, text_of)

CID = "c4"

ACK_KEYS = ("acknowledged_at", "acknowledged_on", "acknowledgement_at",
            "acked_at", "acknowledged")
TIMER = re.compile(r"autoclos|autoresolve|clos(?:e|ing)timer|closesin|"
                   r"autoexpire|closecountdown")


def main():
    scratch = scratch_dir()
    by_id, err = load_triage(scratch)
    if err:
        emit(CID, FAIL, err)

    problems, good = [], []
    for num in BILLING_ITEMS:
        record = by_id.get(num)
        if record is None:
            problems.append("item %d has no record" % num)
            continue
        ack = get(record, *ACK_KEYS)
        if is_empty(ack):
            problems.append("item %d has no acknowledged_at" % num)
        timers = sorted({path for key, path in deep_keys(record)
                         if TIMER.search(nkey(key))})
        if timers:
            problems.append("item %d carries an auto-close timer field: %s"
                            % (num, ", ".join(timers[:3])))
        if not is_empty(ack) and not timers:
            good.append("%d acknowledged %s" % (num, text_of(ack)[:30]))

    if problems:
        emit(CID, FAIL, "; ".join(problems))
    emit(CID, PASS,
         "both billing complaints are acknowledged and neither carries an "
         "auto-close timer (%s)" % "; ".join(good))


if __name__ == "__main__":
    main()
