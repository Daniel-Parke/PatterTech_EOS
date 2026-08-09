#!/usr/bin/env python3
"""Criterion 6: the severity policy, as far as a script can settle it.

The criterion has three clauses:

1. three or more ordered bands, each with a written impact criterion
2. the take-the-higher rule is stated
3. one band changes the response mode, not only the wording

Clauses 1 and 2 are structural and are checked here. A tree that
breaks either fails, and that is a real finding: no policy at all, two
bands, bands with no impact written against them, or no rule for the
case where two bands could apply.

Clause 3 is not checkable. Deciding whether "wake the on-call engineer
and open a bridge" is a different response *mode* from "reply sooner"
is a reading of the prose, and a keyword list dressed up as a check
would return a verdict without doing the reading. So when the
structural clauses hold, this grader exits 2: the criterion is not
settled here and a human judges clause 3. The runner records that as
manual, which is never a pass and blocks a green drill, which is the
honest direction.

What the structural half accepts. A band is a table row, a heading with
prose under it, or a top-level list item, whichever shape the policy
uses. Order comes from a number in the label (SEV1, P2, "Level 3") or
from an ordered severity vocabulary, and the labels must run one way
through the document. The take-the-higher rule is looked for as a
sentence carrying both a comparative (higher, worse, more severe) and
the situation it applies to (doubt, two bands could apply, borderline).
A policy that states the rule in some way this misses would fail on a
rule it does state; the regex is written out below so that a human can
see what was accepted.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, UNSETTLED, emit, find_artefact,  # noqa: E402
                     read, rel, scratch_dir)

# There is no PASS in here on purpose: clause 3 is a human's call, so the
# best this grader returns is "structurally sound, not settled".
CID = "c6"

MIN_BANDS = 3
MIN_IMPACT = 20

SEVERITY_WORDS = [
    "catastrophic", "critical", "severe", "major", "high", "serious",
    "significant", "moderate", "medium", "degraded", "minor", "low",
    "routine", "trivial", "cosmetic", "negligible",
]

COMPARATIVE = re.compile(
    r"(?i)\b(higher|highest|worse|worst|more severe|most severe|more serious|"
    r"most serious|greater|upper|up a band|round up|escalat\w*)\b")
SITUATION = re.compile(
    r"(?i)\b(doubt|unsure|uncertain|ambiguous|borderline|between|either|"
    r"both|two bands|more than one|could apply|would apply|might apply|"
    r"applies|disagree|argue|tie|split|unclear|not sure|choose|choice|"
    r"pick|deciding|decide)\b")
SENTENCE = re.compile(r"(?<=[.!?])\s+|\n{2,}|\n\s*[-*+]\s+|\n\s*\d+[.)]\s+")

NUM = re.compile(r"(\d+)")


def sentences(text):
    flat = re.sub(r"[ \t]+", " ", text)
    return [re.sub(r"\s+", " ", p).strip()
            for p in SENTENCE.split(flat) if p and p.strip()]


def ordinal(label):
    match = NUM.search(label)
    if match:
        return int(match.group(1))
    lowered = label.lower()
    for i, word in enumerate(SEVERITY_WORDS):
        if re.search(r"\b%s\b" % word, lowered):
            return 100 + i
    return None


def bands_from_tables(text):
    """Rows of any Markdown table with three or more data rows."""
    rows, current = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            current.append(cells)
            continue
        if current:
            rows.append(current)
            current = []
    if current:
        rows.append(current)
    for table in rows:
        body = [r for r in table[1:]
                if not all(set(c) <= set("-: ") for c in r if c)]
        body = [r for r in body if any(c for c in r)]
        if len(body) >= MIN_BANDS:
            return [(r[0], " ".join(r[1:])) for r in body if r]
    return []


def bands_from_headings(text):
    lines = text.splitlines()
    marks = []
    for i, line in enumerate(lines):
        m = re.match(r"^\s{0,3}(#{2,6})\s+(.*?)\s*#*$", line)
        if m:
            marks.append((i, len(m.group(1)), m.group(2).strip()))
    out = []
    for j, (i, level, label) in enumerate(marks):
        end = len(lines)
        for k, level2, _ in marks[j + 1:]:
            if level2 <= level:
                end = k
                break
        body = " ".join(lines[i + 1:end]).strip()
        out.append((label, body))
    return out


def bands_from_list(text):
    out, label, body = [], None, []
    for line in text.splitlines():
        m = re.match(r"^\s{0,2}[-*+]\s+(.*)$", line)
        if m:
            if label is not None:
                out.append((label, " ".join(body).strip()))
            item = m.group(1).strip()
            split = re.split(r"\s+[-–—:]\s+|:\s+", item, maxsplit=1)
            label = split[0].strip(" *_`")
            body = [split[1]] if len(split) > 1 else []
            continue
        if label is not None and line.strip() and line.startswith((" ", "\t")):
            body.append(line.strip())
            continue
        if label is not None and not line.strip():
            out.append((label, " ".join(body).strip()))
            label, body = None, []
    if label is not None:
        out.append((label, " ".join(body).strip()))
    return out


def find_bands(text):
    for name, finder in (("table rows", bands_from_tables),
                         ("headings", bands_from_headings),
                         ("list items", bands_from_list)):
        found = [(lab, imp) for lab, imp in finder(text)
                 if lab and ordinal(lab) is not None]
        if len(found) >= MIN_BANDS:
            return name, found
    return None, []


def ordered(bands):
    marks = [ordinal(lab) for lab, _ in bands]
    if any(m is None for m in marks):
        return False
    ups = all(b > a for a, b in zip(marks, marks[1:]))
    downs = all(b < a for a, b in zip(marks, marks[1:]))
    return ups or downs


def main():
    scratch = scratch_dir()
    path = find_artefact(scratch, "severity_policy.md")
    if path is None:
        emit(CID, FAIL,
             "no severity_policy.md: the bands the rota has been meaning to "
             "write down for a year are still not written down")
    where = rel(scratch, path)
    text = read(path)
    if not text.strip():
        emit(CID, FAIL, "%s is empty" % where)

    shape, bands = find_bands(text)
    if len(bands) < MIN_BANDS:
        emit(CID, FAIL,
             "%s defines %d recognisable severity band(s), fewer than the "
             "three the criterion asks for (looked for table rows, headings "
             "and list items whose label carries a number or a severity "
             "word)" % (where, len(bands)))

    thin = [lab for lab, impact in bands if len(impact.strip()) < MIN_IMPACT]
    if thin:
        emit(CID, FAIL,
             "%s: band(s) %s carry no written impact criterion"
             % (where, ", ".join(thin[:4])))

    if not ordered(bands):
        emit(CID, FAIL,
             "%s: the bands %s do not run in one order through the document"
             % (where, ", ".join(lab for lab, _ in bands[:6])))

    higher = [s for s in sentences(text)
              if COMPARATIVE.search(s) and SITUATION.search(s)]
    if not higher:
        emit(CID, FAIL,
             "%s states no take-the-higher rule: no sentence says what to do "
             "when two bands could apply" % where)

    emit(CID, UNSETTLED,
         "%s defines %d ordered bands as %s, each with an impact criterion, "
         "and states the take-the-higher rule (%r). The third clause, that "
         "one band changes the response mode rather than only the wording, "
         "is a reading of the prose and is left for a human: this grader "
         "will not return a verdict it did not earn."
         % (where, len(bands), shape, higher[0][:120]))


if __name__ == "__main__":
    main()
