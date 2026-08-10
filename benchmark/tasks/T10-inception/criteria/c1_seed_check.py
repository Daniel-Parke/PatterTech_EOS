#!/usr/bin/env python3
"""The compiled seed pack must pass eos_check --seed first time.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_seed_check"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_seed_check.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _find_pack(scratch):
    preferred = scratch / "seed"
    if (preferred / "docs" / "LOCKBOOK.md").is_file():
        return preferred
    hits = []
    for lockbook in scratch.rglob("docs/LOCKBOOK.md"):
        rel_parts = lockbook.relative_to(scratch).parts
        if any(p in (".git", "kernel", "inception", "templates")
               for p in rel_parts):
            continue
        hits.append(lockbook.parent.parent)
    if (scratch / "docs" / "LOCKBOOK.md").is_file():
        hits.append(scratch)
    hits.sort(key=lambda p: len(p.parts))
    return hits[0] if hits else None


def main():
    import subprocess
    scratch = scratch_dir()
    pack = _find_pack(scratch)
    if pack is None:
        emit(False, "no compiled seed pack found (no docs/LOCKBOOK.md "
                    "outside the kernel)")
    checker = scratch / "tools" / "eos_check.py"
    if not checker.is_file():
        checker = Path(__file__).resolve().parents[4] / "tools" / \
            "eos_check.py"
    if not checker.is_file():
        emit(False, "no eos_check.py available to validate the pack")
    try:
        proc = subprocess.run(
            [sys.executable, str(checker), "--seed", str(pack)],
            cwd=str(scratch), capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        emit(False, "eos_check --seed timed out")
    lines = proc.stdout.strip().splitlines()
    last = lines[-1] if lines else "no output"
    if proc.returncode == 0:
        emit(True, "seed pack at %s passes eos_check --seed: %s"
             % (pack.name, last))
    emit(False, "eos_check --seed failed on %s: %s" % (pack.name, last))


if __name__ == "__main__":
    main()
