#!/usr/bin/env python3
"""Criterion 10: a funnel carries its three parameters as configuration.

Ordering mode, exclusion steps and conversion denominator, machine
readable, beside the number. The same product yields different rates
under different parameter sets, so a rate without them means nothing.

Three outcomes and each is reported for what it is. A plan that
describes a funnel in prose with no configuration fails. A plan that
declares no funnel at all leaves this criterion without a subject, which
is reported unsettled rather than passed: nothing was measured. A funnel
written only in YAML on a machine with no YAML parser is unsettled for
the same reason.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, all_files, emit,  # noqa: E402
                     read, scratch_dir)

CID = "c10"

PLAN = "growth_decisions.md"

FENCE = re.compile(r"```(?:json|jsonc)\s*\n(.*?)```", re.S | re.I)

NEEDED = (
    ("step ordering mode", re.compile(r"order", re.I)),
    ("exclusion steps", re.compile(r"exclu", re.I)),
    ("conversion denominator", re.compile(r"denominat", re.I)),
)

TEXT_SUFFIXES = (".md", ".txt", ".rst", ".html")


def documents(scratch):
    """Every machine-readable document in the tree, with its origin."""
    out = []
    for path in all_files(scratch):
        rel = path.relative_to(scratch).as_posix()
        suffix = path.suffix.lower()
        if suffix in (".json", ".jsonc"):
            try:
                out.append((rel, json.loads(read(path))))
            except ValueError:
                continue
        elif suffix == ".toml":
            try:
                import tomllib
            except ImportError:
                continue
            try:
                with open(path, "rb") as handle:
                    out.append((rel, tomllib.load(handle)))
            except (OSError, ValueError):
                continue
        elif suffix in TEXT_SUFFIXES:
            for i, block in enumerate(FENCE.findall(read(path))):
                try:
                    out.append(("%s block %d" % (rel, i + 1),
                                json.loads(block)))
                except ValueError:
                    continue
    return out


def funnels(node, key=None, where="$"):
    if isinstance(node, dict):
        marked = "funnel" in str(key or "").lower() or \
            any(str(k).lower() in ("steps", "step_order", "stages")
                for k in node)
        if marked:
            yield where, node
        for name, value in node.items():
            yield from funnels(value, name, "%s.%s" % (where, name))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from funnels(value, key, "%s[%d]" % (where, i))


def keys_under(node):
    out = set()
    if isinstance(node, dict):
        for name, value in node.items():
            out.add(str(name))
            out |= keys_under(value)
    elif isinstance(node, list):
        for value in node:
            out |= keys_under(value)
    return out


def main():
    scratch = scratch_dir()
    plans = [p for p in all_files(scratch) if p.name.lower() == PLAN]
    if not plans:
        emit(CID, FAIL, "no GROWTH_DECISIONS.md, so there is no measurement "
                        "plan and nothing stores a funnel's parameters")

    found = []
    for origin, doc in documents(scratch):
        for where, node in funnels(doc):
            found.append((origin, where, node))

    if not found:
        yaml_talk = [p.relative_to(scratch).as_posix() for p in
                     all_files(scratch)
                     if p.suffix.lower() in (".yaml", ".yml")
                     and "funnel" in read(p).lower()]
        if yaml_talk:
            emit(CID, UNSETTLED,
                 "a funnel appears only in YAML (%s) and no YAML parser is "
                 "in the standard library, so its configuration was not read"
                 % ", ".join(yaml_talk[:3]))
        prose = [p.relative_to(scratch).as_posix() for p in all_files(scratch)
                 if p.suffix.lower() in TEXT_SUFFIXES
                 and "funnel" in read(p).lower()]
        if prose:
            emit(CID, FAIL,
                 "a funnel is described in prose (%s) but no machine-readable "
                 "configuration declares its ordering mode, exclusion steps "
                 "or denominator" % ", ".join(prose[:3]))
        emit(CID, UNSETTLED,
             "the measurement plan declares no funnel, so this criterion has "
             "no subject in this tree and nothing was checked")

    faults = []
    for origin, where, node in found:
        keys = keys_under(node)
        missing = [name for name, pattern in NEEDED
                   if not any(pattern.search(k) for k in keys)]
        if missing:
            faults.append("%s %s stores no %s"
                          % (origin, where, ", ".join(missing)))
    if faults:
        emit(CID, FAIL, "%d funnel(s) are missing configuration: %s"
                        % (len(faults), "; ".join(faults[:4])))

    emit(CID, PASS,
         "%d funnel(s) each store an ordering mode, exclusion steps and a "
         "conversion denominator: %s"
         % (len(found), "; ".join("%s %s" % (o, w) for o, w, _ in found[:4])))


if __name__ == "__main__":
    main()
