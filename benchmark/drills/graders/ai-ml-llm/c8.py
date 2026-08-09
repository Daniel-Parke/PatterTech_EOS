#!/usr/bin/env python3
"""Criterion 8: a held-out split the tuning path never reads.

The prompt-selection path is located structurally rather than by
filename: any source file that reaches for `prompt_b` is part of
choosing between the variants. That is the code the held-out filename
must not appear in. Locating it this way has one blind spot, and the
grader says so when it hits it: if nothing in the tree names prompt_b,
the selection path cannot be found and the criterion fails as
unlocatable rather than passing by default.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, flat_text, load_jsonl,  # noqa: E402
                     read, rel, require_report, scratch_dir, walk)

CID = "c8"

HELD_HINT = re.compile(r"hold|held|test|final|blind|locked|unseen", re.I)
TUNE_HINT = re.compile(r"dev|tune|tuning|train|select|calib|labelled|labeled",
                       re.I)


def data_files(scratch):
    """Sample files, excluding JSON documents that are plainly reports."""
    out = []
    for path in walk(scratch, {".jsonl", ".ndjson", ".csv", ".tsv", ".json"}):
        if path.suffix.lower() == ".json":
            try:
                doc = json.loads(read(path))
            except ValueError:
                continue
            if not isinstance(doc, list) or not doc:
                continue
        out.append(path)
    return out


def rows_in(path):
    if path.suffix.lower() in (".jsonl", ".ndjson"):
        return len(load_jsonl(path))
    if path.suffix.lower() == ".json":
        try:
            return len(json.loads(read(path)))
        except (ValueError, TypeError):
            return 0
    return max(0, len([l for l in read(path).splitlines() if l.strip()]) - 1)


def selection_files(scratch):
    return [p for p in walk(scratch, {".py", ".sh", ".mk", ".toml", ".yml",
                                      ".yaml", ".cfg", ".ini"})
            if "prompt_b" in read(p).lower()]


def mentions(text, path):
    name = path.name
    if name in text:
        return True
    return bool(re.search(r"\b%s\b" % re.escape(path.stem), text))


def main():
    scratch = scratch_dir()
    run = require_report(CID, scratch)

    files = data_files(scratch)
    if len(files) < 2:
        emit(CID, FAIL,
             "the tree holds %d sample file(s) (%s), so nothing was held "
             "back: whatever the prompt was chosen on is what it was "
             "scored on"
             % (len(files), ", ".join(rel(scratch, p) for p in files) or
                "none"))

    selectors = selection_files(scratch)
    if not selectors:
        emit(CID, FAIL,
             "no source file reads prompt_b, so the prompt-selection path "
             "cannot be located and its separation from the held-out split "
             "cannot be shown")

    blob = flat_text(run.report)
    named = [p for p in files if mentions(blob, p)]
    if not named:
        emit(CID, FAIL,
             "%s names none of the sample files (%s), so the report does "
             "not say what it was scored on"
             % (run.rel, ", ".join(rel(scratch, p) for p in files[:4])))

    selector_text = "\n".join(read(p) for p in selectors)
    clean, seen = [], []
    for path in sorted(named, key=lambda p: (not HELD_HINT.search(p.name),
                                             TUNE_HINT.search(p.name) is None,
                                             p.name)):
        if mentions(selector_text, path):
            seen.append(rel(scratch, path))
            continue
        if rows_in(path) < 1:
            continue
        clean.append(path)

    if not clean:
        emit(CID, FAIL,
             "every sample file the report names is also read by the "
             "prompt-selection code (%s in %s), so the split the eval "
             "reports on is the one the prompt was tuned against"
             % (", ".join(seen[:3]) or "none",
                ", ".join(rel(scratch, p) for p in selectors[:3])))

    held = clean[0]
    emit(CID, PASS,
         "%s holds %d records, is named in %s, and none of the "
         "prompt-selection code (%s) mentions it"
         % (rel(scratch, held), rows_in(held), run.rel,
            ", ".join(rel(scratch, p) for p in selectors[:3])))


if __name__ == "__main__":
    main()
