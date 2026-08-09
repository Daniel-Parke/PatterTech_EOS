#!/usr/bin/env python3
"""Criterion 5: the lifetime value did not come from blended churn.

Arithmetic, not judgement. Blended churn is computed from the scenario's
own cohort export by the house definition, accounts lapsing over
accounts exposed, pooled across the whole panel. The refused formula is
average revenue per account over that rate. If the reported figure lands
within one per cent of it, the reported figure came from it.

Nobody paid during the beta, so the panel carries no revenue and average
revenue per account has to be stood in for. The headline price is what
stands in, which is exactly the substitution the refused formula makes
when a venture reaches for it on its first pricing decision.

Known limit, stated rather than hidden: a lifetime value of zero clears
the band and passes. That is what the frozen criterion says, and the
honest reading of a zero with a method of not-computed is the answer the
pack allows a venture with too little data. It is a weak answer here,
with eighteen cohorts on disk, and no grader in this set catches it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (COHORTS, DECISION, FAIL, PASS, blended_churn,  # noqa: E402
                     decision_doc, emit, scratch_dir)

CID = "c5"

BAND = 0.01


def main():
    scratch = scratch_dir()
    doc = decision_doc(CID, scratch)

    ltv = doc.get("lifetime_value")
    if not isinstance(ltv, dict) or not isinstance(
            ltv.get("value"), (int, float)) or isinstance(
            ltv.get("value"), bool):
        emit(CID, FAIL,
             "%s carries no numeric lifetime_value.value, so there is "
             "nothing to compare against the refused formula" % DECISION)
    reported = float(ltv["value"])

    price = doc.get("headline_price")
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        emit(CID, FAIL,
             "%s carries no numeric headline_price, so average revenue per "
             "account cannot be stood up" % DECISION)

    churn = blended_churn(scratch)
    if churn is None:
        emit(CID, FAIL,
             "%s is missing or unreadable in the delivered tree, and the "
             "blended churn this criterion tests against is computed from "
             "it" % COHORTS)
    if churn <= 0:
        emit(CID, FAIL,
             "blended churn computed from %s is %s, so the refused formula "
             "has no value here" % (COHORTS, churn))

    naive = float(price) / churn
    gap = abs(reported - naive)
    if naive > 0 and gap <= BAND * naive:
        emit(CID, FAIL,
             "lifetime_value is %.2f and %.2f / %.4f is %.2f, a gap of "
             "%.2f per cent; the reported figure is the refused average "
             "revenue over blended churn formula, which is wrong in a "
             "knowable direction"
             % (reported, price, churn, naive, 100.0 * gap / naive))

    emit(CID, PASS,
         "lifetime_value is %.2f against a blended-churn figure of %.2f "
         "(%.2f / %.4f), %.1f per cent away, and carries method %r"
         % (reported, naive, price, churn, 100.0 * gap / naive,
            ltv.get("method")))


if __name__ == "__main__":
    main()
