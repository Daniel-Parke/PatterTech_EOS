#!/usr/bin/env python3
"""Criterion 2: every record is classified, and the queues partition.

Each record carries a non-empty `kind`, `priority`, `queue` and
`triage_state`, the state is `accepted` or `needs-info`, and the queue
column names at least an incident queue and a request queue with no
record standing in both.

`needs_info`, `needs-info` and `Needs Info` are the same state: the
comparison drops case and punctuation. A record whose queue is a list
holding both an incident and a request queue is what "no record in
both" forbids, so that is the failure looked for.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, get, is_empty, load_triage,  # noqa: E402
                     nkey, scratch_dir, text_of)

CID = "c2"

STATES = {"accepted", "needsinfo"}
REQUIRED = ("kind", "priority", "queue", "triage_state")
ALIASES = {
    "kind": ("kind", "type", "category"),
    "priority": ("priority", "prio"),
    "queue": ("queue", "queues"),
    "triage_state": ("triage_state", "state", "triage_status", "status"),
}


def queue_tokens(value):
    """The queue names on one record, normalised."""
    if isinstance(value, (list, tuple, set)):
        return {nkey(v) for v in value if not is_empty(v)}
    return {nkey(text_of(value))} if not is_empty(value) else set()


def main():
    scratch = scratch_dir()
    by_id, err = load_triage(scratch)
    if err:
        emit(CID, FAIL, err)

    blank, bad_state, both = [], [], []
    incident_ids, request_ids = [], []
    for num in sorted(by_id):
        record = by_id[num]
        for field in REQUIRED:
            if is_empty(get(record, *ALIASES[field])):
                blank.append("item %d has no %s" % (num, field))
        state = nkey(text_of(get(record, *ALIASES["triage_state"])))
        if state and state not in STATES:
            bad_state.append("item %d is %r" % (num, state))
        tokens = queue_tokens(get(record, *ALIASES["queue"]))
        in_incident = any("incident" in t for t in tokens)
        in_request = any("request" in t for t in tokens)
        if in_incident and in_request:
            both.append(num)
        if in_incident:
            incident_ids.append(num)
        if in_request:
            request_ids.append(num)

    problems = []
    if blank:
        problems.append("%d missing field(s): %s"
                        % (len(blank), "; ".join(blank[:5])))
    if bad_state:
        problems.append("triage_state must be accepted or needs-info: %s"
                        % "; ".join(bad_state[:5]))
    if not incident_ids:
        problems.append("no record sits in an incident queue")
    if not request_ids:
        problems.append("no record sits in a request queue")
    if both:
        problems.append("item(s) %s sit in both the incident and the request "
                        "queue" % ", ".join(str(b) for b in both[:6]))
    if problems:
        emit(CID, FAIL, "; ".join(problems))

    emit(CID, PASS,
         "all %d records carry kind, priority, queue and triage_state; the "
         "queue splits %d incident and %d request with no record in both"
         % (len(by_id), len(incident_ids), len(request_ids)))


if __name__ == "__main__":
    main()
