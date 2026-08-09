#!/usr/bin/env python3
"""Criterion 7: the report carries an abstain rate beside the accuracy.

Beside, because an accuracy computed over the tickets the classifier
chose to answer means nothing without the share it declined: a model
that abstains on nine tickets in ten can post any accuracy it likes.
Sitting in the same object is preferred and reported; nesting the two
under different keys is a layout choice, not a missing number, so it
passes with the location stated.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_keys,  # noqa: E402
                     is_abstain_rate_key, is_accuracy_key, numeric,
                     require_report, scratch_dir, walk_json)

CID = "c7"


def parent(path):
    return path.rsplit(".", 1)[0] if "." in path else path


def main():
    scratch = scratch_dir()
    run = require_report(CID, scratch)
    report = run.report

    accuracy = find_keys(report, is_accuracy_key)
    if not accuracy:
        emit(CID, FAIL,
             "%s reports no accuracy, so there is nothing for an abstain "
             "rate to sit beside" % run.rel)

    rates = [(p, k, v) for p, k, v in find_keys(report, is_abstain_rate_key)
             if numeric(v) is not None]
    if not rates:
        loose = [k for _, k, _ in walk_json(report)
                 if "abstain" in str(k).lower()]
        if loose:
            emit(CID, FAIL,
                 "%s mentions abstention (%s) but reports no rate, so the "
                 "share of tickets declined cannot be read off the output"
                 % (run.rel, ", ".join(sorted(set(map(str, loose)))[:4])))
        emit(CID, FAIL,
             "%s reports an accuracy and no abstain rate, so the accuracy "
             "does not say what it was computed over" % run.rel)

    value = numeric(rates[0][2])
    if not 0.0 <= value <= 100.0:
        emit(CID, FAIL,
             "%s is %r, which is not a rate" % (rates[0][0], rates[0][2]))

    beside = [r for r in rates
              if any(parent(r[0]) == parent(a[0]) for a in accuracy)]
    where = ("in the same object as %s" % accuracy[0][0] if beside
             else "at %s, alongside %s rather than in the same object"
                  % (rates[0][0], accuracy[0][0]))
    emit(CID, PASS,
         "%s reports %s=%s %s" % (run.rel, rates[0][1], rates[0][2], where))


if __name__ == "__main__":
    main()
