#!/usr/bin/env python3
"""Criterion 5: each claimed value cites a ticket, or says unevidenced.

The same claim set criterion 4 reads. The frozen spec names "claims
present, ticket ids absent, 5 fails while 4 passes" as a failure worth
logging on its own, which only means anything if both criteria run over
one set of claims.

The escape hatch is in the criterion and is honoured: a claim marked
unevidenced, with that word, passes. What does not pass is a ticket id
that no ticket carries. An invented citation is worse than none, so it
is reported as its own failure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, ID_RE, PASS, claim_items, emit,  # noqa: E402
                     one_line, scratch_dir, the_doc, ticket_ids)

CID = "c5"

MINIMUM = 2
UNEVIDENCED = "unevidenced"


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)
    known = ticket_ids(scratch)
    if not known:
        emit(CID, FAIL,
             "no tickets found under support/tickets, so no claim could be "
             "tied to one; the fixture was not delivered intact")

    best = None
    for where, text in docs:
        items = claim_items(text)
        if len(items) < MINIMUM:
            best = best or (
                where,
                "only %d claim(s) found, so there is nothing to evidence. "
                "Claims are read as bullets, numbered items or table rows, "
                "so a document that makes them in flowing prose has none "
                "this grader can count. Read the document before treating "
                "this as a finding" % len(items))
            continue
        invented, bare, cited = [], [], set()
        for item in items:
            ids = set(ID_RE.findall(item))
            good = ids & known
            bad = ids - known
            if bad and not good:
                invented.append((item, sorted(bad)))
                continue
            if good:
                cited |= good
                continue
            if UNEVIDENCED in item.lower():
                continue
            bare.append(item)
        if invented:
            item, bad = invented[0]
            best = best or (
                where,
                "a claim cites %s, which is not a ticket in this repository. "
                "The eleven are %s. Claim: %r"
                % (", ".join(bad), ", ".join(sorted(known)),
                   one_line(item, 110)))
            continue
        if bare:
            best = best or (
                where,
                "%d of %d claims carry neither a ticket id nor the word "
                "unevidenced. First: %r"
                % (len(bare), len(items), one_line(bare[0], 130)))
            continue
        emit(CID, PASS,
             "%s: all %d claims are evidenced or marked unevidenced, citing "
             "%d of the %d tickets (%s)"
             % (where, len(items), len(cited), len(known),
                ", ".join(sorted(cited)) or "none, all marked unevidenced"))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
