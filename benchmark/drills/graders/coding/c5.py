#!/usr/bin/env python3
"""Criterion 5: one exception name, spelled the same in three places.

The drill asks for string equality, not synonyms: the name callers are
told to catch must appear in `parser.py`, in a test that asserts the
raise, and in `README.md`, character for character.

Candidate names are taken from `parser.py` by structure, so the grader
never has to guess which word is the exception: classes defined there
that inherit from something exception shaped, names that appear in a
`raise`, and anything spelled `*Error` or `*Exception` in the module
docstring, which covers a module that documents a builtin rather than
declaring its own.
"""

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, parser_files, read,  # noqa: E402
                     rel, scratch_dir, test_files)

CID = "c5"

EXC_SHAPED = re.compile(r"\b([A-Z][A-Za-z0-9_]*(?:Error|Exception|Warning))\b")
BUILTINS = ("ValueError", "TypeError", "KeyError", "RuntimeError",
            "ArithmeticError", "LookupError", "Exception")


def candidate_names(text):
    """Exception names `parser.py` puts in front of a caller."""
    names = set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None

    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    bases.append(ast.unparse(base)
                                 if hasattr(ast, "unparse") else "")
                joined = " ".join(bases)
                if "Error" in joined or "Exception" in joined:
                    names.add(node.name)
            elif isinstance(node, ast.Raise) and node.exc is not None:
                target = node.exc
                if isinstance(target, ast.Call):
                    target = target.func
                if isinstance(target, ast.Name):
                    names.add(target.id)
                elif isinstance(target, ast.Attribute):
                    names.add(target.attr)
        doc = ast.get_docstring(tree) or ""
    else:
        doc = ""

    for match in EXC_SHAPED.finditer(doc):
        names.add(match.group(1))
    for name in BUILTINS:
        if re.search(r"\b%s\b" % name, doc):
            names.add(name)
    return names


def mentions(text, name):
    return re.search(r"\b%s\b" % re.escape(name), text) is not None


def main():
    scratch = scratch_dir()
    files = parser_files(scratch)
    if not files:
        emit(CID, FAIL, "no parser.py in the delivered tree")

    names = set()
    for path in files:
        names |= candidate_names(read(path))
    if not names:
        emit(CID, FAIL,
             "parser.py names no exception type: it defines none, raises "
             "none and its docstring names none, so callers are not told "
             "what to catch")

    readme = None
    for path in scratch.glob("*.md"):
        if path.name.lower() == "readme.md":
            readme = path
            break
    if readme is None:
        for path in scratch.rglob("README.md"):
            if ".git" not in path.parts:
                readme = path
                break
    if readme is None:
        emit(CID, FAIL, "no README.md in the delivered tree")
    readme_text = read(readme)

    tests = [(rel(scratch, p), read(p)) for p in test_files(scratch)]
    raising = [(name, text) for name, text in tests
               if "raises" in text or "assertRaises" in text]
    if not raising:
        emit(CID, FAIL,
             "no test asserts a raise, so the criterion's third place to "
             "check does not exist")

    misses = []
    for name in sorted(names):
        in_test = [n for n, text in raising if mentions(text, name)]
        in_readme = mentions(readme_text, name)
        if in_test and in_readme:
            emit(CID, PASS,
                 "%r appears in parser.py, in %s and in %s, spelled the same "
                 "in all three" % (name, in_test[0], rel(scratch, readme)))
        where = []
        if not in_test:
            where.append("no raising test")
        if not in_readme:
            where.append(rel(scratch, readme))
        misses.append("%s: missing from %s" % (name, " and ".join(where)))

    emit(CID, FAIL,
         "parser.py names %s, but no single name carries across all three "
         "places (%s)"
         % (", ".join(sorted(names)), "; ".join(misses[:4])))


if __name__ == "__main__":
    main()
