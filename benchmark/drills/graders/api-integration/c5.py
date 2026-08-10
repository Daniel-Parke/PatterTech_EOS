#!/usr/bin/env python3
"""Criterion 5: GET /orders pages by cursor and no longer by offset.

Three assertions in one: a cursor style query parameter is declared, the
success response carries a next token, and no offset style parameter
survives. All three are read off the document with local $ref chains
resolved, because the page schema is normally a component.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SPEC_REL, emit, load_spec,  # noqa: E402
                     operation, orders_path, parameters, resolve,
                     scratch_dir)

CID = "c5"

CURSOR = re.compile(
    r"^(page[_-]?token|next[_-]?page[_-]?token|next[_-]?token|cursor|"
    r"page[_-]?cursor|next[_-]?cursor|after|starting[_-]?after)$", re.I)
OFFSET = re.compile(r"^(offset|skip)$", re.I)
NEXT_FIELD = re.compile(
    r"^(next|next[_-]?page|next[_-]?link|next[_-]?url|"
    r"(next[_-]?)?(page[_-]?token|cursor|page[_-]?cursor|token)|"
    r"next[_-]?page[_-]?token|next[_-]?cursor)$", re.I)


def property_names(doc, schema, depth=0, seen=None):
    """Property names in a schema, following local refs and containers."""
    seen = seen or set()
    if depth > 6 or not isinstance(schema, dict):
        return []
    key = id(schema)
    if key in seen:
        return []
    seen.add(key)
    schema = resolve(doc, schema)
    if not isinstance(schema, dict):
        return []
    out = []
    props = schema.get("properties")
    if isinstance(props, dict):
        for name, sub in props.items():
            out.append(str(name))
            out.extend(property_names(doc, sub, depth + 1, seen))
    for combiner in ("allOf", "anyOf", "oneOf"):
        for sub in schema.get(combiner) or []:
            out.extend(property_names(doc, sub, depth + 1, seen))
    items = schema.get("items")
    if isinstance(items, dict):
        out.extend(property_names(doc, items, depth + 1, seen))
    return out


def success_fields(doc, op):
    responses = op.get("responses")
    if not isinstance(responses, dict):
        return []
    names = []
    for code, response in responses.items():
        if not str(code).startswith("2"):
            continue
        response = resolve(doc, response)
        content = (response or {}).get("content")
        if not isinstance(content, dict):
            continue
        for body in content.values():
            if isinstance(body, dict):
                names.extend(property_names(doc, body.get("schema")))
    return names


def main():
    scratch = scratch_dir()
    doc = load_spec(CID, scratch)

    key, item = orders_path(doc)
    if item is None:
        emit(CID, FAIL, "%s declares no order collection path" % SPEC_REL)
    op = operation(item, "get")
    if op is None:
        emit(CID, FAIL, "%s declares no GET %s" % (SPEC_REL, key))

    query = [p for p in parameters(doc, item, op)
             if str(p.get("in", "")).lower() == "query"]
    names = [str(p.get("name", "")).strip() for p in query]
    cursor = [n for n in names if CURSOR.match(n)]
    offset = [n for n in names if OFFSET.match(n)]
    fields = success_fields(doc, op)
    next_field = [f for f in fields if NEXT_FIELD.match(f)]

    problems = []
    if not cursor:
        problems.append(
            "no cursor style query parameter (found %s)"
            % (", ".join(names) or "no query parameters at all"))
    if not next_field:
        problems.append(
            "the success response carries no next token field (found %s)"
            % (", ".join(sorted(set(fields))[:8]) or "no properties"))
    if offset:
        problems.append(
            "%s is still declared, which is the paging FRAG-09 warns about"
            % ", ".join(offset))
    if problems:
        emit(CID, FAIL, "GET %s: %s" % (key, "; ".join(problems)))

    emit(CID, PASS,
         "GET %s takes %s, returns %s and declares no offset parameter"
         % (key, ", ".join(cursor), ", ".join(sorted(set(next_field)))))


if __name__ == "__main__":
    main()
