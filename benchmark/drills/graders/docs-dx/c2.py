#!/usr/bin/env python3
"""Criterion 2: the check is green now and red on the original docs.

A link checker that never goes red is a green badge, so this grader
runs the project's own invocation twice: once over the delivered tree,
where it must exit 0, and once over the same tree with the original
documentation put back, where it must exit non-zero. The second run is
built by restoring the frozen fixture's Markdown on top of a copy of
the delivered tree, so the checker and its configuration are the ones
the agent wrote and only the prose goes back in time. Running the
checker against a bare copy of the fixture would prove nothing: it
would fail because the tooling is missing.

Where the declared checker is a third-party binary this machine does
not have, the criterion is settled on substance instead, with a small
fragment-aware checker in `_common`, and the reason says so. What that
substitution cannot see is a checker configured to skip the files that
carry the faults; what it can see, and what the drill is about, is
whether both broken links are actually fixed.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, broken_links, emit,  # noqa: E402
                     expand_make, frozen_fixture, link_check_commands,
                     markdown_files, one_line, rel, run_command, scratch_dir)

CID = "c2"


def regressed(scratch, fixture, dest):
    """A copy of the delivered tree with the original Markdown restored."""
    shutil.copytree(scratch, dest)
    restored = []
    for path in markdown_files(fixture):
        target = dest / path.relative_to(fixture)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        restored.append(rel(fixture, path))
    return restored


def run_all(commands, tree):
    """Returns (ran, results) where results is [(command, code, output)]."""
    results, unrunnable = [], []
    for _, command, _ in commands:
        for piece in expand_make(tree, command):
            code, output = run_command(piece, tree)
            if code is None:
                unrunnable.append((piece, output))
            else:
                results.append((piece, code, output))
    return results, unrunnable


def main():
    scratch = scratch_dir()
    commands = link_check_commands(scratch)
    if not commands:
        emit(CID, FAIL,
             "no link-checking step in the tree, so there is no invocation "
             "to run; criterion 1 covers that and this one cannot run "
             "without it")

    fixture = frozen_fixture()
    if fixture is None:
        emit(CID, UNSETTLED,
             "the frozen scenario is not next to the graders, so the "
             "before-and-after halves of this criterion cannot be compared")

    work = Path(tempfile.mkdtemp(prefix="drill-docsdx-c2-"))
    try:
        now = work / "now"
        shutil.copytree(scratch, now)
        before = work / "before"
        restored = regressed(scratch, fixture, before)

        green, unrunnable = run_all(commands, now)
        if green:
            bad = [(c, code, out) for c, code, out in green if code != 0]
            if bad:
                emit(CID, FAIL,
                     "the project's own link check fails on the delivered "
                     "tree: %r exits %d, %s"
                     % (bad[0][0], bad[0][1], one_line(bad[0][2])))
            red, _ = run_all(commands, before)
            failed = [(c, code) for c, code, _ in red if code != 0]
            if not failed:
                emit(CID, FAIL,
                     "the link check exits 0 with the original documentation "
                     "restored (%s), so it does not catch the two links the "
                     "fixture broke and would not catch them coming back"
                     % ", ".join(restored[:4]))
            emit(CID, PASS,
                 "%r exits 0 on the delivered tree and exits %d with the "
                 "original documentation restored"
                 % (failed[0][0], failed[0][1]))

        # Nothing runnable here. Settle the substance and say so.
        why = unrunnable[0][1] if unrunnable else "nothing to run"
        now_problems = broken_links(now)
        before_problems = broken_links(before)
        if now_problems:
            emit(CID, FAIL,
                 "%d link(s) in the delivered tree still do not resolve: %s"
                 % (len(now_problems), "; ".join(now_problems[:3])))
        if not before_problems:
            emit(CID, UNSETTLED,
                 "the declared checker could not be run here (%s) and the "
                 "substitute finds no fault in the original documentation "
                 "either, so it is not a trustworthy stand-in" % why)
        emit(CID, PASS,
             "the declared checker could not be run here (%s), so this was "
             "settled on substance: every relative link and fragment in the "
             "delivered tree resolves, and the same check finds %d breakage(s) "
             "with the original documentation restored (%s)"
             % (why, len(before_problems), "; ".join(before_problems[:2])))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
