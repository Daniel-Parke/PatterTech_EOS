#!/usr/bin/env python3
"""The regression test must exist and fail on the baseline tree.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_repro_test"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_repro_test.py <scratch-dir>")
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
    import shutil
    import subprocess
    import tempfile
    scratch = scratch_dir()
    root = _root_commit(scratch)
    candidates = []
    for rel in _changed_files(scratch, root):
        if not (rel.startswith("tests/") and rel.endswith(".py")):
            continue
        path = scratch / rel
        if path.is_file() and "refund" in path.read_text(
                encoding="utf-8", errors="replace"):
            candidates.append(rel)
    if not candidates:
        emit(False, "no new or changed test under tests/ touches refunds")
    worktree = Path(tempfile.mkdtemp(prefix="t04-baseline-"))
    try:
        proc = _git(scratch, "worktree", "add", "--detach", str(worktree),
                    root)
        if proc.returncode != 0:
            emit(False, "could not create baseline worktree: %s"
                 % proc.stderr.strip())
        failing = []
        for rel in candidates:
            target = worktree / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(scratch / rel), str(target))
            try:
                run = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s",
                     "tests", "-p", Path(rel).name],
                    cwd=str(worktree), capture_output=True, text=True,
                    timeout=240)
            except subprocess.TimeoutExpired:
                continue
            out = (run.stderr or run.stdout)
            if run.returncode != 0 and "Ran 0 tests" not in out:
                failing.append(rel)
        if failing:
            emit(True, "regression test fails on the baseline as it "
                       "should: %s" % ", ".join(failing))
        emit(False, "no candidate test fails against the baseline tree "
                    "(checked: %s)" % ", ".join(candidates))
    finally:
        _git(scratch, "worktree", "remove", "--force", str(worktree))
        shutil.rmtree(worktree, ignore_errors=True)


if __name__ == "__main__":
    main()
