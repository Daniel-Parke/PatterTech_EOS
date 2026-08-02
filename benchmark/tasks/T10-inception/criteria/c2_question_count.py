#!/usr/bin/env python3
"""Recorded operator questions must not exceed the scripted answers.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_question_count"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_question_count.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


LIMIT = 15


def main():
    import re
    scratch = scratch_dir()
    name_re = re.compile(r"(?i)(question|session|inception|worklog|log)")
    item_re = re.compile(r"^\s*(?:[-*]|\d+[.)])\s.*\?\s*$")
    total = 0
    counted = []
    for path in sorted(scratch.rglob("*.md")):
        parts = path.relative_to(scratch).parts
        if any(p in (".git", "kernel", "inception") for p in parts):
            continue
        if not name_re.search(path.name):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [line for line in text.splitlines() if item_re.match(line)]
        if hits:
            total += len(hits)
            counted.append("%s: %d" % (path.relative_to(scratch).as_posix(),
                                       len(hits)))
    if total > LIMIT:
        emit(False, "%d operator questions recorded, budget %d (%s)"
             % (total, LIMIT, "; ".join(counted)))
    emit(True, "%d operator questions recorded, within the budget of %d"
         % (total, LIMIT))


if __name__ == "__main__":
    main()
