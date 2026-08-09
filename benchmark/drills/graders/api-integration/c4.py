#!/usr/bin/env python3
"""Criterion 4: a required `currency` implies a version discriminator.

The criterion is an implication, and an implication is satisfied for
free by a document that never adds the required field. That reading
would score an untouched tree as a pass, so the antecedent is required
here too: the change request asked for a required currency field, and
this criterion is where the document is asked whether it added one and
told a caller which version it is talking to.

The discriminator is taken broadly, because more than one versioning
approach is defensible: a URL prefix, a version header or query
parameter, a versioned media type, a schema discriminator keyed on
version, or a pair of versioned schema names. The reason says which one
was found, and the weakest of them is named as such.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SPEC_REL, emit, load_spec,  # noqa: E402
                     required_lists, scratch_dir, version_signals)

CID = "c4"


def main():
    scratch = scratch_dir()
    doc = load_spec(CID, scratch)

    holders = []
    for owner, names in required_lists(doc):
        if any(str(n).strip().lower() == "currency" for n in names):
            holders.append(names)

    if not holders:
        emit(CID, FAIL,
             "no `required` list in %s contains `currency`: the change "
             "request asked for a currency field that must be supplied, and "
             "the document does not require one anywhere" % SPEC_REL)

    signals = version_signals(doc)
    if not signals:
        emit(CID, FAIL,
             "`currency` is required (in %d schema(s)) but %s carries no "
             "version discriminator: no URL version prefix, no version "
             "header or query parameter, no versioned media type, no schema "
             "discriminator and no versioned schema names. A caller sending "
             "yesterday's body gets a 4xx with nothing telling it why"
             % (len(holders), SPEC_REL))

    kind, detail = signals[0]
    weak = " (a schema name labels a shape rather than discriminating a " \
           "request, so this is the weakest form the criterion accepts)" \
           if kind == "versioned schema names" else ""
    emit(CID, PASS,
         "`currency` is required in %d schema(s) and the document carries a "
         "%s: %s%s" % (len(holders), kind, detail, weak))


if __name__ == "__main__":
    main()
