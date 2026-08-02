#!/usr/bin/env python3
"""Every function in app/billing.py must be 30 lines or fewer.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c3_function_length"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c3_function_length.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


LIMIT = 30


def main():
    import ast
    scratch = scratch_dir()
    module = scratch / "app" / "billing.py"
    if not module.is_file():
        emit(False, "app/billing.py is missing from the scratch tree")
    try:
        tree = ast.parse(module.read_text(encoding="utf-8",
                                          errors="replace"))
    except SyntaxError as exc:
        emit(False, "app/billing.py does not parse: %s" % exc)
    over = []
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            count += 1
            length = node.end_lineno - node.lineno + 1
            if length > LIMIT:
                over.append("%s: %d lines" % (node.name, length))
    if not count:
        emit(False, "no functions found in app/billing.py")
    if over:
        emit(False, "functions over the %d line limit: %s"
             % (LIMIT, ", ".join(over)))
    emit(True, "all %d functions are %d lines or fewer" % (count, LIMIT))


if __name__ == "__main__":
    main()
