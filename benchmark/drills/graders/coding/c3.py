#!/usr/bin/env python3
"""Criterion 3: a test that goes red at the fixture and green at the end.

The drill asks for a test asserting that a malformed numeric row now
reaches the caller as an error. The half a machine can settle is the
direction of travel: the test must fail against the fixture commit and
pass against the delivered tree. A test that passes at the fixture
commit is asserting behaviour that was already there, and a test that
fails at the end is not evidence of anything.

Candidates are module level test functions that name `parse_records`
and assert a raise, which is a shape check, not a reading of what the
assertion means. Whether the row it feeds is genuinely a malformed
numeric field is left to the human reading the diff.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tests_into, emit,  # noqa: E402
                     fixture_tree, has_history, node_ids, require_git,
                     require_pytest, run_one, scratch_dir, test_files)

CID = "c3"

RAISE_MARKERS = ("raises", "assertRaises", "except ")


def candidates(scratch):
    found = []
    for node_id, file_text, source in node_ids(scratch):
        if "parse_records" not in source and "parse_records" not in file_text:
            continue
        if not any(marker in source for marker in RAISE_MARKERS):
            continue
        found.append(node_id)
    return found


def main():
    scratch = scratch_dir()
    require_pytest(CID)
    require_git(CID)

    if not test_files(scratch):
        emit(CID, FAIL, "no test file in the delivered tree")
    error_tests = candidates(scratch)
    if not error_tests:
        emit(CID, FAIL,
             "no test asserts that parse_records raises, so nothing checks "
             "that a malformed row now reaches the caller")
    if not has_history(scratch):
        emit(CID, FAIL,
             "the delivered tree has no git history, so the fixture commit "
             "cannot be recovered to run the new test against")

    work = Path(tempfile.mkdtemp(prefix="drill-coding-c3-"))
    try:
        tree, why = fixture_tree(scratch, work)
        if tree is None:
            emit(CID, FAIL, why)
        copy_tests_into(scratch, tree)

        misses = []
        for node_id in error_tests:
            here, out_here = run_one(scratch, node_id)
            if not here:
                misses.append("%s fails in the delivered tree: %s"
                              % (node_id, " ".join(out_here.split())[-180:]))
                continue
            there, _ = run_one(tree, node_id)
            if there:
                misses.append(
                    "%s passes at the %s as well, so it is not evidence of a "
                    "change" % (node_id, why))
                continue
            emit(CID, PASS,
                 "%s fails at the %s and passes in the delivered tree"
                 % (node_id, why))
        emit(CID, FAIL, "; ".join(misses[:3]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
