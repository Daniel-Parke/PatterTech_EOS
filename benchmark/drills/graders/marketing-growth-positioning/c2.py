#!/usr/bin/env python3
"""Criterion 2: the competitive alternative is named, as a named thing.

Two tests. The document has to name something concrete in a sentence
about what the buyer would use instead: a proper noun, or an artefact
like a spreadsheet or a paper diary. "Other scheduling tools" is a
category and matches nothing here, which is the point.

Then, because this repository's real alternative is the manual one, the
document also has to name it. The tickets say so in the buyer's own
words more than once, so a position that competes only with software
has not read the tree it was given.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, one_line, scratch_dir,  # noqa: E402
                     sentences, the_doc)

CID = "c2"

# The sentence has to be about what a buyer uses instead of us.
CONTEXT = re.compile(
    r"\balternativ|\binstead\b|\bincumbent|\bcompet|\bswitch|\bmove[ds]? "
    r"from\b|\bcame from\b|\bcurrently us|\btoday they us|\bwhat they use\b|"
    r"\bbefore us\b|\bstatus quo\b|\bdo nothing\b|\bdoing nothing\b|"
    r"\breplac|\bup against\b|\bthey would use\b|\bwould otherwise\b", re.I)

# The manual alternative, in the shapes the tickets use.
MANUAL = re.compile(
    r"\bspreadsheet\b|\bexcel\b|\bgoogle sheets\b|\bpaper diary\b|"
    r"\bpaper day ?book\b|\bday ?book\b|\bpaper appointment book\b|"
    r"\bnotebook\b|\bpen and paper\b|\bwall planner\b|\bappointment book\b|"
    r"\bdo nothing\b|\bdoing nothing\b|\bstatus quo\b", re.I)

# Words that look like proper nouns but name nobody.
NOT_A_NAME = {
    "we", "our", "ours", "the", "this", "that", "they", "their", "it",
    "a", "an", "and", "but", "if", "when", "who", "what", "why", "how",
    "most", "many", "some", "every", "each", "no", "not", "there", "these",
    "those", "for", "from", "in", "on", "at", "by", "with", "without",
    "practice", "practices", "practitioner", "practitioners", "clinic",
    "clinics", "physio", "physiotherapy", "physiotherapist", "patient",
    "patients", "buyer", "user", "owner", "manager", "receptionist",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "positioning", "position", "alternative", "alternatives", "evidence",
    "criterion", "note", "notes", "scheduling", "software", "tool",
    "tools", "product", "uk", "vat", "csv", "sms", "solo", "clinic",
}

PROPER = re.compile(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\b")


def product_name(scratch):
    readme = scratch / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8",
                                     errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip().lower()
    return ""


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)
    ours = product_name(scratch)

    best = None
    for where, text in docs:
        spans = [s for s in sentences(text) if CONTEXT.search(s)]
        if not spans:
            best = best or (
                where,
                "no sentence about what the buyer would use instead: nothing "
                "mentions an alternative, an incumbent, switching or the "
                "status quo")
            continue

        manual = None
        named = None
        for span in spans:
            hit = MANUAL.search(span)
            if hit and manual is None:
                manual = (hit.group(0), span)
            for match in PROPER.finditer(span):
                # The word that opens a sentence is capitalised because
                # it opens a sentence. Taking it for a product name was
                # an earlier version of this grader calling "Almost" a
                # competitor.
                if match.start() == 0:
                    continue
                candidate = match.group(1)
                low = candidate.lower()
                if low in NOT_A_NAME or low == ours:
                    continue
                if any(w in NOT_A_NAME for w in low.split()):
                    continue
                if named is None:
                    named = (candidate, span)
        if manual is None and named is None:
            best = best or (
                where,
                "the alternative is described but never named: %r names no "
                "product and no artefact, only a category"
                % one_line(spans[0], 140))
            continue
        if manual is None:
            best = best or (
                where,
                "names %r as the alternative but never the manual one, and "
                "the tickets say the spreadsheet and the paper day book are "
                "what these practices actually left behind"
                % named[0])
            continue
        found = "%s (%r)" % (manual[0], one_line(manual[1], 110))
        if named is not None:
            found = "%s, and %s" % (named[0], found)
        emit(CID, PASS, "%s names the alternative: %s" % (where, found))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
