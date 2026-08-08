#!/usr/bin/env python3
"""Criterion 9: a container-level view exists and names both modules.

Either a Structurizr DSL file or a Markdown view carrying an arc42
Building Block View or a C4 Container diagram heading. The Structurizr
CLI is not assumed present: a `.dsl` file is accepted on its structure,
and the criterion is settled on whether the view names both modules,
which is what the drill asks.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, scratch_dir  # noqa: E402

CID = "c9"

MD_HEADING = re.compile(
    r"^#{1,6}\s*(?:.*\b(?:Building\s+Block\s+View|Container\s+diagram|"
    r"Container\s+view)\b.*)$", re.I | re.M)
DSL_SHAPE = re.compile(r"\bworkspace\b[\s\S]*\bmodel\b", re.I)
MODULES = ("billing", "catalogue")


def candidates(scratch):
    for path in scratch.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in (".dsl", ".md"):
            yield path


def main():
    scratch = scratch_dir()
    near_misses = []
    for path in sorted(candidates(scratch)):
        rel = path.relative_to(scratch).as_posix()
        text = read(path)
        if path.suffix.lower() == ".dsl":
            if not DSL_SHAPE.search(text):
                continue
            kind = "Structurizr DSL"
        else:
            heading = MD_HEADING.search(text)
            if not heading:
                continue
            kind = "view heading %r" % " ".join(heading.group(0).split())
        lowered = text.lower()
        missing = [m for m in MODULES if m not in lowered]
        if not missing:
            emit(CID, PASS, "%s carries a %s naming both modules"
                            % (rel, kind))
        near_misses.append("%s is a %s but does not name %s"
                           % (rel, kind, " or ".join(missing)))

    if near_misses:
        emit(CID, FAIL, "; ".join(near_misses[:3]))
    emit(CID, FAIL,
         "no container-level view: no .dsl workspace and no Markdown "
         "Building Block View or Container diagram heading")


if __name__ == "__main__":
    main()
