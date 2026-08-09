#!/usr/bin/env python3
"""Criterion 2: forward only, and said so somewhere parseable.

Two halves. Nothing in the tree may be named as an undo: no down file,
no undo script, no rollback directory. And the change record has to
assert forward-only recovery in a field a machine can read, rather than
leaving it as a sentence in a paragraph.

The field is matched as `key: value`, in Markdown, front matter, JSON,
YAML or a Markdown table row. Prose that merely mentions rolling
forward is not a field and does not count.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, ROLLBACK_TOKENS, SKIP_DIRS,  # noqa: E402
                     document_files, emit, path_tokens, read, scratch_dir)

CID = "c2"

FIELD = re.compile(
    r"""(?im)^[\s>*|\-]*["'`]?\**\s*
        (recovery|rollback|roll[ _-]?forward)
        (?:[ _-](?:strategy|plan|policy|mode|method))?
        \**["'`]?\s*[:=|]\s*\**["'`]?\s*
        (forward[ _-]?only|roll[ _-]?forward|forward[ _-]?fix|
         no[ _-]?rollback|forward)""",
    re.X)


def undo_named(scratch):
    out = []
    for path in sorted(scratch.rglob("*")):
        rel = path.relative_to(scratch)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path_tokens(rel) & ROLLBACK_TOKENS:
            out.append(rel.as_posix() + ("/" if path.is_dir() else ""))
    # A directory and its contents are one finding, not four.
    return [p for p in out
            if not any(p != q and p.startswith(q) for q in out)]


def main():
    scratch = scratch_dir()

    named = undo_named(scratch)
    if named:
        emit(CID, FAIL,
             "%d path(s) are named as an undo: %s. Forward-only recovery "
             "means there is nothing to run backwards"
             % (len(named), ", ".join(named[:6])))

    for path in document_files(scratch):
        match = FIELD.search(read(path))
        if match:
            emit(CID, PASS,
                 "no down or undo file anywhere, and %s asserts it in a "
                 "field: %s"
                 % (path.relative_to(scratch).as_posix(),
                    " ".join(match.group(0).split())))

    emit(CID, FAIL,
         "no down or undo file, but no change record asserts forward-only "
         "recovery in a parseable field (looked for a recovery or rollback "
         "key set to forward-only in the documents of the tree)")


if __name__ == "__main__":
    main()
