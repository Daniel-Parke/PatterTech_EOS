#!/usr/bin/env python3
"""Criterion 5: the same command is wired into a committed automation file.

A contract nothing runs is the drill's first named failure condition,
so this looks for the command in a CI workflow or a pre-commit config
rather than anywhere in the tree: a mention in the README is not
enforcement.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402

CID = "c5"

GLOBS = (
    ".github/workflows/*.yml", ".github/workflows/*.yaml",
    ".gitlab-ci.yml", ".gitlab-ci.yaml",
    ".pre-commit-config.yaml", ".pre-commit-config.yml",
    "Makefile", "noxfile.py", "tox.ini",
    ".circleci/config.yml", "azure-pipelines.yml",
)
COMMANDS = ("lint-imports", "importlinter", "import_linter")


def main():
    scratch = scratch_dir()
    searched, hits = [], []
    for pattern in GLOBS:
        for path in sorted(scratch.glob(pattern)):
            if not path.is_file():
                continue
            rel = path.relative_to(scratch).as_posix()
            searched.append(rel)
            text = read(path)
            for command in COMMANDS:
                if command in text:
                    hits.append((rel, command))
                    break

    if hits:
        emit(CID, PASS,
             "%s invokes %s" % (hits[0][0], hits[0][1]))
    if searched:
        emit(CID, FAIL,
             "found automation files (%s) but none invokes the boundary "
             "command; the contract is documentation, not a gate"
             % ", ".join(searched[:5]))
    emit(CID, FAIL,
         "no CI workflow or pre-commit config in the tree, so nothing runs "
         "the boundary check")


if __name__ == "__main__":
    main()
