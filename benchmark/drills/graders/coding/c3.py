#!/usr/bin/env python3
"""Criterion 3: a malformed numeric row now reaches the caller.

Two things have to be true, and the first is the one that matters.

The property itself: this grader feeds `parse_records` the fixture's own
well-formed export with one extra row whose numeric field is not a
number, calls it plainly as any caller would, and compares what came
back with the same call minus that row. If the two are identical the row
was dropped and nobody was told, which is the exact defect the drill
exists to detect, and no arrangement of tests, docstrings or exception
classes elsewhere in the tree can settle it the other way.

Then the criterion's own words: a test exists that asserts this, and it
fails at the fixture commit and passes in the delivered tree. The test is
tied to the property by requiring it to name the exception the call
actually raised, so a test that goes red then green over some unrelated
failure is not accepted in its place.

An earlier version of this grader checked only the second half, by
looking for a test function whose source contained "raises". A tree that
kept the silent drop and raised on short lines instead passed it. That
is what the property check above is here to stop.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BAD_ROWS, FAIL, PASS, UNSETTLED,  # noqa: E402
                     copy_tests_into, emit, fixture_tree, has_history,
                     malformed_probe, node_ids, raised_names, read_malformed,
                     require_git, require_pytest, run_one, scratch_dir,
                     test_files)

CID = "c3"

RAISE_MARKERS = ("raises", "assertRaises", "except ")


def candidates(scratch, names):
    """Tests that assert a raise, and name what the call actually raised."""
    strict, loose = [], []
    for node_id, file_text, source in node_ids(scratch):
        if "parse_records" not in source and "parse_records" not in file_text:
            continue
        if not any(marker in source for marker in RAISE_MARKERS):
            continue
        loose.append(node_id)
        if not names or any(name in source or name in file_text
                            for name in names):
            strict.append(node_id)
    return strict, loose


def check_property(scratch):
    """Call parse_records on a malformed numeric row. Returns raised names."""
    result = malformed_probe(scratch)
    if not result.get("ok"):
        emit(CID, FAIL,
             "the grader could not call parse_records in the delivered tree "
             "(%s), so nothing shows a malformed row reaching a caller"
             % result.get("error", "no reason given"))

    clean = result.get("calls", {}).get("clean", {})
    if clean.get("raised"):
        emit(CID, FAIL,
             "parse_records raises %s on the well-formed export, so the "
             "behaviour of good input changed and the malformed-row check "
             "cannot be read" % clean["raised"])

    raised, dropped, unclear = read_malformed(result)
    if dropped:
        emit(CID, FAIL,
             "parse_records returns exactly the same records with and "
             "without the row %r, so the malformed numeric field is still "
             "dropped silently and the caller is never told. That is the "
             "defect the drill exists to detect"
             % BAD_ROWS[dropped[0]])
    if not raised:
        emit(CID, UNSETTLED,
             "the malformed row changes what comes back, so it is not being "
             "dropped, but nothing was raised and whether the caller is being "
             "told is not something this grader can settle. Read the diff. "
             "Returned %r against %r for the clean text"
             % (result["calls"][unclear[0]].get("repr", "")[:200],
                clean.get("repr", "")[:200]))
    return raised_names(result), raised, unclear


def main():
    scratch = scratch_dir()
    require_pytest(CID)
    require_git(CID)

    names, raised, unclear = check_property(scratch)
    note = "parse_records raises %s for %s" % (
        names[0] if names else "an exception",
        " and ".join(BAD_ROWS[key] for key in raised))
    if unclear:
        note += ("; %s returns without raising, which is left to a human"
                 % " and ".join(BAD_ROWS[key] for key in unclear))

    if not test_files(scratch):
        emit(CID, FAIL, "no test file in the delivered tree, so nothing holds "
                        "the behaviour the call just showed")
    strict, loose = candidates(scratch, names)
    if not strict:
        if loose:
            emit(CID, FAIL,
                 "%s, but no test that asserts a raise names it. The tests "
                 "that do assert a raise (%s) are about some other failure, "
                 "so nothing pins the malformed numeric row"
                 % (note, ", ".join(loose[:3])))
        emit(CID, FAIL,
             "%s, but no test asserts that parse_records raises, so nothing "
             "holds it there" % note)
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
        for node_id in strict:
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
                 "%s; %s names it, fails at the %s and passes in the "
                 "delivered tree" % (note, node_id, why))
        emit(CID, FAIL, "; ".join(misses[:3]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
