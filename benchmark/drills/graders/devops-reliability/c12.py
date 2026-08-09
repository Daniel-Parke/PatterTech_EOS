#!/usr/bin/env python3
"""Criterion 12: nothing secret-shaped in what the change added.

The diff is computed against the frozen fixture, line by line: a new
file contributes everything in it, a changed file contributes only what
changed. A credential the fixture already carried and the agent left
alone is not part of this change and is not this criterion's finding.

Read the verdict for what it is. On a tree where nothing was delivered
the diff is empty, so this passes without having looked at anything: it
is a do-no-harm gate, not a measure of the work. The second half of the
criterion as written names a repository check script. That script
belongs to the repository the drill is run from, not to the service
fixture, so it is run here only if the delivered tree actually carries
one, and the reason says which of the two halves settled the verdict.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, added_lines, emit,  # noqa: E402
                     require_baseline, run, scratch_dir)

CID = "c12"

REPO_CHECK = "tools/eos_check.py"

SECRET_RES = (
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s:/@]{6,}@"),
     "password in a connection string"),
    (re.compile(r"(?i)(api[_-]?key|secret[_\w-]*|token|password|passwd|"
                r"pwd|access[_-]?key|private[_-]?key|credential)"
                r"\s*[:=]\s*[\"']?([A-Za-z0-9/+=_.-]{16,})[\"']?"),
     "a credential assigned in place"),
)

# Things that look like a secret and are not one.
INNOCENT = re.compile(
    r"(?i)(\$\{|\$\(|%\(|<[a-z_]+>|\bos\.environ\b|\bgetenv\b|\bsecrets\.|"
    r"\bvault\b|xxx+|\*\*\*|changeme|redacted|placeholder|example|dummy|"
    r"your[-_]|\bnone\b|\bnull\b|\benv\b\.|@example\.com)")


def findings(lines):
    out = []
    for rel, line in lines:
        if INNOCENT.search(line):
            continue
        for pattern, label in SECRET_RES:
            match = pattern.search(line)
            if match:
                shown = match.group(0)
                out.append("%s: %s (%s)"
                           % (rel, shown[:24] + ("..." if len(shown) > 24
                                                 else ""), label))
                break
    return out


def main():
    scratch = scratch_dir()
    baseline = require_baseline(CID)

    lines = added_lines(scratch, baseline)
    hits = findings(lines)
    if hits:
        emit(CID, FAIL,
             "%d secret-shaped string(s) in the %d added or changed line(s): "
             "%s" % (len(hits), len(lines), "; ".join(hits[:3])))

    check = scratch / REPO_CHECK
    if check.is_file():
        code, output = run([sys.executable, REPO_CHECK, "--repo"], scratch)
        if code is None:
            emit(CID, FAIL, "%s would not run: %s"
                            % (REPO_CHECK, " ".join(output.split())[:200]))
        if code != 0:
            emit(CID, FAIL,
                 "no secret-shaped string in the diff, but %s --repo exits "
                 "%d: %s" % (REPO_CHECK, code,
                             " ".join(output.split())[-200:]))
        emit(CID, PASS,
             "no secret-shaped string in the %d added or changed line(s), "
             "and %s --repo exits 0" % (len(lines), REPO_CHECK))

    emit(CID, PASS,
         "no secret-shaped string in the %d added or changed line(s) across "
         "%d file(s). The tree carries no %s, so only the secret half of "
         "this criterion was settled"
         % (len(lines), len({rel for rel, _ in lines}), REPO_CHECK))


if __name__ == "__main__":
    main()
