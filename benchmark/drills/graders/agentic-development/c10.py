#!/usr/bin/env python3
"""Criterion 10: four evidence ids, two of them the pack's own.

The pack's own set is derived rather than hardcoded: the fragment file
`packs/agentic-development/research/sources.fragment.json` names the
sources this pack researched, and the estate registry gives each of
them an EV id. Either form of the id counts, which is what the
criterion says.

Deriving it means the check moves when the pack does. Where the
registry cannot be reached, the criterion is left unsettled rather than
decided on a guess about which ids belong to this pack: exit 2, which
the runner records as manual.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, distinct, emit,  # noqa: E402
                     read, repo_root, require_output)

CID = "c10"
NEEDED = 4
NEEDED_OWN = 2

ID = re.compile(r"\b(EV-\d{4}|FRAG-AGENTIC-DEVELOPMENT-\d{2})\b")
FRAGMENT_REL = "packs/agentic-development/research/sources.fragment.json"
REGISTRY_REL = "registry/evidence.json"


def pack_own_ids():
    """Every id that stands for a source this pack researched.

    Returns (ids, note) or (None, why-not).
    """
    root = repo_root()
    if root is None:
        return None, ("no EOS checkout above %s, so the pack's own set could "
                      "not be read" % Path(__file__).resolve().parent)
    fragment = Path(root) / FRAGMENT_REL
    registry = Path(root) / REGISTRY_REL
    if not fragment.is_file():
        return None, "the pack's fragment file is missing: %s" % FRAGMENT_REL
    try:
        records = json.loads(read(fragment)).get("records", [])
        rows = json.loads(read(registry)).get("records", [])
    except ValueError as exc:
        return None, "the pack fragment set or the registry does not parse: %s" % exc

    own = set()
    sources = set()
    for rec in records:
        if rec.get("id"):
            own.add(rec["id"])
        if rec.get("source"):
            sources.add(rec["source"])
    for row in rows:
        if row.get("source") in sources and row.get("id"):
            own.add(row["id"])
    if not own:
        return None, "the pack's fragment set lists no ids"
    return own, "%d ids stand for this pack's own sources" % len(own)


def main():
    _, rel, raw, prose = require_output(CID)
    cited = distinct(ID.findall(prose))

    if len(cited) < NEEDED:
        emit(CID, FAIL,
             "%s cites %d evidence id(s) and the criterion asks for %d: %s"
             % (rel, len(cited), NEEDED, ", ".join(cited) or "none"))

    own, note = pack_own_ids()
    if own is None:
        emit(CID, UNSETTLED,
             "%s cites %d ids (%s), but %s, so whether two of them are the "
             "pack's own was not settled here"
             % (rel, len(cited), ", ".join(cited), note))

    mine = [i for i in cited if i in own]
    if len(mine) < NEEDED_OWN:
        emit(CID, FAIL,
             "%s cites %d ids but only %d from the pack's own set (%s); the "
             "criterion asks for %d. Cited: %s"
             % (rel, len(cited), len(mine), ", ".join(mine) or "none",
                NEEDED_OWN, ", ".join(cited)))
    emit(CID, PASS,
         "%s cites %d evidence ids, %d of them the pack's own (%s)"
         % (rel, len(cited), len(mine), ", ".join(mine)))


if __name__ == "__main__":
    main()
