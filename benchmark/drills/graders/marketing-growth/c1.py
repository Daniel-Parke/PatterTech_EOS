#!/usr/bin/env python3
"""Criterion 1: no JSON-LD property describes text no reader can see.

The orphan half of this criterion is settled here. The other half names
Google's Rich Results validator, which is a hosted service with no
offline equivalent, so a clean tree is reported unsettled rather than
passed. A grader that quietly drops half a criterion is worse than one
that says which half it could not look at.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, UNSETTLED, emit, html_pages,  # noqa: E402
                     jsonld_blocks, read, scratch_dir, visible_text)

CID = "c1"

# Properties that carry machine vocabulary, an address or a timestamp
# rather than words a reader is shown.
TECHNICAL = {
    "@context", "@type", "@id", "@graph", "url", "sameas", "logo", "image",
    "contenturl", "thumbnailurl", "mainentityofpage", "identifier", "sku",
    "gtin", "gtin8", "gtin13", "gtin14", "mpn", "inlanguage", "pricecurrency",
    "currency", "applicationcategory", "applicationsubcategory",
    "operatingsystem", "availability", "itemcondition", "encodingformat",
    "potentialaction", "target", "urltemplate", "query-input", "datepublished",
    "datemodified", "uploaddate", "startdate", "enddate", "validfrom",
    "validthrough", "pricevaliduntil", "duration", "width", "height",
    "position", "bestrating", "worstrating", "email", "telephone",
}

# Numbers a reader is shown, so the figure must appear on the page.
NUMERIC = {"price", "ratingvalue", "ratingcount", "reviewcount",
           "lowprice", "highprice", "offercount"}

# A local structured-data validator, if the machine happens to carry one.
VALIDATORS = ("structured-data-testing-tool", "sdtt", "schemarama")

URLISH = re.compile(r"^(https?:|mailto:|tel:|/|\.\./|#)")
DATEISH = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]|$)")
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def flatten(text):
    text = text.replace(" ", " ")
    for bad, good in (("’", "'"), ("‘", "'"), ("“", '"'),
                      ("”", '"'), ("–", "-"), ("—", "-")):
        text = text.replace(bad, good)
    return re.sub(r"\s+", " ", text).strip().casefold()


def numbers(text):
    return {float(m) for m in NUMBER.findall(text.replace(",", ""))}


def leaves(node, key=None, where="$"):
    """Every (key, value, path) pair under a JSON-LD document."""
    if isinstance(node, dict):
        for name, value in node.items():
            yield from leaves(value, name, "%s.%s" % (where, name))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from leaves(value, key, "%s[%d]" % (where, i))
    elif key is not None:
        yield key, node, where


def orphans_on(page, text):
    """Properties on one page with no matching string in its own DOM."""
    docs, broken = jsonld_blocks(text)
    if broken:
        return None, docs
    shown = flatten(visible_text(text))
    figures = numbers(shown)
    found = []
    for doc in docs:
        for key, value, where in leaves(doc):
            name = str(key).strip().casefold()
            if name in TECHNICAL:
                continue
            if name in NUMERIC:
                try:
                    figure = float(str(value).replace(",", "").strip())
                except (TypeError, ValueError):
                    continue
                if figure not in figures:
                    found.append("%s = %s" % (where, value))
                continue
            if not isinstance(value, str):
                continue
            candidate = value.strip()
            if len(candidate) < 3 or URLISH.match(candidate):
                continue
            if DATEISH.match(candidate):
                continue
            if flatten(candidate) not in shown:
                found.append("%s = %r" % (where, candidate[:60]))
    return found, docs


def main():
    scratch = scratch_dir()
    pages = html_pages(scratch)
    if not pages:
        emit(CID, FAIL, "no pages under site/, so there is no rendered DOM "
                        "to check markup against")

    orphaned, marked = [], 0
    for page in pages:
        rel = page.relative_to(scratch).as_posix()
        found, docs = orphans_on(page, read(page))
        if found is None:
            emit(CID, FAIL, "%s carries a JSON-LD block that does not parse, "
                            "which no validator would accept either" % rel)
        if docs:
            marked += 1
        orphaned.extend("%s %s" % (rel, item) for item in found)

    if not marked:
        emit(CID, FAIL, "no page under site/ carries JSON-LD, so there is no "
                        "structured data to check")
    if orphaned:
        emit(CID, FAIL,
             "%d markup propert%s describe text no reader can see: %s"
             % (len(orphaned), "y" if len(orphaned) == 1 else "ies",
                "; ".join(orphaned[:6])))

    tool = next((t for t in VALIDATORS if shutil.which(t)), None)
    emit(CID, UNSETTLED,
         "zero orphan properties across %d page(s) with markup, which is the "
         "half of this criterion a script can settle. The other half names "
         "Google's Rich Results validator, a hosted service; no local "
         "structured-data validator is installed here (%s), so that half was "
         "not run and the criterion is unsettled rather than passed."
         % (marked, tool or "looked for " + ", ".join(VALIDATORS)))


if __name__ == "__main__":
    main()
