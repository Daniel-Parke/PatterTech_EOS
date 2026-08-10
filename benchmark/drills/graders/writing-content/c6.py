#!/usr/bin/env python3
"""Criterion 6: a failed submit leaves both fields as they were.

WCAG 3.3.3 in one line: when validation rejects what someone typed, do
not take it away from them. The fixture clears the password on failure,
which is the single most common form of this defect.

The check reads the submit handler rather than driving the form,
because these graders cannot run React offline. It finds the fields the
form controls, reads the handler wired to `onSubmit`, and looks for any
statement that empties one of those fields: a state setter called with
an empty string, an assignment of `""` to a `.value`, or a `reset()`.

Where a failure branch can be told apart, the search is scoped to it,
so a tree that clears the form after a successful submit is not failed
for it. Where no failure branch can be identified, the whole handler is
searched and the reason says so.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, function_body, jsx_roots,  # noqa: E402
                     match_bracket, read, rel, scratch_dir, strip_comments)

CID = "c6"

EMPTY = r"""(?:''|""|``)"""
CLEARS = (
    re.compile(r"(?<![\w.$])(set[A-Z]\w*)\s*\(\s*%s\s*\)" % EMPTY),
    re.compile(r"(\w+)\.value\s*=\s*%s" % EMPTY),
    re.compile(r"(\w*\.?reset)\s*\(\s*\)"),
)
ERROR_SETTER = re.compile(
    r"(?<![\w.$])set(Error|Errors|Failed|Invalid|Message|Problem|Issue)\w*"
    r"\s*\(|setState\s*\(\s*\{[^{}]*error", re.I)


def controlled_fields(scratch):
    """State names bound to an input's value, per file."""
    out = {}
    for path, root in jsx_roots(scratch):
        names = set()
        for node in root.elements():
            if node.tag.lower() not in ("input", "textarea", "select"):
                continue
            kind, value = node.attrs.get("value",
                                         node.attrs.get("defaultValue",
                                                        (None, "")))
            if kind != "expr":
                continue
            match = re.match(r"^[A-Za-z_$][\w$]*$", value.strip())
            if match:
                names.add(value.strip())
        if names:
            out[path] = names
    return out


def handlers(text):
    """(name, body) for every function wired to onSubmit in this file."""
    out = []
    for match in re.finditer(r"onSubmit\s*=\s*\{", text):
        end = match_bracket(text, match.end() - 1, "{", "}")
        expr = text[match.end():end - 1].strip() if end != -1 else ""
        name = re.match(r"^[A-Za-z_$][\w$]*$", expr)
        if name:
            decl = re.search(
                r"(?:function\s+%s\s*\(|(?:const|let|var)\s+%s\s*=)"
                % (re.escape(expr), re.escape(expr)), text)
            if decl:
                out.append((expr, function_body(text, decl.end())))
            continue
        if expr:
            out.append(("inline handler", function_body(text, 0) or expr))
    if not out:
        for match in re.finditer(
                r"(?:function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{)", text):
            body = function_body(text, match.start())
            if "preventDefault" in body:
                out.append((match.group(1), body))
    return out


def branches(body):
    """The `if (...) { ... }` blocks inside a handler body."""
    out = []
    for match in re.finditer(r"(?<![\w.$])if\s*\(", body):
        head = match_bracket(body, match.end() - 1)
        if head == -1:
            continue
        rest = body[head:]
        stripped = rest.lstrip()
        offset = head + (len(rest) - len(stripped))
        if stripped.startswith("{"):
            end = match_bracket(body, offset, "{", "}")
            if end != -1:
                out.append(body[offset:end])
        else:
            end = body.find(";", offset)
            out.append(body[offset:end + 1 if end != -1 else len(body)])
    return out


def clearings(chunk, fields):
    hits = []
    for rx in CLEARS:
        for match in rx.finditer(chunk):
            token = match.group(1)
            setters = {"set" + f[0].upper() + f[1:] for f in fields}
            if rx is CLEARS[0] and token not in setters:
                continue
            if rx is CLEARS[1] and token in ("error", "message"):
                continue
            hits.append(" ".join(match.group(0).split()))
    return hits


def main():
    scratch = scratch_dir()
    fields = controlled_fields(scratch)
    if not fields:
        emit(CID, FAIL,
             "no input in the markup binds its value to state, so nothing "
             "says what the fields hold after a submit")

    looked = []
    offences = []
    scoped = True
    for path, names in sorted(fields.items(), key=lambda kv: str(kv[0])):
        text = strip_comments(read(path))
        found = handlers(text)
        if not found:
            continue
        for name, body in found:
            looked.append("%s:%s" % (rel(scratch, path), name))
            failing = [b for b in branches(body)
                       if ERROR_SETTER.search(b) or "return" in b]
            chunks = failing
            if not failing:
                scoped = False
                chunks = [body]
            for chunk in chunks:
                for hit in clearings(chunk, names):
                    offences.append("%s in %s clears a field: %s"
                                    % (rel(scratch, path), name, hit))

    if not looked:
        emit(CID, FAIL,
             "no submit handler found in the files that own the form, so a "
             "failed submit cannot be reasoned about")
    if offences:
        unique = sorted(set(offences))
        emit(CID, FAIL,
             "%d statement(s) empty a field on the failure path: %s"
             % (len(unique), "; ".join(unique[:3])))

    emit(CID, PASS,
         "%s %s and nothing in %s empties a controlled field"
         % ("the failure branch of" if scoped else "the whole body of",
            ", ".join(looked),
            "it" if len(looked) == 1 else "them"))


if __name__ == "__main__":
    main()
