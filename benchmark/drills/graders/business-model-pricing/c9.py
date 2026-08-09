#!/usr/bin/env python3
"""Criterion 9: at least three cited ids, and every one of them resolves.

The ledger is the estate's evidence register plus the fragment files the
packs hold, both read out of the repository this grader ships inside
rather than out of the tree being graded. A venture cannot make an id
resolve by writing it down twice.

Three is the floor and resolution is the test, so a file citing four ids
of which one is invented fails. An id that looks like a citation and
resolves nowhere is the failure this criterion exists for: the number of
citations is easy to reach and the truth of them is not.

Where the ledger cannot be found the criterion is unsettled rather than
failed. Nothing was looked at, and reporting that as a fail invents a
finding about work nobody read.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (EVIDENCE, FAIL, PASS, UNSETTLED, emit, read,  # noqa: E402
                     repo_root, scratch_dir)

CID = "c9"

MINIMUM = 3
EV = re.compile(r"\bEV-\d{3,5}\b")
FRAG = re.compile(r"\bFRAG-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")

LEDGER = "registry/evidence.json"
FRAGMENTS = "packs/*/research/*.fragment.json"


def ids_in(doc):
    records = doc.get("records") if isinstance(doc, dict) else doc
    if not isinstance(records, list):
        return set()
    return {str(r.get("id")).strip() for r in records
            if isinstance(r, dict) and r.get("id")}


def known():
    """Every id the estate can resolve, and where the set came from."""
    root = repo_root()
    found, sources = set(), []
    path = root / LEDGER
    if path.is_file():
        try:
            found |= ids_in(json.loads(path.read_text(encoding="utf-8")))
            sources.append(LEDGER)
        except ValueError:
            pass
    for fragment in sorted(root.glob(FRAGMENTS)):
        try:
            found |= ids_in(json.loads(fragment.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
        sources.append(fragment.relative_to(root).as_posix())
    return found, sources


def main():
    scratch = scratch_dir()
    path = scratch / EVIDENCE
    if not path.is_file():
        emit(CID, FAIL, "no %s in the delivered tree" % EVIDENCE)

    text = read(path)
    cited = sorted(set(EV.findall(text)) | set(FRAG.findall(text)))
    if len(cited) < MINIMUM:
        emit(CID, FAIL,
             "%s cites %d id(s) (%s); the floor is %d"
             % (EVIDENCE, len(cited), ", ".join(cited) or "none", MINIMUM))

    resolvable, sources = known()
    if not resolvable:
        emit(CID, UNSETTLED,
             "no evidence ledger found at %s and no pack fragment files, so "
             "the %d id(s) cited in %s were not resolved against anything"
             % (LEDGER, len(cited), EVIDENCE))

    unresolved = [i for i in cited if i not in resolvable]
    if unresolved:
        emit(CID, FAIL,
             "%s cites %s, which resolve nowhere in %s or the %d pack "
             "fragment file(s); a citation that resolves nowhere is a "
             "number of citations, not evidence"
             % (EVIDENCE, ", ".join(unresolved[:6]), LEDGER,
                max(len(sources) - 1, 0)))

    emit(CID, PASS,
         "%s cites %d id(s) and every one resolves: %s"
         % (EVIDENCE, len(cited), ", ".join(cited[:8])))


if __name__ == "__main__":
    main()
