#!/usr/bin/env python3
"""Criterion 2: CI runs a breaking-change check against the baseline.

Two halves. The first is the criterion's sentence: a committed
automation file invokes a diff tool and points it at
api/baseline/openapi.yaml, and that baseline exists. That is decided
here and it is what the verdict rests on.

The second is the drill's parenthetical, running the tool. oasdiff is
not a standard install, so when it is absent the reason says the wiring
was read and not executed rather than claiming a run that never
happened. When it is present the run happens and its outcome is
reported; a breaking finding is not turned into a failure of this
criterion, because whether a break was shipped silently is what
criteria 3 and 4 decide, on the document itself.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BASELINE_REL, FAIL, PASS, SPEC_REL, ci_files,  # noqa: E402
                     emit, scratch_dir)

CID = "c2"

TOOLS = (
    (re.compile(r"\boasdiff\b", re.I), "oasdiff"),
    (re.compile(r"openapi[-_]diff", re.I), "openapi-diff"),
    (re.compile(r"openapi[-_]changes", re.I), "openapi-changes"),
    (re.compile(r"\boptic\b", re.I), "optic"),
    (re.compile(r"breaking[-_ ]?changes?[-_ ]?(check|action|gate)", re.I),
     "a breaking-change action"),
)
BREAKING = re.compile(r"breaking", re.I)
BASELINE = re.compile(r"baseline[/\\]openapi\.ya?ml", re.I)


def run_oasdiff(scratch):
    binary = shutil.which("oasdiff")
    if not binary:
        return None
    try:
        proc = subprocess.run(
            [binary, "breaking", str(scratch / BASELINE_REL),
             str(scratch / SPEC_REL)],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "oasdiff could not be run here: %s" % exc
    tail = " ".join((proc.stdout + " " + proc.stderr).split())[:160]
    return "oasdiff breaking exits %d: %s" % (proc.returncode, tail)


def main():
    scratch = scratch_dir()
    if not (scratch / BASELINE_REL).is_file():
        emit(CID, FAIL,
             "no %s to compare against; the baseline the check needs is not "
             "in the tree" % BASELINE_REL)

    files = ci_files(scratch)
    if not files:
        emit(CID, FAIL,
             "no committed automation file at all, so nothing runs a "
             "breaking-change check")

    named_tool = []
    for rel, text in files:
        for pattern, label in TOOLS:
            if not pattern.search(text):
                continue
            if label == "oasdiff" and not BREAKING.search(text):
                continue
            named_tool.append((rel, label, text))
            break

    if not named_tool:
        emit(CID, FAIL,
             "none of the %d automation file(s) (%s) invokes a breaking "
             "change check; the baseline sits in the tree unread"
             % (len(files), ", ".join(rel for rel, _ in files[:6])))

    for rel, label, text in named_tool:
        if BASELINE.search(text):
            ran = run_oasdiff(scratch)
            note = ran or ("oasdiff is not installed here, so the wiring was "
                           "read and not executed")
            emit(CID, PASS,
                 "%s invokes %s against %s. %s" % (rel, label, BASELINE_REL,
                                                   note))

    emit(CID, FAIL,
         "%s invokes %s but never points it at %s, so the check has nothing "
         "to compare the delivered document with"
         % (named_tool[0][0], named_tool[0][1], BASELINE_REL))


if __name__ == "__main__":
    main()
