#!/usr/bin/env python3
"""Criterion 6: every commit the agent made carries a sign-off.

`git log --format=%B` over the delivered history, one commit at a time.
The harness's own baseline commit is not the agent's work and is not
held to this; every other commit is, and a history with nothing but the
baseline fails, because a criterion about habit cannot be satisfied
vacuously.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, git, has_history,  # noqa: E402
                     require_git, scratch_dir)

CID = "c6"

SIGN_OFF = re.compile(r"^Signed-off-by: .+ <.+@.+>$", re.M)
BASELINE_SUBJECTS = ("drill baseline",)
SEP = "\x1e"


def commits(scratch):
    """[(sha, subject, body)] over the whole delivered history."""
    code, out = git(scratch, "log", "--format=%H%x1f%s%x1f%B%x1e")
    if code != 0:
        return []
    rows = []
    for chunk in out.split(SEP):
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        parts = chunk.split("\x1f")
        if len(parts) < 3:
            continue
        rows.append((parts[0][:8], parts[1].strip(), parts[2]))
    return rows


def main():
    scratch = scratch_dir()
    require_git(CID)

    if not has_history(scratch):
        emit(CID, FAIL,
             "the delivered tree has no git history, so there is nothing for "
             "`git log` to show and no provenance was recorded")

    rows = commits(scratch)
    if not rows:
        emit(CID, FAIL, "`git log` returned no commits")

    theirs = [r for r in rows
              if r[1].lower() not in BASELINE_SUBJECTS]
    if not theirs:
        emit(CID, FAIL,
             "the only commit in the tree is the fixture baseline: the work "
             "was never committed, so no commit carries a sign-off")

    unsigned = [(sha, subject) for sha, subject, body in theirs
                if not SIGN_OFF.search(body)]
    if unsigned:
        emit(CID, FAIL,
             "%d of %d commit(s) carry no `Signed-off-by: name <address>` "
             "line: %s"
             % (len(unsigned), len(theirs),
                ", ".join("%s %r" % (sha, subject[:40])
                          for sha, subject in unsigned[:4])))

    emit(CID, PASS,
         "all %d commit(s) beyond the fixture baseline carry a sign-off"
         % len(theirs))


if __name__ == "__main__":
    main()
