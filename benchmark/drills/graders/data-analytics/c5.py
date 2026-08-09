#!/usr/bin/env python3
"""Criterion 5: every name in the delivered taxonomy is object then verb.

The frozen regex is `^[A-Z][a-z]+( [A-Z][a-z]+)* [A-Z][a-z]+ed$`, and
the criterion adds that no name may carry a digit or a user identifier.
The raw export is full of `checkout_completed_v2` and `order_placed_v3`,
so a taxonomy that copies the source names forward fails on both counts.

Pulling names out of a free-form file is the part that needs care, and
the rule is precedence rather than guesswork. Structured sources are
taken literally: `name:` values in YAML and JSON, the first column of a
CSV, the first cell of a Markdown table row. Only when a file offers
none of those does it fall back to backticked spans and list items, and
then only to strings that look like a name at all, so that a sentence of
prose in a bullet is not marked as a badly named event.

That fallback is the soft edge of this grader. It is stated here rather
than hidden: a taxonomy written as running prose with no table, no list
and no code spans would be read as declaring no names, and reported as
such rather than passed.
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, parse_yaml, read, rel,  # noqa: E402
                     scratch_dir, walk, walk_docs)

CID = "c5"

SHAPE = re.compile(r"^[A-Z][a-z]+( [A-Z][a-z]+)* [A-Z][a-z]+ed$")
IDENTIFIER = re.compile(r"(?i)email|user_?id|\buid\b|customer_?id|@")
DIGIT = re.compile(r"\d")

SUFFIXES = (".md", ".markdown", ".yml", ".yaml", ".json", ".csv", ".tsv",
            ".txt")
FILENAME_HINTS = ("taxonomy",)
PAIR_HINTS = (("event", "naming"), ("event", "dictionary"),
              ("event", "catalog"), ("event", "catalogue"),
              ("event", "glossary"), ("event", "spec"), ("event", "names"),
              ("event", "map"))

NAME_KEYS = {"name", "event", "event_name", "eventname", "display_name"}
# A name-shaped string: title case throughout, or snake_case.
LOOKS_LIKE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*([ _][A-Za-z0-9_]+){0,5}$")
BACKTICK = re.compile(r"`([^`\n]{2,60})`")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.+?)\s*$", re.M)


def taxonomy_files(scratch):
    out = []
    for path in walk(scratch, SUFFIXES):
        relative = rel(scratch, path)
        lower = relative.lower()
        if any(h in lower for h in FILENAME_HINTS):
            out.append((relative, path, "named for the taxonomy"))
            continue
        if any(a in lower and b in lower for a, b in PAIR_HINTS):
            out.append((relative, path, "an event naming document"))
    if out:
        return out
    for path in walk(scratch, SUFFIXES):
        text = read(path).lower()
        if "taxonomy" in text and "event" in text:
            out.append((rel(scratch, path), path,
                        "declares a taxonomy in its text"))
    return out


def title_case(token_string):
    tokens = token_string.split()
    return bool(tokens) and all(t[:1].isupper() for t in tokens)


def structured_names(path, text):
    """Names from sources that say outright that they are names."""
    suffix = path.suffix.lower()
    out = []
    if suffix in (".yml", ".yaml", ".json"):
        doc = json.loads(text) if suffix == ".json" else parse_yaml(text)
        if doc is None:
            return []
        for node in walk_docs(doc):
            for key, value in node.items():
                if str(key).lower() in NAME_KEYS and isinstance(value, str):
                    out.append(value.strip())
            events = node.get("events")
            if isinstance(events, dict):
                out.extend(str(k).strip() for k in events)
        return out
    if suffix in (".csv", ".tsv"):
        delim = "\t" if suffix == ".tsv" else ","
        rows = list(csv.reader(text.splitlines(), delimiter=delim))
        for row in rows[1:]:
            if row and row[0].strip():
                out.append(row[0].strip())
        return out
    # Markdown table: first cell of every body row.
    rows = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    body = [r for r in rows if not re.match(r"^\s*\|[\s:|-]+\|\s*$", r)]
    for row in body[1:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if cells and cells[0]:
            out.append(re.sub(r"[`*_]", "", cells[0]).strip())
    return out


def loose_names(text):
    out = []
    for match in BACKTICK.finditer(text):
        out.append(match.group(1).strip())
    if not out:
        for match in LIST_ITEM.finditer(text):
            item = re.split(r"\s+[-—:]\s+|:\s", match.group(1), 1)[0]
            out.append(re.sub(r"[`*_]", "", item).strip())
    return [n for n in out
            if LOOKS_LIKE_NAME.match(n) and (title_case(n) or "_" in n)]


def main():
    scratch = scratch_dir()
    files = taxonomy_files(scratch)
    if not files:
        emit(CID, FAIL,
             "no taxonomy file in the delivered tree: nothing is named for a "
             "taxonomy, nothing reads as an event naming document, and no "
             "file declares one in its text")

    best = None
    for relative, path, why in files:
        text = read(path)
        try:
            names = structured_names(path, text)
        except ValueError:
            names = []
        source = "structured"
        if not names:
            names = loose_names(text)
            source = "code spans and list items"
        names = [n for n in dict.fromkeys(names) if n]
        if len(names) < 3:
            best = best or (relative, "declares %d event name(s); a taxonomy "
                                      "for this export names at least the "
                                      "signup, checkout and order events"
                                      % len(names))
            continue
        offences = []
        for name in names:
            if not SHAPE.match(name):
                offences.append("%r is not object then past-tense action"
                                % name)
            elif DIGIT.search(name):
                offences.append("%r carries a digit" % name)
            elif IDENTIFIER.search(name):
                offences.append("%r carries a user identifier" % name)
        if offences:
            best = (relative, "%d of %d names fail: %s"
                    % (len(offences), len(names), "; ".join(offences[:4])))
            continue
        emit(CID, PASS,
             "%s (%s) declares %d event names, read from %s, and every one "
             "matches object then past-tense action with no digit and no "
             "identifier" % (relative, why, len(names), source))

    relative, reason = best
    emit(CID, FAIL, "%s: %s" % (relative, reason))


if __name__ == "__main__":
    main()
