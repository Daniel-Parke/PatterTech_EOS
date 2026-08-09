#!/usr/bin/env python3
"""Criterion 4: no swallowing handler is left in parser.py.

The drill states the check as a grep, so this runs that exact pattern
rather than a cleverer one:

    except\\s*:|except Exception\\s*:\\s*(pass|continue)

Every `parser.py` in the delivered tree is read, because moving the
code into a second module would otherwise retire the criterion.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, parser_files, read,  # noqa: E402
                     rel, scratch_dir)

CID = "c4"

PATTERN = re.compile(r"except\s*:|except Exception\s*:\s*(pass|continue)")


def main():
    scratch = scratch_dir()
    files = parser_files(scratch)
    if not files:
        emit(CID, FAIL, "no parser.py in the delivered tree")

    hits = []
    for path in files:
        text = read(path)
        for match in PATTERN.finditer(text):
            number = text.count("\n", 0, match.start()) + 1
            hits.append("%s:%d: %s"
                        % (rel(scratch, path), number,
                           " ".join(match.group(0).split())))

    if hits:
        emit(CID, FAIL,
             "%d swallowing handler(s) remain: %s"
             % (len(hits), "; ".join(hits[:4])))
    emit(CID, PASS,
         "the grep returns zero matches over %s"
         % ", ".join(rel(scratch, p) for p in files))


if __name__ == "__main__":
    main()
