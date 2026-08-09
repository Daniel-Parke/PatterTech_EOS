#!/usr/bin/env python3
"""Criterion 1: CI runs a pinned link checker, fragments included.

Three separate claims, checked separately, because a tree can satisfy
any two of them and still let the fault back in:

- there is a committed automation file at all,
- one of its steps runs a link checker,
- that checker looks at the part of a link after the `#`.

"Pinned" is read as "cannot change under the project without a commit".
A third-party action or package therefore needs a version or a commit
sha; a checker written into the repository is pinned already, and is
accepted as such rather than being failed for having no version number.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (CHECKERS, FAIL, FRAGMENT_TOKENS, PASS,  # noqa: E402
                     ci_files, emit, link_check_commands, named_files,
                     read, rel, scratch_dir)

CID = "c1"

FLOATING = {"main", "master", "latest", "head", "stable", "edge", "dev"}

CHECKER_CONFIGS = (
    "lychee.toml", ".lychee.toml", "lychee.conf", ".lycheeignore",
    ".markdown-link-check.json", "mlc.toml", ".mlc.toml",
    ".linkspector.yml", ".linkspector.yaml", "linkcheck.toml",
)

# The words a hand-written checker uses when it resolves a `#target`.
SOURCE_FRAGMENT_WORDS = ("fragment", "anchor", "slug", "heading")


def pinned_third_party(text, checker):
    """Is the named third-party checker held at a fixed version?"""
    for m in re.finditer(re.escape(checker) + r"[\w./-]*@([\w.-]+)", text,
                         re.I):
        if m.group(1).lower() not in FLOATING:
            return "@%s" % m.group(1)
    for m in re.finditer(re.escape(checker) + r"[\w.-]*\s*==\s*([\w.]+)",
                         text, re.I):
        return "==%s" % m.group(1)
    for m in re.finditer(re.escape(checker) + r"[\w./-]*:(v?\d[\w.]*)", text,
                         re.I):
        return ":%s" % m.group(1)
    m = re.search(r"rev:\s*([\w.-]+)", text)
    if m and checker in text and m.group(1).lower() not in FLOATING:
        return "rev: %s" % m.group(1)
    return None


def fragment_evidence(scratch, ci_text, commands):
    for token in FRAGMENT_TOKENS:
        if token in ci_text.lower():
            return "the invocation carries %s" % token
    for name in CHECKER_CONFIGS:
        path = scratch / name
        if path.is_file():
            body = read(path).lower()
            for token in FRAGMENT_TOKENS:
                if token in body:
                    return "%s sets %s" % (name, token)
    for _, command, _ in commands:
        for path in named_files(scratch, command):
            body = read(path).lower()
            hits = [w for w in SOURCE_FRAGMENT_WORDS if w in body]
            if hits:
                return ("%s resolves them itself (mentions %s)"
                        % (rel(scratch, path), ", ".join(sorted(hits))))
    return None


def main():
    scratch = scratch_dir()
    files = ci_files(scratch)
    if not files:
        emit(CID, FAIL,
             "no committed automation file in the tree, so nothing checks "
             "the documentation on any change")

    where = ", ".join(rel(scratch, p) for p in files[:4])
    ci_text = "\n".join(read(p) for p in files)
    commands = link_check_commands(scratch)
    if not commands:
        named = [c for c in CHECKERS if c in ci_text.lower()]
        if named:
            emit(CID, FAIL,
                 "%s names %s but no step runs it; a tool listed and never "
                 "invoked checks nothing" % (where, named[0]))
        emit(CID, FAIL,
             "%s runs no link checker: no step names one of %s and no step "
             "runs a link-checking script from the tree"
             % (where, ", ".join(CHECKERS[:4])))

    source, command, checker = commands[0]
    if checker in CHECKERS:
        pin = pinned_third_party(ci_text, checker)
        if pin is None:
            emit(CID, FAIL,
                 "%s runs %s but nothing pins it: an unpinned checker can "
                 "change what it accepts between two runs of the same tree"
                 % (source, checker))
        how = "%s pinned %s" % (checker, pin)
    else:
        how = ("%s, committed in the tree and so pinned to this commit"
               % checker)

    fragments = fragment_evidence(scratch, ci_text, commands)
    if fragments is None:
        emit(CID, FAIL,
             "%s runs %s but nothing shows fragments are checked, so a link "
             "to a heading that no longer exists still passes" % (source, how))

    emit(CID, PASS,
         "%s runs %s, and %s" % (source, how, fragments))


if __name__ == "__main__":
    main()
