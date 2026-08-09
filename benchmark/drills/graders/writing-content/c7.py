#!/usr/bin/env python3
"""Criterion 7: CI checks the terminology, and the check has teeth.

The point is not that the words were made consistent once. It is that
a step in CI would catch the next drift, so the grader proves the check
both ways.

- read the commands CI runs. Installs and anything that fetches are
  skipped, both because criterion 9 forbids the network and because a
  package install is not a check;
- run them against a copy of the delivered tree, and keep the ones that
  pass;
- take another copy, put `log in` into the catalogue where the tree
  says sign in, and run the passing commands again;
- at least one of them must now fail.

A step that passes both times is a step that reads nothing. A tree with
a terminology document and no step fails here, which is the separation
the criterion is for.

If no command could be started at all, because the interpreter it needs
is not on this machine, the grader takes the third exit rather than
reporting the tree as broken.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, base_catalogue,  # noqa: E402
                     ci_commands, ci_files, copy_tree, emit, inject,
                     looks_missing, owns_script, plain_keys, rel,
                     run_command, scratch_dir)

CID = "c7"

SIGN_IN = re.compile(r"sign[\s\-]?in", re.I)
FALLBACK = "Log in to your account"


def injected_value(flat):
    """The catalogue edit: `log in` where the tree says sign in."""
    for key in sorted(flat):
        if SIGN_IN.search(flat[key]):
            return key, SIGN_IN.sub("Log in", flat[key], count=1)
    plain = sorted(plain_keys(flat), key=lambda k: -len(flat[k]))
    if not plain:
        return None, None
    return plain[0], FALLBACK


def main():
    scratch = scratch_dir()
    _, cat_path, flat = base_catalogue(scratch)
    if flat is None:
        emit(CID, FAIL, "no message catalogue found to check")

    configs = ci_files(scratch)
    commands = ci_commands(scratch)
    if not configs:
        emit(CID, FAIL, "no CI configuration in the tree")
    if not commands:
        emit(CID, FAIL,
             "%s run(s) nothing but installs, so no step checks the words"
             % ", ".join(rel(scratch, c) for c in configs))

    key, value = injected_value(flat)
    if key is None:
        emit(CID, FAIL,
             "every message in %s carries a placeholder, so the grader has "
             "nowhere to put the injected term" % rel(scratch, cat_path))

    dest, tree = copy_tree(scratch)
    try:
        clean = []
        stalled = []
        for source, cmd in commands:
            code, output = run_command(tree, cmd)
            if code == 0:
                clean.append((source, cmd))
            elif (code is None or looks_missing(output)) and \
                    owns_script(scratch, cmd):
                stalled.append(cmd)
        if not clean:
            if stalled:
                emit(CID, UNSETTLED,
                     "%d CI command(s) drive a checker this tree ships and "
                     "could not be started on this machine, so the criterion "
                     "was not settled here: %s"
                     % (len(stalled), "; ".join(stalled)[:160]))
            emit(CID, FAIL,
                 "no CI command passes on the delivered tree, so nothing "
                 "there is a check that holds: %s"
                 % "; ".join(c for _, c in commands)[:200])
    finally:
        shutil.rmtree(str(dest), ignore_errors=True)

    dest, tree = copy_tree(scratch)
    try:
        target = Path(tree) / Path(cat_path).relative_to(scratch)
        if not inject(target, key, value):
            emit(CID, FAIL,
                 "could not rewrite %s in %s to inject the term"
                 % (key, rel(scratch, cat_path)))
        flipped = []
        for source, cmd in clean:
            code, _ = run_command(tree, cmd)
            if code != 0:
                flipped.append((source, cmd))
    finally:
        shutil.rmtree(str(dest), ignore_errors=True)

    if not flipped:
        emit(CID, FAIL,
             "%d CI command(s) pass on the tree and every one of them still "
             "passes with %r in %s, so none of them checks the terminology: "
             "%s" % (len(clean), value[:40], key,
                     "; ".join(c for _, c in clean)[:200]))

    emit(CID, PASS,
         "%s in %s passes on the delivered tree and fails once %r is put in "
         "%s" % (flipped[0][1], flipped[0][0], value[:40], key))


if __name__ == "__main__":
    main()
