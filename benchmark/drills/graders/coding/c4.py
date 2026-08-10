#!/usr/bin/env python3
"""Criterion 4: no handler in parser.py swallows an error.

The drill writes the check as a grep:

    except\\s*:|except Exception\\s*:\\s*(pass|continue)

That pattern is run first and unchanged, because it is what the frozen
spec says. It is not the whole criterion, though: it is one spelling of
a property, and the property is that no handler in `parser.py` catches
an error and does nothing with it. `except ValueError: continue` passes
the grep and swallows exactly as hard as the bare `except:` the fixture
ships, so the tree the grep is happy with can still hold the defect.

So the handlers are also read as syntax. A handler is swallowing when
its body does nothing at all: only `pass`, `continue`, `break`, `...` or
a bare string. A handler that re-raises, that wraps and raises, that
calls anything, or that records the bad row for a caller to see later is
left alone, so a tree is free to surface the failure any way it likes.

Every `parser.py` in the delivered tree is read, because moving the code
into a second module would otherwise retire the criterion.
"""

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, parser_files, read,  # noqa: E402
                     rel, scratch_dir)

CID = "c4"

PATTERN = re.compile(r"except\s*:|except Exception\s*:\s*(pass|continue)")

INERT = (ast.Pass, ast.Continue, ast.Break)


def does_nothing(statement):
    """True when this statement leaves no trace of the error anywhere."""
    if isinstance(statement, INERT):
        return True
    if isinstance(statement, ast.Expr):
        value = statement.value
        if isinstance(value, ast.Constant):  # a docstring or `...`
            return True
    return False


def swallowing(text):
    """[(line, source)] for handlers whose body does nothing at all."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    lines = text.splitlines()
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if not all(does_nothing(item) for item in node.body):
            continue
        head = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
        body = lines[node.body[0].lineno - 1].strip() if node.body else ""
        found.append((node.lineno, " ".join(("%s %s" % (head, body)).split())))
    return found


def main():
    scratch = scratch_dir()
    files = parser_files(scratch)
    if not files:
        emit(CID, FAIL, "no parser.py in the delivered tree")

    hits = []
    inert = []
    for path in files:
        text = read(path)
        for match in PATTERN.finditer(text):
            number = text.count("\n", 0, match.start()) + 1
            hits.append("%s:%d: %s"
                        % (rel(scratch, path), number,
                           " ".join(match.group(0).split())))
        for number, source in swallowing(text):
            where = "%s:%d" % (rel(scratch, path), number)
            if any(hit.startswith(where + ":") for hit in hits):
                continue
            inert.append("%s: %s" % (where, source))

    if hits:
        emit(CID, FAIL,
             "%d swallowing handler(s) remain: %s"
             % (len(hits), "; ".join(hits[:4])))
    if inert:
        emit(CID, FAIL,
             "the grep in the spec returns zero matches, but %d handler(s) "
             "catch an error and do nothing with it, which is the same "
             "swallow spelled differently: %s"
             % (len(inert), "; ".join(inert[:4])))
    emit(CID, PASS,
         "the grep returns zero matches over %s, and no handler there catches "
         "an error and does nothing with it"
         % ", ".join(rel(scratch, p) for p in files))


if __name__ == "__main__":
    main()
