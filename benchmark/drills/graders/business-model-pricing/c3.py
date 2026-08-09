#!/usr/bin/env python3
"""Criterion 3: the headline carries every unavoidable charge.

Two charges in this scenario cannot be declined, and the brief says so
in plain words: the card processing fee taken on every monthly payment,
and the one-off joining fee everyone pays first time. Both are added at
the checkout step in the tree as delivered, which is the drip pricing
pattern the ban exists for.

So "every unavoidable charge" is a closed set here, fixed by the
scenario, and the grader checks that set rather than judging honesty in
general. Whether a charge listed as optional really is declinable is
J-02 in the pack's own checks, needs a person, and is not attempted.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISION, FAIL, PASS, decision_doc, emit,  # noqa: E402
                     flatten, scratch_dir)

CID = "c3"

# (what it is, how it is named). The scenario's own words are in the
# first alternative of each; the rest are the ordinary synonyms.
UNAVOIDABLE = (
    ("the card processing fee",
     re.compile(r"process|card\s*fee|transaction\s*fee|payment\s*(?:fee|"
                r"provider|handling)|merchant\s*fee|stripe|gateway", re.I)),
    ("the joining fee",
     re.compile(r"join|sign[\s-]?up\s*fee|set[\s-]?up\s*fee|activation|"
                r"onboarding\s*fee|one[\s-]?off", re.I)),
)


def main():
    scratch = scratch_dir()
    doc = decision_doc(CID, scratch)

    includes = doc.get("headline_price_includes")
    if not isinstance(includes, list) or not includes:
        emit(CID, FAIL,
             "headline_price_includes is %s; the unavoidable set has to be "
             "in the advertised number, so it cannot be empty"
             % ("missing" if includes is None else repr(includes)[:80]))
    included_text = flatten(" ; ".join(str(item) for item in includes))

    charges = doc.get("optional_charges")
    if charges is None:
        charges = []
    if not isinstance(charges, list):
        emit(CID, FAIL, "optional_charges is not a list in %s" % DECISION)

    # A charge marked mandatory inside the optional list is the ban
    # failing at the schema level.
    mandatory = [str(c.get("name", "unnamed")) for c in charges
                 if isinstance(c, dict) and c.get("mandatory") is True]
    if mandatory:
        emit(CID, FAIL,
             "optional_charges marks %s as mandatory:true; an unavoidable "
             "charge in the optional list is the drip pricing pattern with "
             "a schema field on it" % ", ".join(mandatory))

    optional_text = flatten(" ; ".join(
        "%s %s" % (c.get("name", ""), c.get("avoidable_how", ""))
        for c in charges if isinstance(c, dict)))

    missing, smuggled = [], []
    for what, pattern in UNAVOIDABLE:
        if not pattern.search(included_text):
            missing.append(what)
        if pattern.search(optional_text):
            smuggled.append(what)

    if smuggled:
        emit(CID, FAIL,
             "%s appears in optional_charges; the brief says every buyer "
             "pays it, so it belongs inside the headline"
             % " and ".join(smuggled))
    if missing:
        emit(CID, FAIL,
             "headline_price_includes does not carry %s: %r"
             % (" or ".join(missing), included_text[:160]))

    emit(CID, PASS,
         "headline_price_includes carries the card processing fee and the "
         "joining fee, and no entry in optional_charges is mandatory "
         "(%d optional charge(s) checked)" % len(charges))


if __name__ == "__main__":
    main()
