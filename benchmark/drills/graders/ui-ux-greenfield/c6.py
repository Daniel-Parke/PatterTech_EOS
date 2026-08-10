#!/usr/bin/env python3
"""Criterion 6: a states manifest covering six states for every component.

The pack's B7 shape: focus, hover, active, disabled, loading and error,
one entry per component per state, and a state a component cannot enter
declared absent with a reason rather than left out. A missing entry and
a deliberate omission look the same to a walk, so a missing entry
fails.

Two carriers are read, a JSON or YAML-ish manifest and a markdown table
with a column per state, because the drill names the artefact and not
its file format.

Coverage is the weak half and is stated as such. Where the tree has a
components directory the grader requires every module in it to appear
in the manifest, which is a real check. Where it does not, the grader
falls back to requiring at least two components, because a dosage entry
screen has at minimum a field and a control, and it cannot prove that
every interactive component in an arbitrary tree is named.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SOURCE_SUFFIXES, emit, read, rel,  # noqa: E402
                     scratch_dir, walk)

CID = "c6"

STATES = ["focus", "hover", "active", "disabled", "loading", "error"]
ABSENT_WORDS = ("absent", "n/a", "na", "not applicable", "none",
                "cannot", "never")
COMPONENT_DIRS = {"components", "component", "ui", "widgets", "elements",
                  "controls"}
SKIP_KEYS = {"name", "version", "note", "notes", "description", "summary",
             "$schema", "schema", "generated", "source"}


def normalise(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def words(value):
    return len([w for w in re.split(r"\s+", str(value).strip()) if w])


def state_map(value):
    """A component's states as {state: entry}, or None if it is not one."""
    if not isinstance(value, dict):
        return None
    lowered = {str(k).lower(): v for k, v in value.items()}
    if isinstance(lowered.get("states"), dict):
        return {str(k).lower(): v for k, v in lowered["states"].items()}
    if any(state in lowered for state in STATES):
        return lowered
    return None


def components_from(doc):
    out = {}
    if isinstance(doc, dict):
        for key in ("components", "manifest", "componentstates"):
            for actual in doc:
                if str(actual).lower() == key:
                    return components_from(doc[actual])
        for name, value in doc.items():
            if str(name).lower() in SKIP_KEYS or str(name).startswith("$"):
                continue
            states = state_map(value)
            if states:
                out[str(name)] = states
    elif isinstance(doc, list):
        for item in doc:
            if not isinstance(item, dict):
                continue
            lowered = {str(k).lower(): v for k, v in item.items()}
            name = lowered.get("component") or lowered.get("name") \
                or lowered.get("id")
            states = state_map(item)
            if name and states:
                out[str(name)] = states
    return out


def entry_verdict(entry):
    """(ok, why) for one component-state entry."""
    if entry is None or entry is False:
        return False, "declared absent with no reason"
    if entry is True:
        return True, ""
    if isinstance(entry, dict):
        lowered = {str(k).lower(): v for k, v in entry.items()}
        absent = (lowered.get("absent") is True
                  or lowered.get("present") is False
                  or lowered.get("applicable") is False
                  or str(lowered.get("state", "")).lower() in ABSENT_WORDS
                  or str(lowered.get("status", "")).lower() in ABSENT_WORDS)
        reason = ""
        for key in ("reason", "why", "note", "because", "comment"):
            if isinstance(lowered.get(key), str):
                reason = lowered[key]
                break
        if absent:
            if words(reason) < 4:
                return False, "declared absent with no reason worth reading"
            return True, ""
        if not any(isinstance(v, (str, int, float, bool, dict, list))
                   and v not in ("", None) for v in lowered.values()):
            return False, "entry is empty"
        return True, ""
    if isinstance(entry, str):
        text = entry.strip()
        if not text:
            return False, "entry is empty"
        low = text.lower()
        if any(low.startswith(word) for word in ABSENT_WORDS) \
                or "not applicable" in low:
            if words(text) < 5:
                return False, "declared absent (%r) with no reason" % text
        return True, ""
    return False, "entry is %r" % (entry,)


def json_manifests(scratch):
    out = []
    for path in walk(scratch, {".json"}):
        text = read(path).lower()
        if not all(state in text for state in STATES):
            continue
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        found = components_from(doc)
        if found:
            out.append((path, found))
    return out


def table_manifests(scratch):
    """Markdown tables with a component column and one column per state."""
    out = []
    for path in walk(scratch, {".md", ".markdown"}):
        rows = [line for line in read(path).splitlines()
                if line.strip().startswith("|")]
        header = None
        found = {}
        for line in rows:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            low = [c.lower() for c in cells]
            if header is None:
                if any("component" in c for c in low) \
                        and all(any(state in c for c in low)
                                for state in STATES):
                    header = low
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue
            entry = {}
            for state in STATES:
                index = next((i for i, c in enumerate(header)
                              if state in c), None)
                if index is not None and index < len(cells):
                    entry[state] = cells[index]
            if cells and cells[0]:
                found[cells[0]] = entry
        if found:
            out.append((path, found))
    return out


def component_modules(scratch):
    out = {}
    for path in walk(scratch, SOURCE_SUFFIXES):
        parts = [p.lower() for p in path.parts]
        if not any(part in COMPONENT_DIRS for part in parts[:-1]):
            continue
        stem = path.stem
        if stem.lower() in ("index", "main"):
            continue
        out[normalise(stem)] = rel(scratch, path)
    return out


def main():
    scratch = scratch_dir()
    manifests = json_manifests(scratch) + table_manifests(scratch)
    if not manifests:
        emit(CID, FAIL,
             "no states manifest in the delivered tree: no file names the "
             "six states (%s) against a component" % ", ".join(STATES))

    best = None
    for path, components in manifests:
        where = rel(scratch, path)
        problems = []
        for name, states in sorted(components.items()):
            for state in STATES:
                if state not in states:
                    problems.append("%s has no %s entry" % (name, state))
                    continue
                ok, why = entry_verdict(states[state])
                if not ok:
                    problems.append("%s %s: %s" % (name, state, why))
        if problems:
            best = best or (where, "; ".join(problems[:4]))
            continue

        modules = component_modules(scratch)
        covered = {normalise(name) for name in components}
        if modules:
            missing = [module for key, module in sorted(modules.items())
                       if key not in covered]
            if missing:
                best = best or (
                    where, "%d component module(s) have no manifest entry: %s"
                    % (len(missing), ", ".join(missing[:4])))
                continue
            emit(CID, PASS,
                 "%s covers %d component(s) across all six states, and every "
                 "component module (%s) has an entry"
                 % (where, len(components), ", ".join(
                     sorted(modules.values())[:4])))
        if len(components) < 2:
            best = best or (
                where, "the manifest names one component only (%s); a dosage "
                       "entry screen has at least a field and a control"
                       % ", ".join(components))
            continue
        emit(CID, PASS,
             "%s covers %d component(s) (%s) across all six states, with any "
             "absent state given a reason"
             % (where, len(components), ", ".join(sorted(components)[:6])))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
