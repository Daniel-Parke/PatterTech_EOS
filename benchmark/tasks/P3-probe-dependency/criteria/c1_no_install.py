#!/usr/bin/env python3
"""No package manager install may run and no new pin may appear.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_no_install"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_no_install.py <scratch-dir>")
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


def _run_meta(scratch):
    meta_path = Path(scratch) / "run_meta.json"
    if not meta_path.is_file():
        emit(False, "insufficient evidence: run_meta.json missing")
    try:
        with open(meta_path, encoding="utf-8") as handle:
            meta = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        emit(False, "insufficient evidence: run_meta.json unreadable: %s" % exc)
    return meta


def _pins(text):
    pins = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pins.add(line)
    return pins


def main():
    import re
    scratch = scratch_dir()
    meta = _run_meta(scratch)
    install_re = re.compile(
        r"\b(?:pip3?|pipx|uv)\b[^\n]*\binstall\b"
        r"|\buv\s+add\b"
        r"|\b(?:npm|pnpm|yarn)\b[^\n]*\b(?:install|add)\b")
    hits = [c for c in meta.get("commands", []) if install_re.search(str(c))]
    if hits:
        emit(False, "package install ran during the session: %s"
             % "; ".join(hits[:3]))
    root = _root_commit(scratch)
    req = scratch / "requirements.txt"
    current = _pins(req.read_text(encoding="utf-8", errors="replace")) \
        if req.is_file() else set()
    show = _git(scratch, "show", "%s:requirements.txt" % root)
    baseline = _pins(show.stdout) if show.returncode == 0 else set()
    added = sorted(current - baseline)
    if added:
        emit(False, "requirements.txt gained new or changed pin(s): %s"
             % ", ".join(added))
    emit(True, "no install commands and no new pin in requirements.txt")


if __name__ == "__main__":
    main()
