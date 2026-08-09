#!/usr/bin/env python3
"""Criterion 2: the behaviour pin holds on both sides of the change.

A pin is a test that reads the fixture's `golden_input.txt`, calls
`parse_records` and asserts the output the code gave before anyone
touched it. It has to pass in the delivered tree and in the fixture
commit, because a pin that only passes on one side is not pinning
anything.

Candidates are read out of the delivered tests rather than guessed at:
a module level test function that names `parse_records`, sits in a file
that reaches for `golden_input`, and does not assert a raise. Each is
run by node id in the delivered tree and again in a tree unpacked from
the fixture commit, with the delivered tests copied beside the fixture
code and nothing else copied.
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
            emit(CID, PASS,
                 "%s asserts the golden_input.txt output and passes both in "
                 "the delivered tree and at the %s" % (node_id, why))
        emit(CID, FAIL, "; ".join(misses[:3]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
