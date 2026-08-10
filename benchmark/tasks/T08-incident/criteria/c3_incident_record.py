#!/usr/bin/env python3
"""A new markdown incident record must exist.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c3_incident_record"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c3_incident_record.py <scratch-dir>")
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


def main():
    import re
    scratch = scratch_dir()
    root = _root_commit(scratch)
    marker = re.compile(
        r"(?i)(incident|root cause|postmortem|post-mortem|outage)")
    seen = []
    for rel in _changed_files(scratch, root):
        if not rel.endswith(".md"):
            continue
        exists_before = _git(scratch, "cat-file", "-e",
                             "%s:%s" % (root, rel))
        if exists_before.returncode == 0:
            continue
        path = scratch / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        seen.append(rel)
        lines = [l for l in text.splitlines() if l.strip()]
        if marker.search(text) and len(lines) >= 3:
            emit(True, "incident record found at %s" % rel)
    if seen:
        emit(False, "new markdown found (%s) but none reads as an "
                    "incident record" % ", ".join(seen))
    emit(False, "no new markdown incident record in the scratch tree")


if __name__ == "__main__":
    main()
