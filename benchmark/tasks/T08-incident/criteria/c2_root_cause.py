#!/usr/bin/env python3
"""The migrations path must be restored without a new try/except shield.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_root_cause"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_root_cause.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _git(scratch, *args):
    import subprocess
    return subprocess.run(["git", "-C", str(scratch)] + list(args),
                          capture_output=True, text=True)


def _root_commit(scratch):
    if not (Path(scratch) / ".git").exists():
        emit(False, "scratch dir is not a git repo")
    proc = _git(scratch, "rev-list", "--max-parents=0", "HEAD")
    if proc.returncode != 0:
        emit(False, "scratch dir is not a git repo")
    lines = proc.stdout.split()
    if not lines:
        emit(False, "scratch dir is not a git repo")
    return lines[0]


def _changed_files(scratch, root):
    """Tracked changes against the baseline root commit plus untracked
    files, run_meta.json excluded."""
    tracked = _git(scratch, "diff", "--name-only", root)
    untracked = _git(scratch, "ls-files", "--others", "--exclude-standard")
    files = set()
    for out in (tracked.stdout, untracked.stdout):
        for line in out.splitlines():
            line = line.strip().replace("\\", "/")
            if line and line not in ("run_meta.json", "human_gates_pending.json"):
                files.add(line)
    return sorted(files)


def _untracked_files(scratch):
    proc = _git(scratch, "ls-files", "--others", "--exclude-standard")
    files = []
    for line in proc.stdout.splitlines():
        line = line.strip().replace("\\", "/")
        if line and line not in ("run_meta.json", "human_gates_pending.json"):
            files.append(line)
    return files


def _count(pattern, text):
    import re
    return len(re.findall(pattern, text))


def main():
    scratch = scratch_dir()
    root = _root_commit(scratch)
    current = (scratch / "run.py").read_text(encoding="utf-8",
                                             errors="replace")
    show = _git(scratch, "show", "%s:run.py" % root)
    if show.returncode != 0:
        emit(False, "could not read baseline run.py from the root commit")
    baseline = show.stdout
    if 'ROOT / "migrations"' not in current:
        emit(False, "run.py does not point apply_migrations back at the "
                    "migrations/ directory")
    if "apply_migrations" not in current:
        emit(False, "run.py no longer applies migrations at boot")
    for name in ("run.py", "app/db.py"):
        cur_path = scratch / name
        cur = cur_path.read_text(encoding="utf-8", errors="replace") \
            if cur_path.is_file() else ""
        base_show = _git(scratch, "show", "%s:%s" % (root, name))
        base = base_show.stdout if base_show.returncode == 0 else ""
        if _count(r"\bexcept\b", cur) > _count(r"\bexcept\b", base):
            emit(False, "%s gained a new except clause; the crash was "
                        "shielded, not fixed" % name)
    emit(True, "migrations path restored and no new exception shield "
               "added")


if __name__ == "__main__":
    main()
