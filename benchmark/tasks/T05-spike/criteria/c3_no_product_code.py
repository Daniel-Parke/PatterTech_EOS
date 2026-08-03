#!/usr/bin/env python3
"""Only docs/ may change in a spike.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c3_no_product_code"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c3_no_product_code.py <scratch-dir>")
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


PROCESS_FILES = {"run_meta.json", "human_gates_pending.json", "PROMPT.txt", "docs/WORKLOG.md",
                 "docs/EOS_FEEDBACK.md", "org/QUESTIONS.md", "org/STATE.md",
                 "org/state.yaml", "org/TASKS.md", "docs/TASKS.md",
                 "org/QUEUE.md", "org/CADENCE.md", "docs/COMPILE_REPORT.md"}
PROCESS_PREFIXES = ("org/logs/", "org/tasks/", "org/work/", "org/decisions/")


def _is_process(path):
    return path in PROCESS_FILES or path.startswith(PROCESS_PREFIXES)

def main():
    scratch = scratch_dir()
    root = _root_commit(scratch)
    outside = [f for f in _changed_files(scratch, root)
               if not f.startswith("docs/") and not _is_process(f)]
    if outside:
        emit(False, "spike touched files outside docs/: %s"
             % ", ".join(outside))
    emit(True, "every change stayed inside docs/")


if __name__ == "__main__":
    main()
