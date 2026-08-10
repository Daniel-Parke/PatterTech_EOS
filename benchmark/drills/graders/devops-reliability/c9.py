#!/usr/bin/env python3
"""Criterion 9: the SLO still stands, and the record names what is at risk.

The first half is a structural conformance check against the shape
OpenSLO v1 requires: apiVersion, kind, metadata.name, and a spec with a
service, an indicator and at least one objective carrying a numeric
target. It is not a full JSON Schema validation, and the reason says so
rather than claiming more than was done. What it does catch is the
failure this criterion exists for: an SLO file edited or deleted on the
way past.

The second half is a substring: the change record has to name the SLI
or the SLO by the name the file gives it.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, document_files, emit,  # noqa: E402
                     iter_files, load_structured, path_tokens, read,
                     scratch_dir)

CID = "c9"

SLO_TOKENS = {"slo", "slos", "openslo", "sli"}


def slo_files(scratch):
    out = []
    for path in iter_files(scratch, suffixes={".yaml", ".yml", ".json"}):
        rel = path.relative_to(scratch)
        text = read(path)
        if (path_tokens(rel) & SLO_TOKENS) or "openslo" in text.lower():
            out.append(path)
    return out


def conformance(doc):
    """The first thing wrong with an OpenSLO document, or None."""
    if not isinstance(doc, dict):
        return "the document is not a mapping"
    api = str(doc.get("apiVersion") or "")
    if not api.lower().startswith("openslo"):
        return "apiVersion is %r, not an openslo one" % doc.get("apiVersion")
    if str(doc.get("kind") or "").upper() != "SLO":
        return "kind is %r, not SLO" % doc.get("kind")
    metadata = doc.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("name"):
        return "metadata.name is missing"
    spec = doc.get("spec")
    if not isinstance(spec, dict):
        return "spec is missing"
    if not spec.get("service"):
        return "spec.service is missing"
    if not (spec.get("indicator") or spec.get("indicatorRef")):
        return "spec has neither indicator nor indicatorRef"
    objectives = spec.get("objectives")
    if not isinstance(objectives, list) or not objectives:
        return "spec.objectives is empty"
    for objective in objectives:
        if not isinstance(objective, dict):
            return "an objective is not a mapping"
        target = objective.get("target", objective.get("targetPercent"))
        if not isinstance(target, (int, float)) or isinstance(target, bool):
            return "an objective has no numeric target"
    return None


def names_in(doc):
    out = set()
    metadata = doc.get("metadata") or {}
    for key in ("name", "displayName"):
        if metadata.get(key):
            out.add(str(metadata[key]))
    spec = doc.get("spec") or {}
    indicator = spec.get("indicator")
    if isinstance(indicator, dict):
        meta = indicator.get("metadata") or {}
        for key in ("name", "displayName"):
            if meta.get(key):
                out.add(str(meta[key]))
    if spec.get("indicatorRef"):
        out.add(str(spec["indicatorRef"]))
    return {n for n in out if len(n) > 3}


def variants(name):
    base = name.strip()
    return {base, base.replace("-", " "), base.replace("-", "_"),
            base.replace("_", "-"), base.replace(" ", "-")}


def main():
    scratch = scratch_dir()
    files = slo_files(scratch)
    if not files:
        emit(CID, FAIL, "no SLO file in the tree")

    valid, names, problems = [], set(), []
    for path in files:
        rel = path.relative_to(scratch).as_posix()
        doc, error = load_structured(path)
        if error:
            problems.append("%s: %s" % (rel, error))
            continue
        wrong = conformance(doc)
        if wrong:
            problems.append("%s: %s" % (rel, wrong))
            continue
        valid.append(rel)
        names |= names_in(doc)

    if not valid:
        emit(CID, FAIL,
             "no SLO document conforms to the OpenSLO shape: %s"
             % "; ".join(problems[:3]))
    if problems:
        emit(CID, FAIL,
             "%s conforms but %s" % (", ".join(valid), "; ".join(problems[:2])))

    wanted = sorted({v for name in names for v in variants(name)})
    # The SLO file names the SLI by definition, and so may the rollout
    # plan. Neither is the change record, so neither settles this.
    skip = set(files)
    for path in document_files(scratch):
        if path in skip or path.relative_to(scratch).parts[0] in (
                "slo", "slos", "config", "deploy"):
            continue
        text = read(path)
        for token in wanted:
            if re.search(re.escape(token), text, re.I):
                emit(CID, PASS,
                     "%s conforms to the OpenSLO shape (structurally, not "
                     "against the published JSON Schema), and %s names %r"
                     % (", ".join(valid),
                        path.relative_to(scratch).as_posix(), token))

    emit(CID, FAIL,
         "%s conforms, but no change record names the SLI or the SLO at "
         "risk (looked for %s)"
         % (", ".join(valid), ", ".join(sorted(names)) or "nothing nameable"))


if __name__ == "__main__":
    main()
