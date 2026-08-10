#!/usr/bin/env python3
"""Criterion 4: retention is a curve, and the projection sorts.

One row per cohort age, no gaps and no repeats, and a projected
retention rate that does not fall as cohort age rises. The criterion
names what a failure looks like: a flat blended-churn projection. Flat
is non-decreasing on a strict reading, so the test is non-decreasing
across the projected ages and rising somewhere in them. A single average
churn applied forward produces a horizontal line and is refused.

The projected rows have to be marked as such. Observed retention rises
for the same sorting reason, so a file that does not say which rows are
model output cannot settle a criterion about the projection, and this
grader says that rather than checking the observed rows and calling it
the projection.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, RETENTION, emit, number,  # noqa: E402
                     rows_of, scratch_dir)

CID = "c4"

AGE_COLUMNS = ("cohort_age_months", "cohort_age", "age_months", "age")
RATE_COLUMNS = ("retention_rate", "retention", "period_retention",
                "retention_pct", "rate")
BASIS_COLUMNS = ("basis", "status", "source", "kind", "type", "observed")
PROJECTED = ("fitted", "projected", "projection", "modelled", "modeled",
             "model", "forecast", "predicted", "estimate", "estimated")
OBSERVED = ("observed", "actual", "measured", "historic", "historical")


def column(fieldnames, candidates):
    lowered = {(f or "").strip().lower(): f for f in fieldnames or []}
    for name in candidates:
        if name in lowered:
            return lowered[name]
    return None


def main():
    scratch = scratch_dir()
    path = scratch / RETENTION
    if not path.is_file():
        emit(CID, FAIL, "no %s in the delivered tree" % RETENTION)
    rows = rows_of(path)
    if not rows:
        emit(CID, FAIL, "%s is empty or will not parse as CSV" % RETENTION)

    fields = list(rows[0].keys())
    age_col = column(fields, AGE_COLUMNS)
    rate_col = column(fields, RATE_COLUMNS)
    basis_col = column(fields, BASIS_COLUMNS)
    if age_col is None or rate_col is None:
        emit(CID, FAIL,
             "%s has columns %s; a cohort age column and a retention rate "
             "column are both needed" % (RETENTION, ", ".join(fields)))

    ages = []
    for row in rows:
        age = number(row.get(age_col))
        if age is None or age != int(age):
            emit(CID, FAIL,
                 "%s has a non-integer cohort age %r"
                 % (RETENTION, row.get(age_col)))
        ages.append(int(age))

    if len(set(ages)) != len(ages):
        repeats = sorted({a for a in ages if ages.count(a) > 1})
        emit(CID, FAIL,
             "%s repeats cohort age(s) %s; the file is one row per cohort "
             "age" % (RETENTION, ", ".join(str(a) for a in repeats)))
    if sorted(ages) != list(range(min(ages), min(ages) + len(ages))):
        emit(CID, FAIL,
             "cohort ages in %s are not contiguous: %s"
             % (RETENTION, ", ".join(str(a) for a in sorted(ages))[:120]))
    if min(ages) > 1:
        emit(CID, FAIL,
             "%s starts at cohort age %d; the curve starts at the cohort's "
             "own age zero or one" % (RETENTION, min(ages)))

    if basis_col is None:
        emit(CID, FAIL,
             "%s has no column saying which rows are observed and which are "
             "projected (looked for %s), so a criterion about the projection "
             "cannot be settled from it"
             % (RETENTION, ", ".join(BASIS_COLUMNS)))

    projected = []
    observed_seen = False
    for age, row in sorted(zip(ages, rows), key=lambda pair: pair[0]):
        basis = str(row.get(basis_col, "")).strip().lower()
        rate = number(row.get(rate_col))
        if any(word in basis for word in OBSERVED):
            observed_seen = True
            continue
        if any(word in basis for word in PROJECTED) or basis in ("false",
                                                                 "no", "0"):
            if rate is None:
                emit(CID, FAIL,
                     "%s marks cohort age %d as projected with no retention "
                     "rate" % (RETENTION, age))
            projected.append((age, rate))

    if len(projected) < 2:
        emit(CID, FAIL,
             "%s carries %d projected row(s); with eighteen cohorts in the "
             "inputs the curve is expected to run past the observed window, "
             "and two projected ages are the minimum that can show a "
             "direction%s"
             % (RETENTION, len(projected),
                "" if observed_seen else
                ", and no row is marked observed either"))

    rates = [r for _, r in projected]
    for i in range(1, len(projected)):
        if rates[i] < rates[i - 1]:
            emit(CID, FAIL,
                 "projected retention falls from %s at cohort age %d to %s "
                 "at cohort age %d; the sorting effect makes the "
                 "period-over-period rate rise, so a falling projection is a "
                 "blended churn rate applied forward"
                 % (rates[i - 1], projected[i - 1][0], rates[i],
                    projected[i][0]))
    if rates[-1] <= rates[0]:
        emit(CID, FAIL,
             "projected retention is flat at %s across cohort ages %d to %d; "
             "a flat projection is one blended churn rate applied forward, "
             "which the sorting effect says is wrong in a knowable direction"
             % (rates[0], projected[0][0], projected[-1][0]))

    emit(CID, PASS,
         "%s runs one row per cohort age %d to %d, and projected retention "
         "rises from %s at age %d to %s at age %d"
         % (RETENTION, min(ages), max(ages), rates[0], projected[0][0],
            rates[-1], projected[-1][0]))


if __name__ == "__main__":
    main()
