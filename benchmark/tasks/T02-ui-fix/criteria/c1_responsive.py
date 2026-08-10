#!/usr/bin/env python3
"""The stats strip must lose its fixed pixel width outside media queries.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c1_responsive"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c1_responsive.py <scratch-dir>")
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


def main():
    import re
    scratch = scratch_dir()
    sheet = scratch / "css" / "styles.css"
    if not sheet.is_file():
        emit(False, "css/styles.css is missing from the scratch tree")
    rules = _parse_rules(sheet.read_text(encoding="utf-8", errors="replace"))
    fixed = []
    for sel, body, in_media in rules:
        if ".hero-stats" not in sel or in_media:
            continue
        for m in re.finditer(r"(?<![-\w])width\s*:\s*([^;]+)", body):
            value = m.group(1).strip()
            if re.match(r"^\d+(?:\.\d+)?px$", value):
                fixed.append("%s { width: %s }" % (sel, value))
    if fixed:
        emit(False, "fixed pixel width still set outside media queries: %s"
             % "; ".join(fixed))
    emit(True, ".hero-stats carries no fixed pixel width outside media "
               "queries")


if __name__ == "__main__":
    main()
