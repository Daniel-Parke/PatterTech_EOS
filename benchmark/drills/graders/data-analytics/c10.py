#!/usr/bin/env python3
"""Criterion 10: the repository checker exits zero on the delivered tree.

The frozen spec names `python tools/eos_check.py --repo`. That checker
is the EOS's own, and it checks the repository it lives in: it resolves
its root from its own path and validates the front-matter law, the
indexes and the claims of an EOS-governed tree.

The scenario this drill materialises is not one. It is an ordinary
analytics repository with a raw export and a build script, deliberately
so, because a fixture carrying EOS metadata tells a cold agent it is
being tested. There is no checker in it to run and none the agent could
be expected to write.

So this grader runs the checker when the delivered tree carries one, and
otherwise leaves the criterion unsettled with that stated. Exit 2, which
the runner records as manual and never as a fail. Reporting "the tool is
not here" as "the work is wrong" would be a finding against a tree
nothing looked at, and the whole point of the third exit code is to
refuse that trade.
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, UNSETTLED, emit, scratch_dir  # noqa: E402

CID = "c10"

CHECKERS = (
    ("tools/eos_check.py", [sys.executable, "tools/eos_check.py", "--repo"]),
    ("tools/eos/__main__.py", [sys.executable, "-m", "tools.eos", "check",
                               "--repo"]),
)


def main():
    scratch = scratch_dir()
    for marker, argv in CHECKERS:
        if not (scratch / marker).is_file():
            continue
        env = dict(os.environ)
        env["PYTHONPATH"] = str(scratch) + os.pathsep + env.get("PYTHONPATH", "")
        try:
            proc = subprocess.run(argv, cwd=str(scratch), capture_output=True,
                                  text=True, encoding="utf-8",
                                  errors="replace", timeout=900, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            emit(CID, FAIL, "could not run %s: %s" % (" ".join(argv[1:]), exc))
        output = " ".join(((proc.stdout or "") + (proc.stderr or "")).split())
        if proc.returncode == 0:
            emit(CID, PASS,
                 "%s exits 0 on the delivered tree" % " ".join(argv[1:]))
        emit(CID, FAIL,
             "%s exits %d on the delivered tree: %s"
             % (" ".join(argv[1:]), proc.returncode, output[:300]))

    emit(CID, UNSETTLED,
         "the delivered tree carries no repository checker: the scenario is "
         "an ordinary analytics repository, not an EOS-governed one, so "
         "tools/eos_check.py is not in it and nothing the agent was asked "
         "for would put it there. The criterion was not settled here; that "
         "is a gap between the frozen spec and the fixture it grades, not a "
         "finding against the delivered tree.")


if __name__ == "__main__":
    main()
