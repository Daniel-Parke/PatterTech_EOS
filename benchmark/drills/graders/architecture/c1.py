#!/usr/bin/env python3
"""Criterion 1: a boundary contract file exists and parses."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (CONFIG_NAMES, FAIL, PASS, emit, find_config,  # noqa: E402
                     scratch_dir)

CID = "c1"


def main():
    scratch = scratch_dir()
    present = [n for n in CONFIG_NAMES if (scratch / n).is_file()]
    path, sections = find_config(scratch)
    if path is None:
        if present:
            emit(CID, FAIL,
                 "found %s but no parseable import-linter configuration in "
                 "it" % ", ".join(present))
        emit(CID, FAIL,
             "no boundary contract file: looked for %s"
             % ", ".join(CONFIG_NAMES))
    emit(CID, PASS,
         "%s parses and carries %d import-linter section(s)"
         % (path.name, len(sections)))


if __name__ == "__main__":
    main()
