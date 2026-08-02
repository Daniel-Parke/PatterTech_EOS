#!/usr/bin/env python3
"""Copy the canonical acceptance suite into the scratch tree and run it.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_acceptance"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_acceptance.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def main():
    import shutil
    import subprocess
    scratch = scratch_dir()
    canonical = Path(__file__).resolve().parents[1] / "assets" / \
        "test_summary_acceptance.py"
    if not canonical.is_file():
        emit(False, "canonical acceptance file missing from the task dir")
    tests_dir = scratch / "tests"
    if not tests_dir.is_dir():
        emit(False, "scratch tree has no tests/ directory")
    shutil.copyfile(str(canonical),
                    str(tests_dir / "test_summary_acceptance.py"))
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests",
             "-p", "test_summary_acceptance.py"],
            cwd=str(scratch), capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        emit(False, "acceptance suite timed out after 240s")
    out = (proc.stderr or proc.stdout).strip()
    last = out.splitlines()[-1] if out else "no output"
    if "Ran 0 tests" in out:
        emit(False, "acceptance suite discovered no tests")
    if proc.returncode == 0:
        emit(True, "acceptance suite green: %s" % last)
    emit(False, "acceptance suite failed: %s" % last)


if __name__ == "__main__":
    main()
