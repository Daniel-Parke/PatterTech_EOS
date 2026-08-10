#!/usr/bin/env python3
"""Criterion 2: the same record treats the unlicensed copy as a refusal.

The vendored directory has no licence file and no headers. The failure
this catches is the one that reads as diligence: recording it as an
unknown to resolve later. Absence of a licence is not a blank, it is a
refusal, so the record has to say so in words a check can find.

The record that satisfied criterion 1 is looked at first, so "that same
artefact" means what it says on a tree that files more than one.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (COPYLEFT_ID, FAIL, PASS, VENDORED_PATH,  # noqa: E402
                     decision_records, emit, flat, scratch_dir)

CID = "c2"

REFUSALS = ("no licence", "no license", "unlicensed", "exclusive copyright")


def path_named(body):
    return VENDORED_PATH in body or VENDORED_PATH.replace("/", "\\") in body


def main():
    scratch = scratch_dir()
    records = decision_records(scratch)
    if not records:
        emit(CID, FAIL,
             "no decision record in the tree, so the vendored directory is "
             "recorded nowhere; criterion 1 covers the missing record")

    # The criterion-1 artefact first, then the rest.
    records.sort(key=lambda item: COPYLEFT_ID.lower() not in flat(item[1]))

    near = []
    for name, text in records:
        body = flat(text)
        named = path_named(body)
        refusal = next((r for r in REFUSALS if r in body), None)
        if named and refusal:
            emit(CID, PASS,
                 "%s names %s and calls it %r rather than an unknown to fill "
                 "in later" % (name, VENDORED_PATH, refusal))
        if named:
            near.append("%s names %s but says none of %s, so absence of a "
                        "licence is being carried as a gap rather than as a "
                        "refusal" % (name, VENDORED_PATH,
                                     ", ".join(repr(r) for r in REFUSALS)))
        else:
            near.append("%s never names %s" % (name, VENDORED_PATH))

    emit(CID, FAIL, "; ".join(near[:3]))


if __name__ == "__main__":
    main()
