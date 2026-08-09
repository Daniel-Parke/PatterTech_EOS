#!/usr/bin/env python3
"""Criterion 6: classify can abstain, and does on an ambiguous ticket.

The eighteen tickets the two annotators read differently are frozen in
`_common.py` rather than read out of the tree, because the agent is
expected to split and reshape the sample and this criterion has to
survive that. The check is a direct call: the delivered `classify` is
handed those eighteen texts and at least one of them has to come back
with `abstain` true.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (AMBIGUOUS, FAIL, PASS, UNSETTLED,  # noqa: E402
                     call_classify, emit, scratch_dir)

CID = "c6"


def main():
    scratch = scratch_dir()
    outcome = call_classify(scratch, AMBIGUOUS)
    if outcome is None or (outcome.results is None and outcome.missing):
        emit(CID, UNSETTLED,
             "classify needs %r, which is not installed here, so it could "
             "not be called. That is a gap in this environment, not a "
             "finding against the delivered tree."
             % (outcome.missing if outcome else "a missing module"))
    if outcome.results is None:
        emit(CID, FAIL,
             "could not call classify: %s" % (outcome.error or "unknown"))

    shaped = [r for r in outcome.results if isinstance(r, dict)
              and "abstain" in r]
    errors = [r for r in outcome.results
              if isinstance(r, dict) and "error" in r]
    if errors:
        emit(CID, FAIL,
             "classify raised on %d of the %d ambiguous tickets: %s"
             % (len(errors), len(AMBIGUOUS), errors[0]["error"][:160]))
    if not shaped:
        emit(CID, FAIL,
             "classify returns no `abstain` key at all, so there is no way "
             "for it to decline a ticket")

    abstained = [r for r in shaped if r.get("abstain") is True]
    if not abstained:
        emit(CID, FAIL,
             "%s answers all %d of the ambiguous tickets and abstains on "
             "none of them; the labels it gave were %s"
             % (outcome.module, len(shaped),
                sorted({str(r.get("label")) for r in shaped})))

    emit(CID, PASS,
         "%s abstains on %d of the %d tickets the second annotator read "
         "differently" % (outcome.module, len(abstained), len(AMBIGUOUS)))


if __name__ == "__main__":
    main()
