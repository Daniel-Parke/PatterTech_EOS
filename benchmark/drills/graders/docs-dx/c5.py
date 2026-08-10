#!/usr/bin/env python3
"""Criterion 5: the wrong flag is rejected with something a reader can use.

The fixture prints `error` and exits 1, which is why the user in the
prompt could not tell what went wrong. Three things are required of the
replacement and all three are the criterion as written: a non-zero
exit, the real flag named in the output, and enough output to be a
sentence rather than a word.

Run in a copy: the command is expected to fail, but a tree that
wrongly accepts `--outdir` would otherwise write into the delivered
tree while being graded.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, one_line, run_command, scratch_dir  # noqa: E402

CID = "c5"

COMMAND = "python cli.py --outdir /tmp/x"
NEEDLE = "--out-dir"
MIN_LEN = 20


def main():
    scratch = scratch_dir()
    if not (scratch / "cli.py").is_file():
        emit(CID, FAIL, "no cli.py in the tree to run")

    work = Path(tempfile.mkdtemp(prefix="drill-docsdx-c5-"))
    try:
        tree = work / "tree"
        shutil.copytree(scratch, tree)
        code, output = run_command(COMMAND, tree, timeout=60)
        if code is None:
            emit(CID, FAIL, "could not run %r: %s" % (COMMAND, output))
        combined = (output or "").strip()

        if code == 0:
            emit(CID, FAIL,
                 "%r exits 0, so the removed flag is silently accepted: %s"
                 % (COMMAND, one_line(combined) or "no output"))
        if NEEDLE not in combined:
            emit(CID, FAIL,
                 "%r exits %d but its output never names %s, so a reader is "
                 "told they are wrong and not told what is right: %r"
                 % (COMMAND, code, NEEDLE, one_line(combined) or ""))
        if len(combined) < MIN_LEN:
            emit(CID, FAIL,
                 "%r exits %d and names %s but its whole output is %d "
                 "characters (%r); the criterion asks for at least %d"
                 % (COMMAND, code, NEEDLE, len(combined),
                    one_line(combined), MIN_LEN))

        emit(CID, PASS,
             "%r exits %d and says %r" % (COMMAND, code, one_line(combined)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
