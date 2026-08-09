#!/usr/bin/env python3
"""Criterion 2: the behaviour pin holds on both sides, and actually pins.

A pin is a test that reads the fixture's `golden_input.txt`, calls
`parse_records` and asserts the output the code gave before anyone
touched it. Two halves, and the graders used to check one.

The half that was there: the test has to pass in the delivered tree and
at the fixture commit, because a pin that only passes on one side is not
pinning anything. Candidates are read out of the delivered tests rather
than guessed at, then run by node id in the delivered tree and again in
a tree unpacked from the fixture commit, with the delivered tests copied
beside the fixture code and nothing else copied.

The half that was missing: passing in both trees is also what a test
that asserts nothing does. So the fixture tree is then rebuilt with the
parsed output deliberately changed, by putting one more well-formed row
at the top of `golden_input.txt` and by bumping every number
`parse_records` returns, and the pin is run once more. It has to fail
there. A test that still passes when the records come back different is
not asserting the output of anything, whatever it is named, and it would
have let a rewrite of the well-formed path through untouched.

The mutation is applied to a throwaway copy of the fixture commit. The
delivered tree is never written to.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tests_into, emit,  # noqa: E402
                     fixture_tree, has_history, node_ids, require_git,
                     require_pytest, run_one, scratch_dir, test_files)

CID = "c2"

RAISE_MARKERS = ("raises", "assertRaises", "except ")

COLLECTION_TROUBLE = ("found no collectors", "during collection",
                      "ImportError", "ModuleNotFoundError")

EXTRA_ROW = "2024-03-31 | Depot | 42.5 | kWh"

# Appended to the fixture's parser.py in the mutant copy only. It leaves
# the module importable and every record different.
BUMP = '''

# Added by the drill grader to a throwaway copy of the fixture, to see
# whether the pin notices that parse_records returns different records.
_drill_inner_parse_records = parse_records


def parse_records(*args, **kwargs):
    result = _drill_inner_parse_records(*args, **kwargs)
    try:
        items = list(result)
    except TypeError:
        return result
    for item in items:
        if not isinstance(item, dict):
            continue
        for key, value in list(item.items()):
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                item[key] = value + 1
    return items
'''


def why_not(output):
    """Say plainly when the module, not the assertion, is what broke."""
    if any(marker in output for marker in COLLECTION_TROUBLE):
        return ("the test module does not import at the fixture commit, so "
                "the pin cannot be run there. A pin that only exists once "
                "the change is in place is not pinning the old behaviour; "
                "keep it in a module that imports against either tree")
    return " ".join(output.split())[-220:]


def candidates(scratch):
    found = []
    for node_id, file_text, source in node_ids(scratch):
        if "parse_records" not in source and "parse_records" not in file_text:
            continue
        if "golden_input" not in file_text:
            continue
        if any(marker in source for marker in RAISE_MARKERS):
            continue
        found.append(node_id)
    return found


def mutate(tree, dest):
    """A copy of the fixture tree whose parsed output is different."""
    mutant = Path(dest) / "mutant"
    if mutant.exists():
        shutil.rmtree(mutant, ignore_errors=True)
    shutil.copytree(tree, mutant)
    touched = []
    for path in mutant.rglob("golden_input.txt"):
        text = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(EXTRA_ROW + "\n" + text, encoding="utf-8")
        touched.append("one more row in golden_input.txt")
        break
    for path in mutant.rglob("parser.py"):
        if "__pycache__" in path.parts:
            continue
        with path.open("a", encoding="utf-8") as handle:
            handle.write(BUMP)
        touched.append("every number in the records moved by one")
        break
    return mutant, " and ".join(touched)


def main():
    scratch = scratch_dir()
    require_pytest(CID)
    require_git(CID)

    if not test_files(scratch):
        emit(CID, FAIL, "no test file in the delivered tree")
    pins = candidates(scratch)
    if not pins:
        emit(CID, FAIL,
             "no test reads golden_input.txt and calls parse_records without "
             "asserting a raise, so nothing pins the pre-change behaviour")
    if not has_history(scratch):
        emit(CID, FAIL,
             "the delivered tree has no git history, so the fixture commit "
             "cannot be recovered to run the pin against")

    work = Path(tempfile.mkdtemp(prefix="drill-coding-c2-"))
    try:
        tree, why = fixture_tree(scratch, work)
        if tree is None:
            emit(CID, FAIL, why)
        copy_tests_into(scratch, tree)
        mutant, changed = mutate(tree, work)

        misses = []
        for node_id in pins:
            here, out_here = run_one(scratch, node_id)
            if not here:
                misses.append("%s fails in the delivered tree" % node_id)
                continue
            there, out_there = run_one(tree, node_id)
            if not there:
                misses.append(
                    "%s passes in the delivered tree but fails at the %s: %s"
                    % (node_id, why, why_not(out_there)))
                continue
            blind, _ = run_one(mutant, node_id)
            if blind:
                misses.append(
                    "%s passes at the %s even with %s, so it does not assert "
                    "what parse_records returns for golden_input.txt and pins "
                    "nothing" % (node_id, why, changed))
                continue
            emit(CID, PASS,
                 "%s asserts the golden_input.txt output, passes both in the "
                 "delivered tree and at the %s, and fails when the same "
                 "fixture is changed so that %s"
                 % (node_id, why, changed))
        emit(CID, FAIL, "; ".join(misses[:3]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
