#!/usr/bin/env python3
"""Criterion 5: the password error sits with the field and says what to do.

Four assertions, read off the markup and the catalogue rather than a
rendered page. The markup is where the relationship lives, so this one
loses nothing by being static.

- the password error is a sibling or descendant within the field, not a
  banner somewhere above the form. The test is that the element the
  input points at hangs below the input's own parent;
- the input is wired to it by `aria-describedby`, and the id that
  attribute names is an id something actually renders;
- the message states the requirement: a digit, or the word
  `characters`;
- the message is not `Invalid input`.

The message text is resolved through the catalogue, so a tree that
renders `{t("signup.passwordHint")}` is read by what the key holds. A
tree that hides the text behind indirection this grader cannot follow
fails with that said plainly, rather than passing on the benefit of the
doubt.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, base_catalogue, emit,  # noqa: E402
                     password_input, jsx_roots, rel, scratch_dir,
                     string_literals, t_calls)

CID = "c5"

BANNED = "invalid input"
REQUIREMENT = re.compile(r"\d|charact", re.I)


def ids_from(kind, value):
    if kind == "string":
        return [tok for tok in value.split() if tok]
    return [v for _, v in string_literals(value) if v.strip()]


def node_ids(node):
    kind, value = node.attrs.get("id", (None, ""))
    if kind is None:
        return []
    return ids_from(kind, value)


def message_of(node, flat):
    """The words a node renders, resolved through the catalogue."""
    parts = []
    for expr in node.exprs():
        for _, _, _, key in t_calls(expr):
            if key and key in flat:
                parts.append(flat[key])
    for child in node.elements():
        parts.extend(message_of(child, flat))
    parts.extend(t.strip() for t in node.texts() if t.strip())
    return [p for p in parts if p]


def main():
    scratch = scratch_dir()
    _, cat_path, flat = base_catalogue(scratch)
    if flat is None:
        emit(CID, FAIL, "no message catalogue found")

    roots = jsx_roots(scratch)
    field = password_input(scratch, roots)
    if field is None:
        emit(CID, FAIL, "no password input in the delivered markup")

    kind, value = field.attrs.get("aria-describedby",
                                  field.attrs.get("ariaDescribedBy",
                                                  (None, "")))
    if kind is None:
        emit(CID, FAIL,
             "%s carries no aria-describedby, so nothing connects the error "
             "to the field for anyone not looking at it" % field.where())
    wanted = ids_from(kind, value)
    if not wanted:
        emit(CID, FAIL,
             "%s sets aria-describedby to %r and no id can be read out of it"
             % (field.where(), value[:60]))

    described = []
    for _, root in roots:
        for node in root.elements():
            if set(node_ids(node)) & set(wanted):
                described.append(node)
    if not described:
        emit(CID, FAIL,
             "aria-describedby on %s names %s and nothing in the markup "
             "renders that id" % (field.where(), ", ".join(wanted)))

    parent = field.parent
    near = [n for n in described
            if n is parent or parent in list(n.ancestors())]
    if not near:
        where = described[0]
        emit(CID, FAIL,
             "the described element at %s is not inside %s, the field that "
             "owns the input; an error above the form is not next to it"
             % (where.where(), "<%s>" % (parent.tag if parent else "?")))

    texts = []
    for node in near:
        texts.extend(message_of(node, flat))
    if not texts:
        emit(CID, FAIL,
             "the element at %s renders no text this grader can resolve "
             "through %s, so the wording cannot be read"
             % (near[0].where(), rel(scratch, cat_path)))

    joined = " ".join(texts)
    if BANNED in joined.lower():
        emit(CID, FAIL,
             "the password error still reads %r" % joined.strip()[:60])
    if not REQUIREMENT.search(joined):
        emit(CID, FAIL,
             "the password error reads %r and states no requirement: no "
             "digit and no mention of characters" % joined.strip()[:80])

    emit(CID, PASS,
         "%s points at %s inside the same field, and it reads %r"
         % (field.where(), ", ".join(sorted(set(wanted))),
            joined.strip()[:80]))


if __name__ == "__main__":
    main()
