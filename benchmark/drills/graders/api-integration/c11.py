#!/usr/bin/env python3
"""Criterion 11: `python tools/eos_check.py --repo` exits zero.

That script is the EOS repository's own check. The tree this drill
grades is a standalone orders service: the frozen spec asks for a
command that belongs to a different repository, and no grader can honour
it by inventing one. So when the script is not in the delivered tree the
criterion is left unsettled rather than failed, which the runner records
as manual and which blocks a green drill exactly as it should.

When the script is there, it is run, and its exit code decides.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, UNSETTLED, emit, scratch_dir  # noqa: E402

CID = "c11"
SCRIPT = "tools/eos_check.py"


def main():
    scratch = scratch_dir()
    script = scratch / SCRIPT
    if not script.is_file():
        emit(CID, UNSETTLED,
             "no %s in the delivered tree. That script is the EOS "
             "repository's own check and the tree graded here is the "
             "service repository the drill seeds, so this criterion cannot "
             "be settled against it. A gap in the frozen spec, not a "
             "finding against the work." % SCRIPT)
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--repo"], cwd=str(scratch),
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        emit(CID, FAIL, "%s could not be run: %s" % (SCRIPT, exc))
    tail = " ".join((proc.stdout + " " + proc.stderr).split())[:250]
    if proc.returncode == 0:
        emit(CID, PASS, "%s --repo exits 0: %s" % (SCRIPT, tail))
    emit(CID, FAIL,
         "%s --repo exits %d: %s" % (SCRIPT, proc.returncode, tail))


if __name__ == "__main__":
    main()
