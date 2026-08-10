#!/usr/bin/env python3
"""Criterion 7: the incident record is complete and dated sensibly.

`incident-0001.json` carries all eight named keys, its `severity` is a
band the policy defines, and `postmortem_due` is at most five days after
`resolved_at`.

The severity match is made on the bare characters: `SEV-2`, `Sev 2` and
`sev2` all reduce to `sev2`, and that has to appear in the policy. A
severity the policy never names is the failure worth catching, because a
band invented at the moment of the incident is the thing the policy
exists to stop.
"""

import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_artefact, get,  # noqa: E402
                     is_empty, load_incident, nkey, parse_dt, read, rel,
                     scratch_dir, text_of)

CID = "c7"

REQUIRED = ("severity", "declared_at", "declared_by", "comms_owner",
            "fix_owner", "customers_affected", "resolved_at",
            "postmortem_due")
MAX_POSTMORTEM_DAYS = 5


def main():
    scratch = scratch_dir()
    doc, err = load_incident(scratch)
    if err:
        emit(CID, FAIL, err)

    # `customers_affected: 0` is a value, not an absence, and is_empty
    # says so: only None, blank strings and empty containers count.
    missing = [k for k in REQUIRED if is_empty(get(doc, k))]
    if missing:
        emit(CID, FAIL,
             "incident-0001.json is missing or leaves empty: %s"
             % ", ".join(missing))

    policy = find_artefact(scratch, "severity_policy.md")
    if policy is None:
        emit(CID, FAIL,
             "incident-0001.json declares severity %s but there is no "
             "severity_policy.md defining any band"
             % text_of(get(doc, "severity"))[:40])
    band = text_of(get(doc, "severity")).strip()
    policy_text = nkey(read(policy))
    if len(nkey(band)) < 2 or nkey(band) not in policy_text:
        emit(CID, FAIL,
             "severity %r is not a band defined in %s"
             % (band[:40], rel(scratch, policy)))

    resolved = parse_dt(get(doc, "resolved_at"))
    due = parse_dt(get(doc, "postmortem_due"))
    if resolved is None:
        emit(CID, FAIL, "resolved_at %r is not a date"
                        % text_of(get(doc, "resolved_at"))[:40])
    if due is None:
        emit(CID, FAIL, "postmortem_due %r is not a date"
                        % text_of(get(doc, "postmortem_due"))[:40])
    gap = due - resolved
    if gap > _dt.timedelta(days=MAX_POSTMORTEM_DAYS):
        emit(CID, FAIL,
             "postmortem_due is %.1f days after resolved_at, more than the "
             "%d the criterion allows"
             % (gap.total_seconds() / 86400.0, MAX_POSTMORTEM_DAYS))

    emit(CID, PASS,
         "incident-0001.json carries all eight keys, severity %s is defined "
         "in %s, and the postmortem is due %.1f days after resolution"
         % (band, rel(scratch, policy), gap.total_seconds() / 86400.0))


if __name__ == "__main__":
    main()
