#!/usr/bin/env python3
"""Criterion 1: pricing/decision.json exists and parses."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DECISION, FAIL, PASS, emit, scratch_dir  # noqa: E402

CID = "c1"

# Places a decision record turns up when the path was not read.
NEAR = ("decision.json", "pricing/pricing-decision.json",
        "pricing/decision.yaml", "pricing/decision.yml",
        "pricing/decision.md", "docs/pricing/decision.json",
        "pricing/pricing.json")


def main():
    scratch = scratch_dir()
    path = scratch / DECISION
    if not path.is_file():
        found = [n for n in NEAR if (scratch / n).is_file()]
        if found:
            emit(CID, FAIL,
                 "no %s; the nearest thing in the tree is %s, and the drill "
                 "names the path" % (DECISION, ", ".join(found)))
        emit(CID, FAIL, "no %s in the delivered tree" % DECISION)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        emit(CID, FAIL, "%s exists but does not parse: %s" % (DECISION, exc))
    if not isinstance(doc, dict):
        emit(CID, FAIL,
             "%s parses but holds a %s, not an object"
             % (DECISION, type(doc).__name__))
    emit(CID, PASS,
         "%s parses and holds %d top-level field(s)" % (DECISION, len(doc)))


if __name__ == "__main__":
    main()
