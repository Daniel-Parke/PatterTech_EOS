#!/usr/bin/env python3
"""Run the fixture's visible unittest suite; it must be green.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c3_visible_suite"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c3_visible_suite.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def main():
    import subprocess
    scratch = scratch_dir()
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=str(scratch), capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        emit(False, "visible suite timed out after 240s")
    tail = (proc.stderr or proc.stdout).strip().splitlines()
    last = tail[-1] if tail else "no output"
    if proc.returncode == 0:
        emit(True, "visible suite green: %s" % last)
    emit(False, "visible suite failed: %s" % last)


if __name__ == "__main__":
    main()
