#!/usr/bin/env python3
"""Criterion 10: a decision record states versioning and compatibility.

FRAG-14 and FRAG-18. The criterion asks for a parseable line recording
the versioning approach and the compatibility tier, and gives
`compatibility: BACKWARD` as the example, so both facts are looked for
as key and value lines in one record: the tier, and the approach that
tier was reached by.

Markdown decoration is tolerated (list bullets, bold keys, backticked
values) because a record is written for people first, but the line has
to be a key and a value, not a paragraph mentioning both words.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, SKIP_DIRS, emit, read, scratch_dir  # noqa: E402

CID = "c10"

RECORD_NAME = re.compile(
    r"^(decisions?|adr[-_0-9]*.*|[0-9]{3,4}-.*|.*-adr.*)\.(md|markdown)$",
    re.I)
RECORD_DIR = re.compile(r"(^|/)(docs/)?(decisions|adr|adrs|architecture/"
                        r"decisions)(/|$)", re.I)

TIER = (r"backward[_ -]?(compatible|compatibility)?|forward[_ -]?"
        r"(compatible|compatibility)?|full[_ -]?(compatible|compatibility)?|"
        r"backwards[_ -]?compatible|none|breaking|non[_ -]?breaking|"
        r"compatible")
COMPAT_LINE = re.compile(
    r"(?im)^\s*(?:[-*+]\s*)?(?:\*\*|__|`)?\s*"
    r"(compatibility(?:\s*(?:tier|mode|level|policy))?)"
    r"\s*(?:\*\*|__|`)?\s*[:=]\s*(?:\*\*|__|`)?\s*(%s)\b" % TIER)
VERSION_LINE = re.compile(
    r"(?im)^\s*(?:[-*+]\s*)?(?:\*\*|__|`)?\s*"
    r"((?:api[_ -]?)?version(?:ing)?(?:[_ -]?(?:approach|strategy|scheme|"
    r"style|policy|method))?)"
    r"\s*(?:\*\*|__|`)?\s*[:=]\s*(?:\*\*|__|`)?\s*([^\n]{2,60})")


def records(scratch):
    out = []
    for path in sorted(scratch.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".md",
                                                             ".markdown"):
            continue
        rel = path.relative_to(scratch).as_posix()
        if any(part in SKIP_DIRS for part in Path(rel).parts):
            continue
        if RECORD_NAME.match(path.name) or RECORD_DIR.search(
                rel.rsplit("/", 1)[0] if "/" in rel else ""):
            out.append(rel)
    return out


def main():
    scratch = scratch_dir()
    found = records(scratch)
    if not found:
        emit(CID, FAIL,
             "no DECISIONS.md and no ADR file: nothing in the tree records "
             "how the API is versioned or what it promises callers")

    near = []
    for rel in found:
        text = read(scratch / rel)
        compat = COMPAT_LINE.search(text)
        versioning = VERSION_LINE.search(text)
        if compat and versioning:
            emit(CID, PASS,
                 "%s records %s: %s and %s: %s"
                 % (rel, compat.group(1).strip(), compat.group(2).strip(),
                    versioning.group(1).strip(),
                    " ".join(versioning.group(2).split())[:60]))
        missing = []
        if not compat:
            missing.append("no `compatibility: <tier>` line")
        if not versioning:
            missing.append("no `versioning: <approach>` line")
        near.append("%s has %s" % (rel, " and ".join(missing)))

    emit(CID, FAIL,
         "%s; the criterion wants both facts on parseable key and value "
         "lines, for example `compatibility: BACKWARD`" % "; ".join(near[:3]))


if __name__ == "__main__":
    main()
