#!/usr/bin/env python3
"""Criterion 7: the answer carries an SRM check with a computed p-value.

Three things, and all three: the check is named, a p-value is given as a
number rather than gestured at, and the check is reported as failing.
The fixture assigns 52.6/47.4 against a declared 50/50 across 40,000
users, so the honest p-value is around 2.5e-25 and any correct answer
reports a number far below any threshold anyone would pick.

The number has to sit near the SRM mention. A p-value somewhere else in
a document, about the conversion lift, is not this check.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, answer_files, emit, flatten, scratch_dir  # noqa: E402

CID = "c7"

SRM = re.compile(r"(?i)sample\s+ratio\s+mismatch|\bSRM\b")
WINDOW = 400

# p = 1.2e-9, p-value of 0.0001, p < 0.001, p-value: 2.5e-25
PVALUE = re.compile(
    r"(?i)\bp[\s-]*(?:value)?\s*(?:of|is|=|==|<|≈|~|:)\s*"
    r"(\d*\.?\d+(?:[eE][-+]?\d+)?)")
FAILING = re.compile(
    r"(?i)\bfail(?:s|ed|ing|ure)?\b|\breject(?:s|ed|ing)?\b|"
    r"\bmismatch(?:ed)?\b|\bimbalanc\w*|\bnot\s+50[/ -]?50\b|"
    r"\bflag(?:s|ged)?\b|\btripp?(?:s|ed)\b|\bviolat\w+")


def main():
    scratch = scratch_dir()
    answers = answer_files(scratch)
    if not answers:
        emit(CID, FAIL,
             "the delivery wrote no answer: no Markdown or text file in the "
             "tree differs from the scenario's own copy")

    named, numbered = [], []
    for relative, text in answers:
        flat = flatten(text)
        for hit in SRM.finditer(flat):
            named.append(relative)
            start = max(0, hit.start() - WINDOW)
            window = flat[start:hit.end() + WINDOW]
            values = []
            for match in PVALUE.finditer(window):
                try:
                    values.append((float(match.group(1)), match.group(0)))
                except ValueError:
                    continue
            if not values:
                continue
            numbered.append(relative)
            smallest = min(values)
            if smallest[0] >= 0.05:
                continue
            if not FAILING.search(window):
                continue
            emit(CID, PASS,
                 "%s runs the sample ratio mismatch check, reports %s and "
                 "calls it failed" % (relative, " ".join(smallest[1].split())))

    if numbered:
        emit(CID, FAIL,
             "%s names the sample ratio mismatch check and gives a p-value, "
             "but does not report the check as failing, or the value it "
             "gives is not below 0.05" % numbered[0])
    if named:
        emit(CID, FAIL,
             "%s mentions the sample ratio mismatch check but computes no "
             "p-value for it; naming the check is not running it" % named[0])
    emit(CID, FAIL,
         "no delivered answer mentions a sample ratio mismatch check "
         "(looked in %s)" % ", ".join(r for r, _ in answers[:5]))


if __name__ == "__main__":
    main()
