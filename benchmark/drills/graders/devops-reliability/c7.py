#!/usr/bin/env python3
"""Criterion 7: the restore drill is evidence, not a paragraph.

`evidence/restore-drill.json` has to carry the eight named keys, and the
script that produced it has to still produce them. The second half is
what stops a hand-written file: the committed script is run in a copy
with the evidence deleted first, and it must put the same key set back.

A script this machine cannot start leaves the criterion unsettled. A
script that runs and does not regenerate the file fails it.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SKIP_DIRS, UNSETTLED, copy_tree,  # noqa: E402
                     emit, path_tokens, read, run, scratch_dir)

CID = "c7"

REQUIRED = ("started_at", "completed_at", "elapsed_seconds", "rto_seconds",
            "rpo_seconds", "rows_validated", "validation_query", "result")
EVIDENCE = "evidence/restore-drill.json"


def scripts(scratch):
    out = []
    for path in sorted(scratch.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(scratch)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() not in (".py", ".sh"):
            continue
        if "restore" in path_tokens(rel) or "restore" in path.name.lower():
            out.append(rel)
    return sorted(out, key=lambda p: (len(p.parts), p.name))


def main():
    scratch = scratch_dir()
    evidence = scratch / EVIDENCE
    if not evidence.is_file():
        found = sorted(p.relative_to(scratch).as_posix()
                       for p in (scratch / "evidence").glob("*")
                       ) if (scratch / "evidence").is_dir() else []
        emit(CID, FAIL,
             "no %s; evidence/ holds %s" % (EVIDENCE,
                                            ", ".join(found) or "nothing"))
    try:
        doc = json.loads(read(evidence))
    except ValueError as exc:
        emit(CID, FAIL, "%s does not parse: %s" % (EVIDENCE, exc))
    if not isinstance(doc, dict):
        emit(CID, FAIL, "%s is not a JSON object" % EVIDENCE)

    missing = [k for k in REQUIRED if k not in doc]
    if missing:
        emit(CID, FAIL,
             "%s is missing %s" % (EVIDENCE, ", ".join(missing)))

    found = scripts(scratch)
    if not found:
        emit(CID, FAIL,
             "%s exists but no restore script is committed, so nothing can "
             "regenerate it" % EVIDENCE)

    work, copy = copy_tree(scratch, "drill-devops-c7-")
    try:
        problems = []
        for rel in found:
            target = copy / EVIDENCE
            if target.is_file():
                target.unlink()
            if rel.suffix.lower() == ".py":
                argv = [sys.executable, rel.as_posix()]
            else:
                if not shutil.which("sh"):
                    problems.append("%s needs sh, which is not on this "
                                    "machine" % rel.as_posix())
                    continue
                argv = ["sh", rel.as_posix()]
            code, output = run(argv, copy, timeout=420)
            if code is None:
                problems.append("%s would not start: %s"
                                % (rel.as_posix(),
                                   " ".join(output.split())[:150]))
                continue
            if not target.is_file():
                problems.append("%s ran (exit %d) and wrote no %s"
                                % (rel.as_posix(), code, EVIDENCE))
                continue
            try:
                again = json.loads(target.read_text(encoding="utf-8"))
            except ValueError as exc:
                problems.append("%s regenerated %s but it does not parse: %s"
                                % (rel.as_posix(), EVIDENCE, exc))
                continue
            if set(again) != set(doc):
                problems.append(
                    "%s regenerated a different key set (%s)"
                    % (rel.as_posix(),
                       ", ".join(sorted(set(again) ^ set(doc)))))
                continue
            emit(CID, PASS,
                 "%s carries all eight keys and %s regenerates the same set "
                 "(result %r, %s rows)"
                 % (EVIDENCE, rel.as_posix(), again.get("result"),
                    again.get("rows_validated")))
        if problems and all("not on this machine" in p for p in problems):
            emit(CID, UNSETTLED, "; ".join(problems))
        emit(CID, FAIL, "; ".join(problems[:3]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
