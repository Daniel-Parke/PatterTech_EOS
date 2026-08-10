#!/usr/bin/env python3
"""Criterion 7: parser.py carries no more duplication than it started with.

The drill pins the measurement to jscpd, so this grader drives jscpd
and nothing else. The invocation and the threshold are the drill config
and are recorded here:

    jscpd --min-lines 12 --min-tokens 70 --format python
          --reporters json --silent --output <tmp> <parser.py>

Both sides are measured the same way: the delivered `parser.py` and the
one unpacked from the fixture commit. The criterion is a comparison,
not a target, so equal counts pass.

Where jscpd is not installed the criterion is left unsettled rather
than failed or waved through. A stdlib clone counter written here would
report a number the drill never froze, and a number nobody agreed to is
worse than an admitted gap.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, emit, fixture_tree,  # noqa: E402
                     has_history, parser_files, rel, require_git,
                     scratch_dir)

CID = "c7"

MIN_LINES = "12"
MIN_TOKENS = "70"
JSCPD_TIMEOUT_S = 180


def jscpd_command(scratch):
    """The pinned runner, or None. Never reaches the network."""
    direct = shutil.which("jscpd")
    if direct:
        return [direct]
    local = Path(scratch) / "node_modules" / ".bin"
    for name in ("jscpd.cmd", "jscpd"):
        candidate = local / name
        if candidate.is_file():
            return [str(candidate)]
    npx = shutil.which("npx")
    if npx:
        try:
            probe = subprocess.run([npx, "--no-install", "jscpd", "--version"],
                                   capture_output=True, text=True,
                                   encoding="utf-8", errors="replace",
                                   timeout=JSCPD_TIMEOUT_S)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if probe.returncode == 0:
            return [npx, "--no-install", "jscpd"]
    return None


def clone_count(runner, target):
    """Duplicated blocks jscpd finds in one file. (count, note)."""
    out = Path(tempfile.mkdtemp(prefix="drill-coding-c7-out-"))
    try:
        cmd = runner + ["--min-lines", MIN_LINES, "--min-tokens", MIN_TOKENS,
                        "--format", "python", "--reporters", "json",
                        "--silent", "--output", str(out), str(target)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace",
                                  timeout=JSCPD_TIMEOUT_S,
                                  env=dict(os.environ))
        except (OSError, subprocess.TimeoutExpired) as exc:
            return None, str(exc)
        report = out / "jscpd-report.json"
        if not report.is_file():
            return None, ("jscpd exited %d and wrote no report: %s"
                          % (proc.returncode,
                             " ".join((proc.stdout + proc.stderr).split())[:200]))
        try:
            doc = json.loads(report.read_text(encoding="utf-8"))
        except ValueError as exc:
            return None, "jscpd report does not parse: %s" % exc
        duplicates = doc.get("duplicates")
        if isinstance(duplicates, list):
            return len(duplicates), "jscpd report"
        stats = doc.get("statistics", {}).get("total", {})
        if "clones" in stats:
            return int(stats["clones"]), "jscpd statistics"
        return None, "jscpd report carries no duplicate count"
    finally:
        shutil.rmtree(out, ignore_errors=True)


def main():
    scratch = scratch_dir()
    files = parser_files(scratch)
    if not files:
        emit(CID, FAIL, "no parser.py in the delivered tree")

    runner = jscpd_command(scratch)
    if runner is None:
        emit(CID, UNSETTLED,
             "jscpd is not installed here and this grader will not reach the "
             "network for it, so the pinned duplicate-block measurement did "
             "not run. That is a gap in the environment, not a finding "
             "against the delivered tree.")

    require_git(CID)
    if not has_history(scratch):
        emit(CID, FAIL,
             "the delivered tree has no git history, so there is no fixture "
             "commit to measure duplication against")

    work = Path(tempfile.mkdtemp(prefix="drill-coding-c7-"))
    try:
        tree, why = fixture_tree(scratch, work)
        if tree is None:
            emit(CID, FAIL, why)
        before_files = sorted(p for p in Path(tree).rglob("parser.py"))
        if not before_files:
            emit(CID, FAIL,
                 "the fixture commit carries no parser.py, so there is "
                 "nothing to compare against")

        before, note = clone_count(runner, before_files[0])
        if before is None:
            emit(CID, UNSETTLED,
                 "jscpd could not measure the fixture commit (%s), so the "
                 "comparison did not run" % note)
        after_total = 0
        for path in files:
            count, note = clone_count(runner, path)
            if count is None:
                emit(CID, UNSETTLED,
                     "jscpd could not measure %s (%s), so the comparison did "
                     "not run" % (rel(scratch, path), note))
            after_total += count

        if after_total > before:
            emit(CID, FAIL,
                 "parser.py holds %d duplicate block(s) against %d at the %s, "
                 "so the fix was bought with fresh duplication"
                 % (after_total, before, why))
        emit(CID, PASS,
             "parser.py holds %d duplicate block(s) against %d at the %s"
             % (after_total, before, why))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
