#!/usr/bin/env python3
"""Criterion 9: the comms log shows three updates, and who each was for.

Three or more entries, timestamps strictly increasing, the first before
`resolved_at`, and each entry naming an audience. The first-before-
resolution clause is the one with teeth: a log written after the fact,
all of it stamped once the outage was over, is the "nobody told us
anything" the fixture's rota notes complain about.

An entry is a line carrying a timestamp, either plain text or a JSON
object per line. The audience test looks for an explicit `audience`
field first, and otherwise for a named group in the line: affected
customers, all customers, the status page, the internal channel,
finance, the exec, and so on. The vocabulary is listed below. It is a
keyword test and it can be fooled by a log that names its audience in
words nobody uses; that limit is stated here rather than hidden in a
pass.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_artefact, get,  # noqa: E402
                     load_incident, parse_dt, read, rel, scratch_dir,
                     text_of)

CID = "c9"

MIN_ENTRIES = 3

AUDIENCE_FIELD = re.compile(r"(?i)\baudience\b\s*[:=]")
AUDIENCE_WORD = re.compile(
    r"(?i)\b(customers?|accounts?|subscribers?|users?|clients?|"
    r"status ?page|forum|community|public|everyone|all affected|affected|"
    r"internal|staff|team|engineers?|engineering|on[- ]?call|support|"
    r"finance|sales|exec\w*|leadership|board|management|reporters?|"
    r"stakeholders?)\b")

TS = re.compile(
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?")


def entries(text):
    """(timestamp, line) for every log line that carries one."""
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("{"):
            try:
                doc = json.loads(line)
            except ValueError:
                doc = None
            if isinstance(doc, dict):
                stamp = parse_dt(get(doc, "at", "ts", "time", "timestamp",
                                     "sent_at", "posted_at", "when"))
                if stamp is not None:
                    out.append((stamp, line))
                    continue
        match = TS.search(line)
        if match:
            stamp = parse_dt(match.group(0))
            if stamp is not None:
                out.append((stamp, line))
    return out


def main():
    scratch = scratch_dir()
    path = find_artefact(scratch, "comms.log")
    if path is None:
        emit(CID, FAIL, "no comms.log: nothing records what anyone was told")
    where = rel(scratch, path)
    found = entries(read(path))
    if len(found) < MIN_ENTRIES:
        emit(CID, FAIL,
             "%s carries %d timestamped entr%s, fewer than the %d required"
             % (where, len(found), "y" if len(found) == 1 else "ies",
                MIN_ENTRIES))

    for (a, line_a), (b, _line_b) in zip(found, found[1:]):
        if b <= a:
            emit(CID, FAIL,
                 "%s: timestamps do not strictly increase, %s follows %s "
                 "(entry %r)" % (where, b.isoformat(), a.isoformat(),
                                 line_a[:60]))

    voiceless = [line for _stamp, line in found
                 if not AUDIENCE_FIELD.search(line)
                 and not AUDIENCE_WORD.search(line)]
    if voiceless:
        emit(CID, FAIL,
             "%s: %d entr%s name no audience, such as %r"
             % (where, len(voiceless), "y" if len(voiceless) == 1 else "ies",
                voiceless[0][:80]))

    doc, err = load_incident(scratch)
    if err:
        emit(CID, FAIL,
             "%s has %d increasing entries but %s, so there is no "
             "resolved_at to place the first one against"
             % (where, len(found), err))
    resolved = parse_dt(get(doc, "resolved_at"))
    if resolved is None:
        emit(CID, FAIL,
             "incident-0001.json has no readable resolved_at (%r), so the "
             "first comms entry cannot be placed before it"
             % text_of(get(doc, "resolved_at"))[:40])
    if found[0][0] >= resolved:
        emit(CID, FAIL,
             "%s: the first entry is stamped %s, at or after the incident "
             "was resolved at %s. Customers were told afterwards."
             % (where, found[0][0].isoformat(), resolved.isoformat()))

    emit(CID, PASS,
         "%s carries %d entries with strictly increasing timestamps, each "
         "naming an audience, the first at %s and resolution at %s"
         % (where, len(found), found[0][0].isoformat(), resolved.isoformat()))


if __name__ == "__main__":
    main()
