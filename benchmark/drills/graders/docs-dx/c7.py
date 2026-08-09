#!/usr/bin/env python3
"""Criterion 7: an unreachable external link must not fail the build.

The trap this criterion sets is enthusiasm. An agent that wires up a
link checker and points it at the whole internet has built a gate that
goes red when somebody else's server is down, and a gate like that gets
switched off within a month. So the grader adds a link to
`https://example.invalid/`, a domain that can never resolve, and
requires every step that was green to stay green.

A tree with no link checking at all is failed here rather than passed.
Nothing fails when nothing runs, and reading that as a pass would hand
the criterion to the emptiest possible tree.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, OFFLINE_TOKENS, ONLINE_TOKENS, PASS,  # noqa: E402
                     UNSETTLED, ci_files, docs_target, emit, expand_make,
                     link_check_commands, one_line, read, rel, run_command,
                     scratch_dir)

CID = "c7"

INJECTED = ("\nFurther reading lives at "
            "[the project site](https://example.invalid/).\n")


def static_verdict(scratch):
    """What the configuration says, when the checker cannot be run."""
    text = "\n".join(read(p) for p in ci_files(scratch)).lower()
    for name in ("lychee.toml", ".lychee.toml", ".markdown-link-check.json",
                 ".linkspector.yml", "mlc.toml"):
        path = scratch / name
        if path.is_file():
            text += "\n" + read(path).lower()
    for token in OFFLINE_TOKENS:
        if token in text:
            return PASS, "the invocation carries %s" % token
    if "continue-on-error: true" in text:
        return PASS, "the step is marked continue-on-error: true"
    for token in ONLINE_TOKENS:
        if token in text:
            return FAIL, ("the invocation carries %s, so somebody else's "
                          "outage turns this build red" % token)
    return None, ("the checker could not be run here and its configuration "
                  "says nothing either way about external links")


def main():
    scratch = scratch_dir()
    commands = link_check_commands(scratch)
    if not commands:
        emit(CID, FAIL,
             "no link-checking step in the tree. Nothing fails because "
             "nothing runs, which is not what this criterion is asking; "
             "criterion 1 covers the missing check")

    work = Path(tempfile.mkdtemp(prefix="drill-docsdx-c7-"))
    try:
        tree = work / "tree"
        shutil.copytree(scratch, tree)

        pieces = []
        for _, command, _ in commands:
            pieces.extend(expand_make(tree, command))

        green, unrunnable = [], []
        for piece in pieces:
            code, output = run_command(piece, tree)
            if code is None:
                unrunnable.append((piece, output))
            elif code == 0:
                green.append(piece)
            else:
                emit(CID, FAIL,
                     "%r already exits %d on the delivered tree, so what an "
                     "unreachable link does to it cannot be read: %s"
                     % (piece, code, one_line(output)))

        if not green:
            verdict, why = static_verdict(scratch)
            if verdict is None:
                emit(CID, UNSETTLED,
                     "%s (%s)" % (why, unrunnable[0][1] if unrunnable
                                  else "nothing to run"))
            emit(CID, verdict, why)

        target = docs_target(tree) or (tree / "README.md")
        target.write_text(
            read(target) + INJECTED, encoding="utf-8")

        for piece in green:
            code, output = run_command(piece, tree)
            if code != 0:
                emit(CID, FAIL,
                     "%r exits %d once a link to https://example.invalid/ is "
                     "added to %s, so the build depends on the network being "
                     "up and on other people's servers answering: %s"
                     % (piece, code, rel(tree, target), one_line(output)))

        emit(CID, PASS,
             "all %d link-checking step(s) still exit 0 with a link to "
             "https://example.invalid/ in %s"
             % (len(green), rel(tree, target)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
