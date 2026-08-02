#!/usr/bin/env python3
"""The fixture's own checker must pass with zero errors.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_checker_green"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_checker_green.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def main():
    import subprocess
    scratch = scratch_dir()
    checker = scratch / "tools" / "eos_check.py"
    if not checker.is_file():
        emit(False, "tools/eos_check.py missing from the scratch tree")
    try:
        proc = subprocess.run(
            [sys.executable, str(checker), "--repo"], cwd=str(scratch),
            capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        emit(False, "eos_check --repo timed out")
    lines = proc.stdout.strip().splitlines()
    last = lines[-1] if lines else "no output"
    if proc.returncode == 0:
        emit(True, "eos_check --repo clean: %s" % last)
    emit(False, "eos_check --repo failed: %s" % last)


if __name__ == "__main__":
    main()
