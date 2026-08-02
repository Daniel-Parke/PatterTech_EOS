#!/usr/bin/env python3
"""No script tag may be added to any page.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_no_script"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_no_script.py <scratch-dir>")
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
            if line and line != "run_meta.json":
                files.add(line)
    return sorted(files)


def _untracked_files(scratch):
    proc = _git(scratch, "ls-files", "--others", "--exclude-standard")
    files = []
    for line in proc.stdout.splitlines():
        line = line.strip().replace("\\", "/")
        if line and line != "run_meta.json":
            files.append(line)
    return files


def main():
    import re
    scratch = scratch_dir()
    root = _root_commit(scratch)
    script_re = re.compile(r"<script\b", re.I)
    offenders = []
    for rel in _changed_files(scratch, root):
        if not rel.endswith((".html", ".htm")):
            continue
        path = scratch / rel
        current = len(script_re.findall(
            path.read_text(encoding="utf-8", errors="replace"))) \
            if path.is_file() else 0
        show = _git(scratch, "show", "%s:%s" % (root, rel))
        baseline = len(script_re.findall(show.stdout)) \
            if show.returncode == 0 else 0
        if current > baseline:
            offenders.append("%s (%d -> %d script tags)"
                             % (rel, baseline, current))
    if offenders:
        emit(False, "script tag added: %s" % "; ".join(offenders))
    emit(True, "no script tag added to any page")


if __name__ == "__main__":
    main()
