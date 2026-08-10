#!/usr/bin/env python3
"""Criterion 9: the run itself. Two clauses of four can be read here.

The criterion asks for at least one commit, nothing under `drills/`
modified, under twenty minutes, and criteria 1 to 8 run with no
network. The first two are properties of the delivered tree and this
grader reads them. The last two are properties of the session that
produced it: how long the agent took, and whether it reached the
network. No inspection of a tree can settle either.

So this grader never passes. It fails when a clause it can read is
broken, and otherwise takes the third exit with the two unread clauses
named, which the runner records as manual. A pass here would claim the
stopwatch and the network log were looked at, and they were not.

That is not a gap to paper over. It is the honest shape of a criterion
that mixes what the tree shows with what only the harness saw.
"""

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, UNSETTLED, emit, scratch_dir  # noqa: E402

CID = "c9"

BASELINE = "drill baseline"


def git(scratch, *args):
    try:
        proc = subprocess.run(["git", "-C", str(scratch), *args],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main():
    scratch = scratch_dir()
    if not shutil.which("git"):
        emit(CID, UNSETTLED,
             "no git on this machine, so neither the commits nor the paths "
             "they touched could be read")
    if not (Path(scratch) / ".git").exists():
        emit(CID, FAIL,
             "the delivered tree is not a git repository, so there is no "
             "commit")

    code, out = git(scratch, "log", "--format=%H%x09%s")
    if code != 0:
        emit(CID, FAIL, "no commit in the delivered tree: %s"
                        % " ".join(out.split())[:120])
    rows = [line.split("\t", 1) for line in out.splitlines() if line.strip()]
    work = [r for r in rows if len(r) == 2 and r[1].strip() != BASELINE]
    if not work:
        emit(CID, FAIL,
             "%d commit(s) in the tree and every one of them is the drill "
             "baseline, so the agent committed nothing" % len(rows))

    touched = set()
    for sha, _ in work:
        code, out = git(scratch, "show", "--name-only", "--format=", sha)
        if code != 0:
            continue
        for line in out.splitlines():
            line = line.strip().replace("\\", "/")
            if line.startswith("drills/") or "/drills/" in line:
                touched.add(line)
    if touched:
        emit(CID, FAIL,
             "%d path(s) under drills/ were modified: %s"
             % (len(touched), ", ".join(sorted(touched)[:5])))

    emit(CID, UNSETTLED,
         "%d commit(s) beyond the baseline and nothing under drills/ was "
         "touched. The other two clauses, under twenty minutes and criteria "
         "1 to 8 run with no network, are properties of the session rather "
         "than of the tree, and no reading of the tree settles them, so this "
         "criterion is left for the harness record" % len(work))


if __name__ == "__main__":
    main()
