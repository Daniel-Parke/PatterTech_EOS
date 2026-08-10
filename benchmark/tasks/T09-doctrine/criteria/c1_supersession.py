#!/usr/bin/env python3
"""The stale guidance must be superseded bidirectionally, not deleted.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_supersession"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_supersession.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


STALE = "responsive variants are not worth the build cost"
IMAGES = "doctrine/mini/guidance/IMAGES.md"


def _front_matter(text):
    import re
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", lines[i])
        if m:
            fm[m.group(1)] = m.group(2).strip()
        i += 1
    return fm


def _norm(value):
    return value.strip().strip("`'\"").replace("\\", "/").lstrip("./")


def main():
    scratch = scratch_dir()
    files = {}
    for path in sorted(scratch.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(scratch).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        files[rel] = (_front_matter(text), text)
    if IMAGES not in files:
        emit(False, "%s was deleted; supersession keeps the old file in "
                    "place" % IMAGES)
    stale_active = [rel for rel, (fm, text) in files.items()
                    if STALE in text and not fm.get("superseded_by")]
    if stale_active:
        emit(False, "stale claim still active (no superseded_by) in: %s"
             % ", ".join(stale_active))
    fm_old = files[IMAGES][0]
    target_ref = _norm(fm_old.get("superseded_by", ""))
    if not target_ref:
        emit(False, "%s has no superseded_by in its front-matter" % IMAGES)
    target_rel = None
    for rel in files:
        if rel == target_ref or rel.endswith("/" + target_ref) \
                or Path(rel).name == Path(target_ref).name:
            if rel != IMAGES:
                target_rel = rel
                break
    if target_rel is None:
        emit(False, "superseded_by points at %s, which does not exist"
             % target_ref)
    back_ref = _norm(files[target_rel][0].get("supersedes", ""))
    if not back_ref:
        emit(False, "%s does not carry supersedes back to the old file"
             % target_rel)
    if not (back_ref == IMAGES or IMAGES.endswith("/" + back_ref)
            or Path(back_ref).name == Path(IMAGES).name):
        emit(False, "%s supersedes %s, not the retired guidance"
             % (target_rel, back_ref))
    emit(True, "%s is superseded by %s with a bidirectional link"
         % (IMAGES, target_rel))


if __name__ == "__main__":
    main()
