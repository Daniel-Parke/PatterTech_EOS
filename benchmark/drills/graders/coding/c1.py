#!/usr/bin/env python3
"""Criterion 1: an oracle existed before the implementation landed.

The fixture arrives as the root commit of the scratch repository, so
that commit is the starting line and never counts as the agent's work.
Everything after it is read in order: the first commit that touches
`parser.py` must have a commit adding a test file somewhere ahead of it.
One commit carrying both the test and the change fails, which is the
point of the criterion.

The order of the commits is only the visible half. The criterion says
the run fails "if implementation lands before any oracle exists", and an
empty file named `test_parser.py` is not an oracle: it is a filename
that satisfies a check. So the earlier commit is unpacked and its tests
are run there, at that commit, with nothing from later in the history
copied in. At least one test that calls `parse_records` has to pass in
that tree. A test that is red at that point is not held against the
agent, because writing the failing test first is the practice this
criterion is trying to reward, but something has to be green or nothing
was pinned.

That needs pytest as well as git. Where either is missing the criterion
is left unsettled rather than guessed at.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, commit_files, commits, emit,  # noqa: E402
                     has_history, is_test_file, node_ids, require_git,
                     require_pytest, root_commit, run_one, scratch_dir,
                     tree_at)

CID = "c1"


def oracle_runs(scratch, sha, added):
    """Run the tests as they stood at `sha`. Returns (ok, note)."""
    work = Path(tempfile.mkdtemp(prefix="drill-coding-c1-"))
    try:
        tree, why = tree_at(scratch, sha, work, name="oracle")
        if tree is None:
            return False, why
        found = [(node_id, text) for node_id, text, _ in node_ids(tree)
                 if "parse_records" in text]
        if not found:
            return False, ("the test file %s carries no test function that "
                           "calls parse_records at %s, so it is a filename "
                           "rather than an oracle" % (added, sha[:8]))
        for node_id, _ in found:
            passed, _ = run_one(tree, node_id)
            if passed:
                return True, "%s passes at %s" % (node_id, sha[:8])
        return False, ("none of the %d test(s) calling parse_records pass at "
                       "%s, so nothing was pinned before parser.py changed"
                       % (len(found), sha[:8]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    scratch = scratch_dir()
    require_git(CID)
    require_pytest(CID)
    if not has_history(scratch):
        emit(CID, FAIL,
             "the delivered tree has no git history, so there is no commit "
             "order to read")

    history = commits(scratch)
    if len(history) < 2:
        emit(CID, FAIL,
             "git log shows %d commit(s); the criterion asks for at least "
             "two" % len(history))

    root = root_commit(scratch)
    work = [sha for sha in history if sha != root]
    if not work:
        emit(CID, FAIL,
             "every commit is a root commit, so nothing was committed on top "
             "of the fixture")

    touched_parser = None
    added_test = None
    for index, sha in enumerate(work):
        rows = commit_files(scratch, sha)
        paths = [path for _, path in rows]
        if added_test is None:
            for status, path in rows:
                if status.startswith("A") and is_test_file(path):
                    added_test = (index, sha, path)
                    break
        if touched_parser is None:
            for path in paths:
                if Path(path).name == "parser.py":
                    touched_parser = (index, sha, path)
                    break
        if touched_parser is not None:
            break

    if touched_parser is None:
        emit(CID, FAIL,
             "no commit after the fixture commit touches parser.py, so the "
             "change the prompt asked for was never committed")
    if added_test is None:
        emit(CID, FAIL,
             "the first commit touching parser.py (%s) is not preceded by "
             "any commit that adds a test file: the implementation landed "
             "before an oracle existed"
             % touched_parser[1][:8])
    if added_test[0] >= touched_parser[0]:
        emit(CID, FAIL,
             "the test file %s and the parser.py change arrived in the same "
             "commit %s, so no oracle existed before the change"
             % (added_test[2], touched_parser[1][:8]))

    ok, note = oracle_runs(scratch, added_test[1], added_test[2])
    if not ok:
        emit(CID, FAIL,
             "%s lands before parser.py is touched in %s, but %s"
             % (added_test[2], touched_parser[1][:8], note))

    emit(CID, PASS,
         "%d commits; %s adds %s and %s, and parser.py is first touched later "
         "in %s" % (len(history), added_test[1][:8], added_test[2], note,
                    touched_parser[1][:8]))


if __name__ == "__main__":
    main()
