#!/usr/bin/env python3
"""Every repo path cited in the new note must exist.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_paths_resolve"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_paths_resolve.py <scratch-dir>")
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


def _new_notes(scratch, root):
    notes = []
    for rel in _changed_files(scratch, root):
        if rel.startswith("docs/") and rel.endswith(".md"):
            baseline = _git(scratch, "cat-file", "-e", "%s:%s" % (root, rel))
            if baseline.returncode != 0 and (scratch / rel).is_file():
                notes.append(rel)
    return notes


def main():
    import re
    scratch = scratch_dir()
    root = _root_commit(scratch)
    notes = _new_notes(scratch, root)
    if not notes:
        emit(False, "no new markdown file under docs/")
    path_re = re.compile(
        r"(?<![\w/])((?:[A-Za-z0-9_][A-Za-z0-9_.-]*/)+"
        r"[A-Za-z0-9_][A-Za-z0-9_.-]*\.[A-Za-z0-9]{1,5})")
    missing = []
    cited = 0
    for rel in notes:
        text = (scratch / rel).read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"https?://\S+", " ", text)
        for cite in sorted(set(path_re.findall(text))):
            cited += 1
            if not (scratch / cite).exists():
                missing.append("%s cites %s" % (rel, cite))
    if missing:
        emit(False, "invented citation(s): %s" % "; ".join(missing))
    emit(True, "all %d cited repo paths exist" % cited)


if __name__ == "__main__":
    main()
