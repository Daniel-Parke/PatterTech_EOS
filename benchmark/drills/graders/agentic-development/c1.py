#!/usr/bin/env python3
"""Criterion 1: front-matter with summary, type and tags including eos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, parse_front_matter,  # noqa: E402
                     require_output, split_front_matter)

CID = "c1"


def main():
    _, rel, raw, _ = require_output(CID)
    block, _body = split_front_matter(raw)
    if block is None:
        emit(CID, FAIL,
             "%s has no front-matter block: the file must open with a line "
             "of three dashes and close the block with another" % rel)

    data = parse_front_matter(block)
    problems = []
    for key in ("summary", "type"):
        value = data.get(key)
        if not value or not str(value).strip():
            problems.append("%s is missing or empty" % key)

    tags = data.get("tags")
    if tags is None:
        problems.append("tags is missing")
    elif not isinstance(tags, list):
        problems.append("tags is not a list: found %r" % tags)
    elif not any(str(t).strip().lower() == "eos" for t in tags):
        problems.append("tags does not contain eos: found %s"
                        % ", ".join(str(t) for t in tags))

    if problems:
        emit(CID, FAIL, "%s: %s" % (rel, "; ".join(problems)))
    emit(CID, PASS,
         "%s carries summary, type=%s and tags %s"
         % (rel, data.get("type"), data.get("tags")))


if __name__ == "__main__":
    main()
