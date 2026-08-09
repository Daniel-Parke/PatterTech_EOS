#!/usr/bin/env python3
"""Criterion 2: the check is green now and red on the original docs.

A link checker that never goes red is a green badge, so this grader
runs the project's own invocation twice over: once on the delivered
tree, where it must exit 0, and once for each page the fixture broke,
with that page put back as it was, where it must exit non-zero.

The regression is built by restoring the frozen fixture's Markdown on
top of a copy of the delivered tree, so the checker and its
configuration are the ones the agent wrote and only the prose goes back
in time. Running the checker against a bare copy of the fixture would
prove nothing: it would fail because the tooling is missing.

Page by page rather than all at once, because the two planted faults
are different kinds. One is a link to a file that does not exist, which
any checker catches. The other is a link to a heading that no longer
exists, which only a checker configured for fragments catches. Put both
back together and the first fault alone turns the run red, and a
checker blind to anchors passes a criterion that exists to require
them. A restored page whose links happen to resolve in the delivered
tree is skipped rather than failed: an agent who really did create the
missing page has not left the link broken.

Where the declared checker is a third-party binary or a hosted action
this machine cannot run, the criterion is settled on substance instead,
with the fragment-aware checker in `_common`, and the reason says so.
What that substitution cannot see is a checker configured to skip the
files that carry the faults; what it can see, and what the drill is
about, is whether both broken links are actually fixed.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, broken_links,  # noqa: E402
                     checker_actions, emit, expand_make, frozen_fixture,
                     link_check_commands, looks_like_missing_tool,
                     markdown_files, one_line, rel, run_command, scratch_dir)

CID = "c2"


def restore(scratch, fixture, dest, only=None):
    """A copy of the delivered tree with the original Markdown put back."""
    shutil.copytree(scratch, dest)
    restored = []
    for path in markdown_files(fixture):
        where = rel(fixture, path)
        if only is not None and where != only:
            continue
        target = dest / where
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        restored.append(where)
    return restored


def defect_pages(fixture):
    """Fixture pages carrying a broken link, with what is broken."""
    pages = {}
    for problem in broken_links(fixture):
        page = problem.split(":", 1)[0]
        pages.setdefault(page, []).append(problem)
    return pages


def run_all(commands, tree):
    """Run every link-checking command in `tree`."""
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
    actions = checker_actions(scratch)
    if not commands and not actions:
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
        results, unrunnable = run_all(commands, now) if commands else ([], [])

        if results:
            bad = [(c, code, out) for c, code, out in results if code != 0]
            if bad:
                if looks_like_missing_tool(bad[0][2]):
                    emit(CID, UNSETTLED,
                         "the project's link check cannot run on this "
                         "machine: %r exits %d, %s"
                         % (bad[0][0], bad[0][1], one_line(bad[0][2])))
                emit(CID, FAIL,
                     "the project's own link check fails on the delivered "
                     "tree: %r exits %d, %s"
                     % (bad[0][0], bad[0][1], one_line(bad[0][2])))

            caught, missed, skipped = [], [], []
            for i, (page, problems) in enumerate(
                    sorted(defect_pages(fixture).items())):
                copy = work / ("before-%d" % i)
                restore(scratch, fixture, copy, only=page)
                still = [p for p in broken_links(copy)
                         if p.startswith(page + ":")]
                if not still:
                    skipped.append(page)
                    continue
                red, _ = run_all(commands, copy)
                failing = [(c, code) for c, code, _ in red if code != 0]
                if failing:
                    caught.append((page, failing[0][1]))
                else:
                    missed.append((page, still[0]))

            if missed:
                emit(CID, FAIL,
                     "the link check exits 0 with the original %s restored, "
                     "so it does not catch %s and would not catch it coming "
                     "back" % (missed[0][0], missed[0][1]))
            if not caught:
                emit(CID, FAIL,
                     "the link check is green on the delivered tree, but "
                     "restoring the original documentation (%s) leaves "
                     "nothing for it to catch, so it was never shown to go "
                     "red" % (", ".join(skipped) or "nothing was restored"))
            emit(CID, PASS,
                 "the link check exits 0 on the delivered tree and exits "
                 "non-zero on each original page that was broken: %s"
                 % ", ".join("%s (exit %d)" % (p, c) for p, c in caught))

        # Nothing runnable here. Settle the substance and say so.
        if unrunnable:
            why = unrunnable[0][1]
        elif actions:
            why = "the check is a hosted action, %s" % actions[0][1]
        else:
            why = "nothing to run"
        before = work / "before-all"
        restored = restore(scratch, fixture, before)
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
                 "either (%s restored), so it is not a trustworthy stand-in"
                 % (why, ", ".join(restored[:4])))
        emit(CID, PASS,
             "the declared checker could not be run here (%s), so this was "
             "settled on substance: every relative link and fragment in the "
             "delivered tree resolves, and the same check finds %d "
             "breakage(s) with the original documentation restored (%s)"
             % (why, len(before_problems), "; ".join(before_problems[:2])))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
