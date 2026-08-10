#!/usr/bin/env python3
"""Criterion 8: the restore drill actually passed, inside its objective.

`result` is pass, the run fitted inside the stated RTO, and something
was validated. Nothing here is a judgement: the three numbers are read
out of the evidence file and compared.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402

CID = "c8"
EVIDENCE = "evidence/restore-drill.json"


def number(doc, key):
    value = doc.get(key)
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def main():
    scratch = scratch_dir()
    path = scratch / EVIDENCE
    if not path.is_file():
        emit(CID, FAIL, "no %s, so no restore drill was recorded" % EVIDENCE)
    try:
        doc = json.loads(read(path))
    except ValueError as exc:
        emit(CID, FAIL, "%s does not parse: %s" % (EVIDENCE, exc))
    if not isinstance(doc, dict):
        emit(CID, FAIL, "%s is not a JSON object" % EVIDENCE)

    result = str(doc.get("result", "")).strip().lower()
    if result != "pass":
        emit(CID, FAIL,
             "result is %r, not \"pass\"" % doc.get("result"))

    elapsed = number(doc, "elapsed_seconds")
    rto = number(doc, "rto_seconds")
    rows = number(doc, "rows_validated")
    for key, value in (("elapsed_seconds", elapsed), ("rto_seconds", rto),
                       ("rows_validated", rows)):
        if value is None:
            emit(CID, FAIL,
                 "%s is %r, which is not a number" % (key, doc.get(key)))

    if elapsed > rto:
        emit(CID, FAIL,
             "the restore took %gs against an RTO of %gs" % (elapsed, rto))
    if rows <= 0:
        emit(CID, FAIL,
             "rows_validated is %g, so the restore proved nothing about the "
             "data" % rows)

    emit(CID, PASS,
         "result pass, %gs against an RTO of %gs, %g rows validated"
         % (elapsed, rto, rows))


if __name__ == "__main__":
    main()
