#!/usr/bin/env python3
"""Criterion 1: a philosophy record exists, names one, and cites evidence.

Three clauses, checked separately so the reason says which one broke:
the record exists at all, it selects exactly one philosophy from the
list in GD-UIUX-001, and it cites at least one evidence id that
resolves in `registry/evidence.json`.

The record is read through a labelled field rather than through prose.
A document that discusses eight philosophies has not chosen one, and
the drill's third logged failure is an agent that asks instead of
choosing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PHILOSOPHIES, UNSETTLED, emit,  # noqa: E402
                     evidence_ids, ledger_ids, philosophies_in, read, rel,
                     records, scratch_dir, text_files)

CID = "c1"


def main():
    scratch = scratch_dir()
    known = ledger_ids()
    if known is None:
        emit(CID, UNSETTLED,
             "the estate evidence ledger could not be read, so an evidence "
             "id cannot be resolved. That is a gap in the environment, not "
             "a finding against the delivered tree.")

    found = records(scratch)
    if not found:
        mentions = [rel(scratch, p) for p in text_files(scratch)
                    if "philosoph" in read(p).lower()]
        if mentions:
            emit(CID, FAIL,
                 "%s mention a philosophy but none carries a labelled field "
                 "naming the one chosen, so no record was recognised"
                 % ", ".join(mentions[:4]))
        emit(CID, FAIL,
             "no philosophy record in the delivered tree: no file carries a "
             "labelled field naming one of the philosophies in "
             "packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md")

    best = None
    for path, text, chosen, _ in found:
        where = rel(scratch, path)
        letters = set()
        for _, value in chosen:
            letters |= philosophies_in(value)
        if not letters:
            best = best or (where, "the philosophy field names nothing from "
                                   "the list: %r" % chosen[0][1][:80])
            continue
        if len(letters) > 1:
            best = best or (
                where,
                "the record names %d philosophies as chosen (%s); the "
                "criterion asks for exactly one"
                % (len(letters), ", ".join("%s %s" % (l, PHILOSOPHIES[l][0])
                                           for l in sorted(letters))))
            continue
        cited = evidence_ids(text)
        if not cited:
            best = best or (where, "names %s but cites no evidence id"
                            % PHILOSOPHIES[sorted(letters)[0]][0])
            continue
        resolved = [i for i in cited if i in known]
        if not resolved:
            best = best or (where, "cites %s, and none of those resolve in "
                            "registry/evidence.json" % ", ".join(cited))
            continue
        letter = sorted(letters)[0]
        emit(CID, PASS,
             "%s names one philosophy, %s %s, and cites %s, which resolves "
             "in the ledger"
             % (where, letter, PHILOSOPHIES[letter][0],
                ", ".join(resolved[:4])))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
