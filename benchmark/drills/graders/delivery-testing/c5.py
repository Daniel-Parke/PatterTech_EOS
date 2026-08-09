#!/usr/bin/env python3
"""Criterion 5: a contract suite runs both gateways off one parameter.

A file under `tests/contract/` whose name matches `test_*gateway*.py`,
carrying a parameterisation that reaches both the fake and the real
client class. Both from the same parameterisation is the whole point: a
file with one test for the fake and a separate one for the real client
is two suites that can drift apart, which is the thing being tested for.

Names are resolved through module level definitions, up to three hops,
so `parametrize("g", GATEWAYS)` with `GATEWAYS = [build_fake,
build_real]` and factory functions counts as reaching both. The real
client class is read out of the shipped `gateway.py` rather than hard
coded, so renaming it in the delivery is fine as long as the class the
agent kept is the one under contract.
"""

import ast
import fnmatch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PRISTINE, dotted, emit, parse,  # noqa: E402
                     public_classes, relative, scratch_dir)

CID = "c5"

PATTERN = "tests/contract/test_*gateway*.py"
FAKE_CLASS = "FakeGateway"
HOPS = 3


def contract_files(scratch):
    out = []
    for path in scratch.rglob("*.py"):
        if ".git" in path.parts:
            continue
        rel = relative(scratch, path)
        if fnmatch.fnmatch(rel, PATTERN):
            out.append(path)
    return sorted(out)


def module_level_definitions(tree):
    """name -> the node that defines it, for one hop of resolution."""
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            out[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = node.value
    return out


def symbols_in(node):
    found = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            found.add(sub.id)
        elif isinstance(sub, ast.Attribute):
            found.add(sub.attr)
            name = dotted(sub)
            if name:
                found.update(name.split("."))
        elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            found.update(sub.value.replace(":", ".").split("."))
    return found


def reachable(node, defs):
    found = symbols_in(node)
    for _ in range(HOPS):
        grown = set(found)
        for name in list(found):
            target = defs.get(name)
            if target is not None:
                grown |= symbols_in(target)
        if grown == found:
            break
        found = grown
    return found


def parameterisations(tree):
    """Every parametrize call and every params= fixture in a file."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = dotted(node.func)
        short = func.split(".")[-1]
        if short == "parametrize":
            yield func, node
        elif short == "fixture":
            for kw in node.keywords:
                if kw.arg == "params":
                    yield func, kw.value


def main():
    scratch = scratch_dir()
    real_classes = set(public_classes(PRISTINE / "gateway.py"))
    real_classes |= set(public_classes(scratch / "gateway.py"))
    real_classes.discard(FAKE_CLASS)

    files = contract_files(scratch)
    if not files:
        near = [relative(scratch, p) for p in scratch.rglob("test_*.py")
                if "contract" in relative(scratch, p)]
        emit(CID, FAIL,
             "no contract suite matching %s%s" % (
                 PATTERN,
                 "; nearest: " + ", ".join(sorted(near)[:3]) if near else ""))

    seen = []
    for path in files:
        tree = parse(path)
        if tree is None:
            emit(CID, FAIL, "%s does not parse" % relative(scratch, path))
        defs = module_level_definitions(tree)
        for func, node in parameterisations(tree):
            names = reachable(node, defs)
            hit = sorted(real_classes & names)
            if FAKE_CLASS in names and hit:
                emit(CID, PASS,
                     "%s parameterises %s over %s and %s"
                     % (relative(scratch, path), func or "a fixture",
                        FAKE_CLASS, ", ".join(hit)))
            seen.append("%s in %s reaches %s"
                        % (func or "a params fixture",
                           relative(scratch, path),
                           ", ".join(sorted(names & (real_classes |
                                                     {FAKE_CLASS})))
                           or "neither class"))

    if not seen:
        emit(CID, FAIL,
             "%s exists but carries no parametrize call and no params "
             "fixture" % ", ".join(relative(scratch, p) for p in files))
    emit(CID, FAIL,
         "no single parameterisation reaches both %s and the real client "
         "(%s): %s" % (FAKE_CLASS, ", ".join(sorted(real_classes)) or "none "
                       "found in gateway.py", "; ".join(seen[:3])))


if __name__ == "__main__":
    main()
