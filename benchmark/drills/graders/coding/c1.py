#!/usr/bin/env python3
"""Criterion 1: the oracle commit lands before the implementation commit.

The fixture arrives as the root commit of the scratch repository, so
that commit is the starting line and never counts as the agent's work.
Everything after it is read in order: the first commit that touches
`parser.py` must have a commit adding a test file somewhere ahead of
it. One commit carrying both the test and the change fails, which is
the point of the criterion.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, commit_files, commits, emit,  # noqa: E402
                     has_history, is_test_file, require_git, root_commit,
                     scratch_dir)

CID = "c1"


def main():
    scratch = scratch_dir()
    require_git(CID)
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

    emit(CID, PASS,
         "%d commits; %s adds %s, and parser.py is first touched later in %s"
         % (len(history), added_test[1][:8], added_test[2],
            touched_parser[1][:8]))


if __name__ == "__main__":
    main()
