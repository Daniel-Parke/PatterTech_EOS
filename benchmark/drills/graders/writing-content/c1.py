#!/usr/bin/env python3
"""Criterion 1: no lookup-then-concatenate, and one id carries the count.

Two assertions over the delivered source.

The first is the spec's own wording: no source line matches a
translation lookup followed by string concatenation. A `+` on either
side of a `t(...)` call counts, and so does a template literal that
interpolates a lookup alongside anything else, because that is the same
sentence assembled from parts under a different syntax.

The second is that the item count resolves through a single message id
whose message selects the plural form inside itself, rather than
through two ids picked by a comparison in the component. A ternary that
chooses between two lookups fails even when nothing is concatenated,
because the grammar decision has still been made in English.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, app_files, base_catalogue, emit,  # noqa: E402
                     line_of, plural_messages, read, rel, scratch_dir,
                     strip_comments, t_calls)

CID = "c1"

TERNARY = re.compile(
    r"\?[^;{}]{0,160}?(?<![\w.$])t\s*\([^()]*\)[^;{}]{0,160}?:"
    r"[^;{}]{0,160}?(?<![\w.$])t\s*\(")
COUNT_BRANCH = re.compile(r"[=!<>]==?\s*1\s*\)?\s*\?")


def concatenations(text):
    """Every lookup with a `+` on one side of it, as (line, snippet)."""
    hits = []
    for start, end, _, _ in t_calls(text):
        before = text[:start].rstrip()
        after = text[end:].lstrip()
        if before.endswith("+") or after.startswith("+"):
            hits.append((line_of(text, start),
                         " ".join(text[start:end + 12].split())))
    for match in re.finditer(r"`(?:\\.|[^`\\])*`", text, re.S):
        body = match.group(0)
        if not re.search(r"\$\{[^{}]*(?<![\w.$])t\s*\(", body):
            continue
        literal = re.sub(r"\$\{[^{}]*\}", "", body).strip("`").strip()
        if body.count("${") > 1 or literal:
            hits.append((line_of(text, match.start()),
                         " ".join(body.split())[:70]))
    return hits


def main():
    scratch = scratch_dir()
    files = app_files(scratch)
    if not files:
        emit(CID, FAIL, "no application source found to read")

    offences = []
    branches = []
    for path in files:
        text = strip_comments(read(path))
        name = rel(scratch, path)
        for line, snippet in concatenations(text):
            offences.append("%s:%d %s" % (name, line, snippet))
        flat = re.sub(r"\s+", " ", text)
        for match in TERNARY.finditer(flat):
            branches.append("%s picks between two lookups: %s"
                            % (name, match.group(0)[:70]))
        for match in COUNT_BRANCH.finditer(flat):
            branches.append("%s branches on a count of one: %s"
                            % (name, match.group(0)[:40]))

    if offences:
        emit(CID, FAIL,
             "%d translation lookup(s) are concatenated: %s"
             % (len(offences), "; ".join(offences[:4])))

    code, path, flat = base_catalogue(scratch)
    if flat is None:
        emit(CID, FAIL, "no message catalogue found, so no message id "
                        "carries anything")

    plurals = plural_messages(flat)
    if not plurals:
        emit(CID, FAIL,
             "no message in %s selects a plural form inside itself; the "
             "count still needs a decision outside the catalogue"
             % rel(scratch, path))

    used = set()
    for f in files:
        text = strip_comments(read(f))
        for _, _, _, key in t_calls(text):
            if key:
                used.add(key)
    live = sorted(k for k in plurals if k in used)
    if not live:
        emit(CID, FAIL,
             "%s declares plural selection on %s but no source file looks "
             "the message up, so nothing renders through it"
             % (rel(scratch, path), ", ".join(sorted(plurals))))

    if branches:
        emit(CID, FAIL,
             "%d place(s) still decide the form in the component: %s"
             % (len(branches), "; ".join(branches[:3])))

    emit(CID, PASS,
         "no lookup is concatenated in %d source file(s), and %s carries the "
         "count in one message with categories %s"
         % (len(files), live[0],
            ", ".join(sorted(plurals[live[0]]))))


if __name__ == "__main__":
    main()
