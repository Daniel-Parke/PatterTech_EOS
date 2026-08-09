#!/usr/bin/env python3
"""Criterion 2: nothing generated has been edited by hand.

The spec words this as `git diff --exit-code` after the build. The
grader takes the same measurement without needing the delivered tree to
be a git repository: it records the bytes of every file, runs the
regeneration, and requires every file that existed before to be
unchanged. A file the build newly creates is not a diff in this sense,
because a build that writes an ignored output directory is ordinary.

A hand edit to a generated file shows up here as the build putting its
own version back. So does a generator that is not deterministic, which
is the same defect wearing a different hat: either way the committed
file is not what the source says it should be.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SKIP_DIRS, build_commands,  # noqa: E402
                     copy_tree, emit, generated_token_files, rel, run_build,
                     scratch_dir)

CID = "c2"


def snapshot(tree):
    out = {}
    for path in Path(tree).rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            out[rel(tree, path)] = path.read_bytes()
        except OSError:
            continue
    return out


def main():
    scratch = scratch_dir()
    if not build_commands(scratch):
        emit(CID, FAIL,
             "no regeneration entry point: nothing under tools/ or scripts/ "
             "rebuilds the generated files, so 'regenerate and diff' cannot "
             "be run at all")
    outputs = generated_token_files(scratch)
    if not outputs:
        emit(CID, FAIL,
             "no generated token output in the tree, so a no-op build would "
             "satisfy this criterion for free")

    work, copy = copy_tree(scratch, prefix="drill-uiux-c2-")
    try:
        before = snapshot(copy)
        ok, label, why = run_build(copy)
        if not ok:
            emit(CID, FAIL, "regeneration failed: %s" % why)
        after = snapshot(copy)

        changed = sorted(n for n, blob in before.items()
                         if after.get(n) != blob)
        if changed:
            generated = {rel(scratch, p) for p in outputs}
            hit = [n for n in changed if n in generated]
            tail = ""
            if hit:
                tail = (". %s is generated token output, so it was edited by "
                        "hand or the generator is not deterministic" % hit[0])
            emit(CID, FAIL,
                 "%s changed %d committed file(s) after a clean run: %s%s"
                 % (label, len(changed), ", ".join(changed[:4]), tail))

        emit(CID, PASS,
             "%s reproduces the tree exactly: %d file(s) checked, %d of them "
             "generated token output, none changed"
             % (label, len(before), len(outputs)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
