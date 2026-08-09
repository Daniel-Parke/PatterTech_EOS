#!/usr/bin/env python3
"""Criterion 2: the contract declares a rule on `order_total`.

Not-null or an accepted range; either satisfies the drill. The check is
structural first: find the node in the parsed contract that names the
column and look for a rule inside it. Only if no parsed contract names
the column at all does it fall back to reading the file, and it says so
in the reason when it does, because a text window is a weaker claim than
a node and a reader deserves to know which one they got.

Naming the column somewhere in a contract file is not the criterion. A
column listed with a type and no rule is a schema, and a schema that
admits nulls is what let the seeded batch through in the first place.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, RULE_TOKENS, contract_files, emit,  # noqa: E402
                     names_in, read, scratch_dir, subtree_text, walk_docs)

CID = "c2"
COLUMN = "order_total"


def rule_in(text):
    return next((t for t in RULE_TOKENS if t in text), None)


def main():
    scratch = scratch_dir()
    found, _ = contract_files(scratch)
    if not found:
        emit(CID, FAIL,
             "no contract or expectation file to inspect; criterion 1 covers "
             "that, and this one cannot run without it")

    named_but_unruled = []
    for relative, kind, doc in found:
        for node in walk_docs(doc):
            if COLUMN not in {n.lower() for n in names_in(node)}:
                continue
            token = rule_in(subtree_text(node))
            if token:
                emit(CID, PASS,
                     "%s (%s) declares %r on %s"
                     % (relative, kind, token, COLUMN))
            named_but_unruled.append(relative)

    # Fallback: the column is in the file but not under a node this
    # reader recognises as naming it.
    for relative, kind, _ in found:
        text = read(scratch / relative).lower()
        for match in re.finditer(re.escape(COLUMN), text):
            window = text[max(0, match.start() - 400):match.end() + 400]
            token = rule_in(window)
            if token:
                emit(CID, PASS,
                     "%s (%s) carries %r within 400 characters of %s; read "
                     "from the file text, not from a parsed node, so this is "
                     "a weaker reading than a structural one"
                     % (relative, kind, token, COLUMN))

    if named_but_unruled:
        emit(CID, FAIL,
             "%s names %s but declares no not-null or accepted-range rule on "
             "it; a type without a rule is a schema, not a contract"
             % (named_but_unruled[0], COLUMN))
    emit(CID, FAIL,
         "no contract file mentions %s at all (looked in %s)"
         % (COLUMN, ", ".join(r for r, _, _ in found[:4])))


if __name__ == "__main__":
    main()
