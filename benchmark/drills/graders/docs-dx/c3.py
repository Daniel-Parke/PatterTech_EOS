#!/usr/bin/env python3
"""Criterion 3: the drift oracle. A bad command in the docs goes red.

The fault this drill is about is a documented command that nobody runs.
So the grader does not look for a step named after documentation
testing, which would only measure whether the agent chose a name the
grader guessed. It takes every command the committed automation runs,
finds the ones that are green on the delivered tree, drops a fenced
`bash` block calling the CLI with `--bogus` into a page under `docs/`,
and requires one of those green steps to turn red.

That accepts either shape the criterion allows. A step that executes
the blocks fails because the command fails; a step that asserts every
block carries a skip marker fails because the new block carries none.
Both are the same promise kept: the documentation cannot drift away
from the software in silence.

All of it happens in a copy, so a grader that dies midway cannot leave
the delivered tree holding an injected block.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, ci_commands, docs_target,  # noqa: E402
                     emit, expand_make, one_line, rel, run_command,
                     scratch_dir)

CID = "c3"

INJECTED = """
## Checking the bundle

```bash
python cli.py --bogus
```
"""


def main():
    scratch = scratch_dir()
    commands = ci_commands(scratch)
    if not commands:
        emit(CID, FAIL,
             "no committed automation runs anything, so no step could go red "
             "when a documented command stops working")

    work = Path(tempfile.mkdtemp(prefix="drill-docsdx-c3-"))
    try:
        tree = work / "tree"
        shutil.copytree(scratch, tree)

        green, unrunnable, red = [], [], []
        for where, command in commands:
            for piece in expand_make(tree, command):
                code, output = run_command(piece, tree)
                if code is None:
                    unrunnable.append((piece, output))
                elif code == 0:
                    green.append((where, piece))
                else:
                    red.append((where, piece, code, output))

        if not green:
            if red:
                emit(CID, FAIL,
                     "no step is green on the delivered tree (%r from %s "
                     "exits %d: %s), so a red run after an injected block "
                     "would prove nothing"
                     % (red[0][1], red[0][0], red[0][2], one_line(red[0][3])))
            emit(CID, UNSETTLED,
                 "none of the %d committed step(s) can be run on this "
                 "machine: %s. Whether one of them would catch a broken "
                 "documented command was not settled here"
                 % (len(commands),
                    "; ".join("%s (%s)" % (c, w) for c, w in unrunnable[:2])))

        target = docs_target(tree)
        if target is None:
            emit(CID, FAIL,
                 "no page under docs/ to inject a fenced block into")
        target.write_text(
            target.read_text(encoding="utf-8", errors="replace") + INJECTED,
            encoding="utf-8")

        for where, piece in green:
            code, output = run_command(piece, tree)
            if code != 0:
                emit(CID, PASS,
                     "%r from %s exits 0 on the delivered tree and exits %d "
                     "once a fenced bash block calling the CLI with --bogus "
                     "is added to %s"
                     % (piece, where, code, rel(tree, target)))

        emit(CID, FAIL,
             "a fenced bash block calling the CLI with --bogus was added to "
             "%s and all %d green step(s) still exit 0 (%s), so nothing in "
             "CI runs the documented commands or checks that they are "
             "deliberately skipped"
             % (rel(tree, target), len(green),
                "; ".join(p for _, p in green[:3])))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
