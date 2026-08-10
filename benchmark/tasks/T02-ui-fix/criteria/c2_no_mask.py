#!/usr/bin/env python3
"""The overflow must not be masked on html, body or the universal selector.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_no_mask"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_no_mask.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _parse_rules(css):
    """Return (selector, body, in_media) for every non-at rule."""
    import re
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules = []
    stack = []
    buf = ""
    for ch in css:
        if ch == "{":
            stack.append(buf.strip())
            buf = ""
        elif ch == "}":
            if stack:
                sel = stack.pop()
                in_media = any(s.startswith("@media") for s in stack)
                if sel and not sel.startswith("@"):
                    rules.append((sel, buf, in_media))
            buf = ""
        else:
            buf += ch
    return rules


MASK_SELECTORS = {"html", "body", "*", ":root"}


def main():
    import re
    scratch = scratch_dir()
    offenders = []
    for path in sorted(scratch.rglob("*.css")):
        if ".git" in path.parts:
            continue
        rules = _parse_rules(path.read_text(encoding="utf-8",
                                            errors="replace"))
        for sel, body, _ in rules:
            parts = {p.strip() for p in sel.split(",")}
            if not (parts & MASK_SELECTORS):
                continue
            if re.search(r"overflow(?:-x)?\s*:\s*(hidden|clip)", body):
                offenders.append("%s in %s" % (sel, path.name))
    for path in sorted(scratch.rglob("*.html")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"<(html|body)[^>]*style=\"[^\"]*overflow[^\"]*hidden",
                     text, flags=re.I):
            offenders.append("inline style in %s" % path.name)
    if offenders:
        emit(False, "overflow mask added: %s" % "; ".join(offenders))
    emit(True, "no overflow mask on html, body or the universal selector")


if __name__ == "__main__":
    main()
