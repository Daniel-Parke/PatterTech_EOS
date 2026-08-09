#!/usr/bin/env python3
"""Criterion 1: a valid token source, two platform outputs, reproducible.

Three questions, in order. Does `tokens/tokens.json` parse and hold a
document the DTCG format would accept: every token typed, every alias
resolving, no illegal names. Are there generated outputs for at least
two platforms. And are those outputs what the source produces now,
which is settled by deleting them on a copy and building again, rather
than by trusting a header comment.

The delete-and-rebuild is the part worth having. An output that merely
exists proves someone once ran a generator; an output the current
source reproduces byte for byte proves the pipeline is real.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tree, dtcg_check, emit,  # noqa: E402
                     generated_token_files, platform_of, read, rel,
                     run_build, scratch_dir, short, token_source)

CID = "c1"


def main():
    scratch = scratch_dir()
    source = token_source(scratch)
    if not source.is_file():
        emit(CID, FAIL, "no token source at tokens/tokens.json")

    try:
        doc = json.loads(read(source))
    except ValueError as exc:
        emit(CID, FAIL, "tokens/tokens.json does not parse: %s" % short(exc))
    if not isinstance(doc, dict):
        emit(CID, FAIL, "tokens/tokens.json is not a DTCG document: the top "
                        "level is %s, not an object" % type(doc).__name__)

    tokens, errors = dtcg_check(doc)
    if errors:
        emit(CID, FAIL,
             "tokens/tokens.json is not valid DTCG (%d problem(s)): %s"
             % (len(errors), "; ".join(errors[:3])))
    if not tokens:
        emit(CID, FAIL, "tokens/tokens.json holds no tokens: nothing has a "
                        "$value")

    outputs = generated_token_files(scratch)
    platforms = sorted({platform_of(p) for p in outputs})
    if len(platforms) < 2:
        emit(CID, FAIL,
             "generated token output covers %d platform(s) %s; the criterion "
             "asks for at least two. Looked for built files under tokens/ or "
             "a build, generated or dist directory"
             % (len(platforms), platforms or "[]"))

    work, copy = copy_tree(scratch, prefix="drill-uiux-c1-")
    try:
        before = {}
        for path in outputs:
            before[rel(scratch, path)] = path.read_bytes()
        for name in before:
            (copy / name).unlink()

        ok, label, why = run_build(copy)
        if not ok:
            emit(CID, FAIL,
                 "the generated token output could not be reproduced: %s"
                 % why)

        missing, differing = [], []
        for name, blob in sorted(before.items()):
            rebuilt = copy / name
            if not rebuilt.is_file():
                missing.append(name)
            elif rebuilt.read_bytes() != blob:
                differing.append(name)
        if missing:
            emit(CID, FAIL,
                 "%s did not write %s again, so %s is not generated from "
                 "tokens/tokens.json"
                 % (label, ", ".join(missing[:3]), missing[0]))
        if differing:
            emit(CID, FAIL,
                 "a fresh build from tokens/tokens.json differs from the "
                 "committed output in %s" % ", ".join(differing[:3]))

        emit(CID, PASS,
             "%d tokens validate as DTCG; %d generated file(s) across %s "
             "reproduce byte for byte from the source via %s"
             % (len(tokens), len(before), ", ".join(platforms), label))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
