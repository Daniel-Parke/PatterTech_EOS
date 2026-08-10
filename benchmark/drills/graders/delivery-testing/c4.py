#!/usr/bin/env python3
"""Criterion 4: the new pricing test stays outside the module.

The test that pins the defect has to work through the public function.
A test that reaches a private helper, or patches something inside
`pricing`, pins today's implementation rather than the behaviour, and
the next refactor breaks it for no reason.

"The new test" is taken to be every test file that is new or changed
against the shipped scenario and that reaches the pricing module. If
there is no such file there is nothing to inspect and nothing was
delivered, which is a fail rather than a vacuous pass.
"""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PRICING_MODULE, changed_files,  # noqa: E402
                     dotted, emit, parse, relative, scratch_dir,
                     touches_module)

CID = "c4"

SETTERS = ("setattr", "setitem", "delattr", "delitem")
PATCHERS = ("patch", "object", "dict")


def _is_patcher(func):
    """Does this call replace an attribute somewhere, by any spelling?

    Covers `monkeypatch.setattr`, the builtin `setattr`, `mock.patch`,
    `patch.object` and `patch.dict`. The point is not to enumerate
    every library but to catch a test that swaps something out inside
    the module under test.
    """
    short = func.split(".")[-1]
    if short in SETTERS:
        return True
    return short in PATCHERS and ("patch" in func or "mock" in func)


def _names_pricing(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value == PRICING_MODULE or \
            node.value.startswith(PRICING_MODULE + ".")
    name = dotted(node)
    return name == PRICING_MODULE or name.startswith(PRICING_MODULE + ".")


def findings_in(path, tree, rel):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == PRICING_MODULE:
            for alias in node.names:
                if alias.name.startswith("_"):
                    out.append("%s imports the private name %s from %s"
                               % (rel, alias.name, PRICING_MODULE))
        if isinstance(node, ast.Attribute):
            name = dotted(node)
            if name.startswith(PRICING_MODULE + ".") and \
                    name.split(".")[-1].startswith("_"):
                out.append("%s reaches %s, a private name inside the module"
                           % (rel, name))
        if isinstance(node, ast.Call):
            func = dotted(node.func)
            short = func.split(".")[-1]
            if _is_patcher(func) and node.args and \
                    _names_pricing(node.args[0]):
                out.append("%s patches inside %s with %s(...)"
                           % (rel, PRICING_MODULE, func or short))
            elif short == "getattr" and len(node.args) >= 2 and \
                    _names_pricing(node.args[0]) and \
                    isinstance(node.args[1], ast.Constant) and \
                    str(node.args[1].value).startswith("_"):
                out.append("%s pulls the private name %r out of %s with "
                           "getattr" % (rel, node.args[1].value,
                                        PRICING_MODULE))
    return out


def main():
    scratch = scratch_dir()

    candidates = []
    for path in changed_files(scratch, ".py"):
        name = path.name
        if not (name.startswith("test_") or name.endswith("_test.py")):
            continue
        tree = parse(path)
        if tree is None:
            emit(CID, FAIL, "%s does not parse" % relative(scratch, path))
        if touches_module(tree, PRICING_MODULE):
            candidates.append((path, tree))

    if not candidates:
        emit(CID, FAIL,
             "no new or changed test file reaches the pricing module, so "
             "there is no regression test to inspect")

    problems = []
    for path, tree in candidates:
        problems.extend(findings_in(path, tree, relative(scratch, path)))

    if problems:
        emit(CID, FAIL, "; ".join(problems[:4]))
    emit(CID, PASS,
         "%s uses the public pricing function only: no private name, no "
         "patching inside the module"
         % ", ".join(relative(scratch, p) for p, _ in candidates))


if __name__ == "__main__":
    main()
