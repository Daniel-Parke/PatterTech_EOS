#!/usr/bin/env python3
"""Criterion 4: the removed flag is gone from the docs and the real one is in.

Both halves matter. Deleting the offending block removes `--outdir` and
leaves a quickstart that no longer shows anyone how to choose an output
directory, so the grader also requires `--out-dir` to appear in the
quickstart itself.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, rel, scratch_dir  # noqa: E402

CID = "c4"

REMOVED = "--outdir"
CURRENT = "--out-dir"


def searched(scratch):
    """`grep -r -- "--outdir" docs README.md`, as files."""
    found = []
    docs = scratch / "docs"
    if docs.is_dir():
        found.extend(p for p in sorted(docs.rglob("*"))
                     if p.is_file() and ".git" not in p.parts)
    readme = scratch / "README.md"
    if readme.is_file():
        found.append(readme)
    return found


def main():
    scratch = scratch_dir()
    files = searched(scratch)
    if not files:
        emit(CID, FAIL, "neither docs/ nor README.md is in the tree")

    hits = []
    for path in files:
        text = read(path)
        for i, line in enumerate(text.splitlines(), 1):
            # `--out-dir` does not contain `--outdir`, so a plain
            # substring test is exact here.
            if REMOVED in line:
                hits.append("%s:%d: %s"
                            % (rel(scratch, path), i, line.strip()[:80]))
    if hits:
        emit(CID, FAIL,
             "the removed flag %s still appears %d time(s) under docs/ or in "
             "README.md: %s" % (REMOVED, len(hits), "; ".join(hits[:3])))

    quickstart = scratch / "docs" / "quickstart.md"
    if not quickstart.is_file():
        emit(CID, FAIL,
             "docs/quickstart.md is not in the tree, so the flag a reader "
             "needs cannot be in it")
    if CURRENT not in read(quickstart):
        emit(CID, FAIL,
             "%s is gone from the docs but %s never appears in "
             "docs/quickstart.md, so the quickstart no longer shows how to "
             "choose an output directory" % (REMOVED, CURRENT))

    emit(CID, PASS,
         "%s appears nowhere under docs/ or in README.md, and %s appears in "
         "docs/quickstart.md" % (REMOVED, CURRENT))


if __name__ == "__main__":
    main()
