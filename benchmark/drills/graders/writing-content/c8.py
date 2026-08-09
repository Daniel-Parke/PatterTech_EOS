#!/usr/bin/env python3
"""Criterion 8: no readability score gates anything.

The one criterion that fails a tree for doing too much. A long sentence
is a matter for an editor, and a pipeline that blocks a merge on a
grade level has turned taste into a gate.

Two assertions:

- nothing wired into a check is a readability scorer, by name;
- a forty-word sentence put into the catalogue in place of an ordinary
  message must not turn any passing check red. The sentence carries no
  banned term, no placeholder and no markup, so anything that fails on
  it is failing on its length.

The sentence replaces an existing message rather than adding a key, so
a completeness check comparing catalogues is not tripped by the
injection itself and blamed on the length.

A tree with no checks at all fails here. The criterion is about which
signals block and which do not, and a tree that gates nothing has not
answered the question; it has skipped it. That reading is deliberate
and is the reason this grader also fails an untouched fixture.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, base_catalogue,  # noqa: E402
                     ci_commands, ci_files, copy_tree, emit, inject,
                     looks_missing, owns_script, plain_keys, read, rel,
                     run_command, scratch_dir)

CID = "c8"

SENTENCE = (
    "We keep a record of every basket you leave behind so that when you "
    "come back to the shop on another day of the week the things you liked "
    "are still there waiting for you and nothing needs finding twice")

SCORERS = re.compile(
    r"textstat|flesch|kincaid|hemingway|gunning|fog[-_ ]?index|smog|"
    r"coleman[-_ ]?liau|dale[-_ ]?chall|retext-readability|readability|"
    r"reading[-_ ]?(level|ease|grade)|grade[-_ ]?level|syllable", re.I)


def main():
    scratch = scratch_dir()
    _, cat_path, flat = base_catalogue(scratch)
    if flat is None:
        emit(CID, FAIL, "no message catalogue found")

    words = len(SENTENCE.split())
    if words != 40:
        emit(CID, FAIL,
             "the grader's own sentence is %d words, not forty; fix the "
             "grader before reading anything into this" % words)

    configs = ci_files(scratch)
    commands = ci_commands(scratch)
    if not commands:
        emit(CID, FAIL,
             "no check runs in this tree, so nothing was proved about what "
             "gates a merge. This criterion is answered by the checks the "
             "tree adds, and there are none")

    named = []
    for source, cmd in commands:
        if SCORERS.search(cmd):
            named.append("a CI step runs %s" % cmd)
    for path in list(configs) + [Path(scratch) / "package.json"]:
        if not Path(path).is_file():
            continue
        text = read(path)
        for match in SCORERS.finditer(text):
            named.append("%s names %s" % (rel(scratch, path), match.group(0)))
    if named:
        unique = sorted(set(named))
        emit(CID, FAIL,
             "%d readability scorer reference(s) in the pipeline: %s"
             % (len(unique), "; ".join(unique[:4])))

    plain = sorted(plain_keys(flat), key=lambda k: -len(flat[k]))
    if not plain:
        emit(CID, FAIL,
             "every message in %s carries a placeholder, so the sentence "
             "has nowhere to go" % rel(scratch, cat_path))
    key = plain[0]

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
    finally:
        shutil.rmtree(str(dest), ignore_errors=True)

    if not clean:
        if stalled:
            emit(CID, UNSETTLED,
                 "%d CI command(s) drive a checker this tree ships and could "
                 "not be started here, so nothing could be run with the "
                 "sentence in it: %s"
                 % (len(stalled), "; ".join(stalled)[:160]))
        emit(CID, FAIL,
             "no CI command passes on the delivered tree, so the tree has no "
             "working check for the sentence to be measured against")

    dest, tree = copy_tree(scratch)
    try:
        target = Path(tree) / Path(cat_path).relative_to(scratch)
        if not inject(target, key, SENTENCE):
            emit(CID, FAIL,
                 "could not rewrite %s in %s" % (key, rel(scratch, cat_path)))
        broke = []
        for source, cmd in clean:
            code, output = run_command(tree, cmd)
            if code != 0:
                broke.append("%s now fails: %s"
                             % (cmd, " ".join(output.split())[:120]))
    finally:
        shutil.rmtree(str(dest), ignore_errors=True)

    if broke:
        emit(CID, FAIL,
             "a forty-word sentence in %s turns %d passing check(s) red: %s"
             % (key, len(broke), "; ".join(broke[:3])))

    emit(CID, PASS,
         "no readability scorer is wired into the pipeline, and a forty-word "
         "sentence in %s leaves all %d passing check(s) green"
         % (key, len(clean)))


if __name__ == "__main__":
    main()
