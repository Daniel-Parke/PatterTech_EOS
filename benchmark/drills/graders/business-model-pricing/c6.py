#!/usr/bin/env python3
"""Criterion 6: every metric named in the decision is defined, with a formula.

The name diff is what decides this. A definitions file that defines
twelve metrics the decision never mentions is fine; a decision naming
one metric the file does not define is not.

Definitions are read out of a Markdown table of the shape the pack's own
definitions reference uses, and out of headed sections with a formula
line under them, because both are ordinary ways to write the same file.
A definition whose formula cell is empty, a dash or a placeholder does
not count: the criterion says with a formula.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISION, DEFINITIONS, FAIL, PASS,  # noqa: E402
                     decision_doc, emit, read, scratch_dir)

CID = "c6"

ROW = re.compile(r"^\s*\|(?P<cells>.+)\|\s*$", re.M)
SEPARATOR = re.compile(r"^[\s|:-]+$")
HEADING = re.compile(r"^#{2,6}\s+(?P<name>.+?)\s*$", re.M)
FORMULA_LINE = re.compile(
    r"^\s*(?:\*\*)?formula(?:\*\*)?\s*[:=]\s*(?P<body>.+?)\s*$",
    re.I | re.M)

PLACEHOLDER = {"", "-", "--", "n/a", "na", "tbd", "tbc", "todo", "?",
               "see above", "as above", "same"}
MIN_FORMULA = 8

# Words that carry no distinguishing weight when two metric names are
# compared, so "average revenue per account" still matches a definition
# written as "Average revenue per account (ARPA)".
NOISE = re.compile(r"[^a-z0-9 ]+")


def normalise(name):
    return re.sub(r"\s+", " ", NOISE.sub(" ", str(name).lower())).strip()


def formula_ok(text):
    body = re.sub(r"\s+", " ", str(text)).strip()
    return body.lower() not in PLACEHOLDER and len(body) >= MIN_FORMULA


def definitions(text):
    """{normalised name: formula} from tables and from headed sections."""
    found = {}

    for match in ROW.finditer(text):
        raw = match.group("cells")
        if SEPARATOR.match(raw):
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 2:
            continue
        name, formula = cells[0], cells[1]
        if not name or normalise(name) in ("metric", "name", "term"):
            continue
        if formula_ok(formula):
            found.setdefault(normalise(name), formula)

    for match in HEADING.finditer(text):
        name = match.group("name")
        tail = text[match.end():]
        stop = HEADING.search(tail)
        section = tail[:stop.start()] if stop else tail
        line = FORMULA_LINE.search(section)
        if line and formula_ok(line.group("body")):
            found.setdefault(normalise(name), line.group("body").strip())
        else:
            equation = next((ln for ln in section.splitlines()
                             if "=" in ln and formula_ok(ln)), None)
            if equation:
                found.setdefault(normalise(name), equation.strip())

    return found


def resolves(metric, defined):
    """A metric name against the defined names, tightest match first."""
    key = normalise(metric)
    if not key:
        return None
    if key in defined:
        return key
    for name in defined:
        if re.search(r"\b%s\b" % re.escape(key), name):
            return name
    return None


def main():
    scratch = scratch_dir()
    doc = decision_doc(CID, scratch)

    metrics = doc.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        emit(CID, FAIL,
             "%s names no metrics, so there is no name diff to close and "
             "nothing was reported with a definition" % DECISION)

    path = scratch / DEFINITIONS
    if not path.is_file():
        emit(CID, FAIL,
             "%s names %d metric(s) and there is no %s"
             % (DECISION, len(metrics), DEFINITIONS))

    defined = definitions(read(path))
    if not defined:
        emit(CID, FAIL,
             "%s carries no definition with a formula that this grader can "
             "read; a Markdown table of metric and formula, or a heading per "
             "metric with a formula line under it, are both read"
             % DEFINITIONS)

    undefined = [m for m in metrics if resolves(m, defined) is None]
    if undefined:
        emit(CID, FAIL,
             "the name diff is not empty: %s named in %s with no definition "
             "carrying a formula in %s (%d metric(s) defined there)"
             % (", ".join(repr(str(m)) for m in undefined[:6]), DECISION,
                DEFINITIONS, len(defined)))

    emit(CID, PASS,
         "all %d metric(s) named in %s resolve to a definition with a "
         "formula in %s" % (len(metrics), DECISION, DEFINITIONS))


if __name__ == "__main__":
    main()
