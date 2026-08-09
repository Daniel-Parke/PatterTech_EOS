#!/usr/bin/env python3
"""Criterion 7: who buys, who uses, and whether they are the same person.

Three separate things, and the third is the one that carries meaning in
this market: the practice owner who signs and the receptionist who
lives in the diary are often, but not always, one person. The document
has to say which.

A role has to be named. "The buyer is our customer" names nobody, so a
role word from the market is required in the same sentence as the
buying or the using.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, one_line, scratch_dir,  # noqa: E402
                     sentences, the_doc)

CID = "c7"

BUYER = re.compile(
    r"\bbuyer\b|\bbuys?\b|\bbought\b|\bpurchas\w*\b|\bpays?\b|\bpaying\b|"
    r"\bsigns? (?:the|off|up)\b|\bdecision[- ]maker\b|\bwho holds the "
    r"budget\b|\bbudget holder\b|\beconomic buyer\b", re.I)

USER = re.compile(
    r"\buser\b|\busers\b|\buses?\b|\busing\b|\bday[- ]to[- ]day\b|"
    r"\bin (?:it|the diary) all day\b|\boperator\b|\bwho works in it\b|"
    r"\bwho lives in it\b|\bend user\b", re.I)

ROLE = re.compile(
    r"\bpractice owner\b|\bowner\b|\bprincipal\b|\bpartner\b|"
    r"\bpractice manager\b|\bmanager\b|\breceptionist\b|\bfront desk\b|"
    r"\badministrator\b|\badmin\b|\bphysiotherapist\b|\bphysio\b|"
    r"\bpractitioner\b|\bclinician\b|\bsole trader\b|\boperations "
    r"director\b|\bbookkeeper\b|\blocum\b", re.I)

# The sameness statement has to be a statement. A heading reading
# "Buyer and user" is a label, and an earlier draft of this grader
# accepted one, which would have passed a document that never answers
# the question.
SAME = re.compile(
    r"\b(?:the )?same person\b|\bthe same individual\b|\bone and the same\b|"
    r"\bboth roles\b|\bwears? both\b|\bdifferent people\b|"
    r"\bseparate people\b|\btwo (?:different )?people\b|"
    r"\bdistinct people\b|\bare (?:not )?the same\b|"
    r"\bbuyer and (?:the )?user are\b|\buser and (?:the )?buyer are\b", re.I)


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)

    best = None
    for where, text in docs:
        lines = sentences(text)
        buyer = next((s for s in lines
                      if BUYER.search(s) and ROLE.search(s)), None)
        user = next((s for s in lines
                     if USER.search(s) and ROLE.search(s)), None)
        same = next((s for s in lines if SAME.search(s)), None)
        missing = []
        if buyer is None:
            missing.append("no named role is said to buy or pay")
        if user is None:
            missing.append("no named role is said to use it day to day")
        if same is None:
            missing.append("no statement of whether buyer and user are the "
                           "same person")
        if missing:
            best = best or (where, "; ".join(missing))
            continue
        emit(CID, PASS,
             "%s names the buyer (%r), the user (%r) and settles whether "
             "they are one person (%r)"
             % (where, one_line(buyer, 90), one_line(user, 90),
                one_line(same, 90)))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
