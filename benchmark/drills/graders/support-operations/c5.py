#!/usr/bin/env python3
"""Criterion 5: the five reports of one outage share one incident id.

Item 17 is the outage. Items 19, 21, 24 and 28 are four customers
reporting the same stalled export queue that morning, each independently.
All five records must carry the same incident id, and that id must be
the one in `incident-0001.json`.

Ids are compared with case and punctuation dropped, so `INC-0001` and
`inc0001` are the same id. Five different ids, or four out of five, is
the failure this criterion exists to catch: five conversations answered
five times by five people, which is what the fixture's rota notes say
keeps happening.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, OUTAGE_CLUSTER, PASS, emit, get,  # noqa: E402
                     is_empty, load_incident, load_triage, nkey,
                     scratch_dir, text_of)

CID = "c5"

REF_KEYS = ("incident_id", "incident", "incident_ref", "incident_key",
            "incident_number", "linked_incident", "incident_uid")
DOC_ID_KEYS = ("incident_id", "id", "incident", "incident_number",
               "incident_ref", "uid")


def reference(record):
    value = get(record, *REF_KEYS)
    if isinstance(value, dict):
        value = get(value, *DOC_ID_KEYS)
    return "" if is_empty(value) else text_of(value).strip()


def main():
    scratch = scratch_dir()
    by_id, err = load_triage(scratch)
    if err:
        emit(CID, FAIL, err)

    refs, missing = {}, []
    for num in OUTAGE_CLUSTER:
        record = by_id.get(num)
        if record is None:
            missing.append("item %d has no record" % num)
            continue
        ref = reference(record)
        if not ref:
            missing.append("item %d references no incident" % num)
            continue
        refs[num] = ref
    if missing:
        emit(CID, FAIL, "; ".join(missing))

    distinct = {nkey(r) for r in refs.values()}
    if len(distinct) != 1:
        emit(CID, FAIL,
             "the five reports of the outage carry %d different incident "
             "ids: %s" % (len(distinct),
                          ", ".join("%d=%s" % (n, refs[n])
                                    for n in sorted(refs))))

    shared = next(iter(refs.values()))
    doc, err = load_incident(scratch)
    if err:
        emit(CID, FAIL,
             "the five reports agree on %s but %s, so there is nothing to "
             "match it against" % (shared, err))
    doc_id = get(doc, *DOC_ID_KEYS)
    if is_empty(doc_id):
        emit(CID, FAIL,
             "incident-0001.json carries no id of its own, so the shared "
             "reference %s matches nothing" % shared)
    if nkey(text_of(doc_id)) != nkey(shared):
        emit(CID, FAIL,
             "the five reports share %s but incident-0001.json calls itself "
             "%s" % (shared, text_of(doc_id)))

    emit(CID, PASS,
         "items %s all reference %s, which is the id in incident-0001.json"
         % (", ".join(str(n) for n in OUTAGE_CLUSTER), shared))


if __name__ == "__main__":
    main()
