#!/usr/bin/env python3
"""Criterion 8: a pricing statement that the pricing page agrees with.

Full semantic agreement between two documents is not decidable, and
this grader does not pretend otherwise. It settles the three
contradictions that are decidable and that actually happen:

- a money figure the pricing page does not carry, which is what an
  agent writing from its prior invents;
- a free plan claimed against a page that says there is not one;
- per-practitioner or per-seat pricing claimed against a page that
  prices per practice.

A document that states a price the page also states, and contradicts
none of the three, passes. A subtler disagreement, say about what a
plan includes, would pass here and needs a person. That limit is worth
knowing when reading the verdict.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, money_figures, one_line,  # noqa: E402
                     pricing_page, scratch_dir, sentences, the_doc,
                     visible_text)

CID = "c8"

FREE_PLAN = re.compile(
    r"\bfree (?:plan|tier|forever|for ever|version|for good|account)\b|"
    r"\bfreemium\b|\bfree to use\b|\bfree for ever\b", re.I)
NO_FREE_PLAN = re.compile(r"\bno free (?:plan|tier|version)\b", re.I)

PER_SEAT = re.compile(
    r"\bper[- ](?:practitioner|seat|user|clinician|head|physio)\b|"
    r"\bfor each practitioner\b|\bper person\b", re.I)
PER_PRACTICE = re.compile(
    r"\bper practice\b|\bper[- ]practice\b|\bnot per practitioner\b", re.I)

MODEL_CUE = re.compile(
    r"\bprice|\bpricing\b|\bcosts?\b|\bcharge[sd]?\b|\ba month\b|"
    r"\bper month\b|\bmonthly\b|\bplan\b|\bsubscription\b", re.I)


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)
    where_page, page = pricing_page(scratch)
    if where_page is None:
        emit(CID, FAIL,
             "no pricing page in the tree, so nothing could be checked "
             "against it; the fixture ships one at web/pricing.html")

    page_figures = money_figures(page)
    page_says_no_free = bool(NO_FREE_PLAN.search(page))
    page_per_practice = bool(PER_PRACTICE.search(page))

    best = None
    for where, text in docs:
        body = visible_text(text)
        figures = money_figures(body)
        wrong = sorted(figures - page_figures, key=lambda v: float(v))

        if wrong:
            best = best or (
                where,
                "states %s, which %s does not carry. The page prices are %s"
                % (", ".join("£" + w for w in wrong), where_page,
                   ", ".join("£" + f for f in sorted(page_figures,
                                                     key=lambda v: float(v)))))
            continue

        if page_says_no_free:
            claim = next((s for s in sentences(text) if FREE_PLAN.search(s)
                          and not re.search(r"free trial", s, re.I)), None)
            if claim:
                best = best or (
                    where,
                    "claims a free plan while %s says there is none: %r"
                    % (where_page, one_line(claim, 130)))
                continue

        if page_per_practice:
            claim = next((s for s in sentences(text) if PER_SEAT.search(s)
                          and not re.search(r"not per|rather than per",
                                            s, re.I)), None)
            if claim:
                best = best or (
                    where,
                    "prices per practitioner or per seat while %s prices per "
                    "practice: %r" % (where_page, one_line(claim, 130)))
                continue

        if figures:
            emit(CID, PASS,
                 "%s states %s, all of which %s carries"
                 % (where, ", ".join("£" + f for f in
                                     sorted(figures, key=lambda v: float(v))),
                    where_page))

        model = next((s for s in sentences(text)
                      if PER_PRACTICE.search(s) and MODEL_CUE.search(s)), None)
        if model and page_per_practice:
            emit(CID, PASS,
                 "%s states the pricing model rather than a figure, and it "
                 "matches %s: %r" % (where, where_page, one_line(model, 130)))

        best = best or (
            where,
            "no pricing statement: the document names no price and no "
            "pricing model, so there is nothing for %s to agree with"
            % where_page)

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
