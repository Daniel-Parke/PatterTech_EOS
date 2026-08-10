#!/usr/bin/env python3
"""Criterion 7: the flake is fixed by controlling time, not by retrying.

Three things have to hold, and the criterion needs all three.

- No retry machinery was added. `flaky`, `rerun`, `retries` and
  `--reruns` are counted in code and config, never in prose: comments
  and Python string literals are skipped and Markdown is left alone, so
  a note in a docstring saying reruns were deliberately avoided does
  not read as a rerun being added.
- The schedule tests supply the clock. Every function in the shipped
  `scheduling.py` that takes a `now` argument has to be called with one,
  unless the test file freezes or patches time some other way. A test
  that still reads the ambient clock and only loosens its assertion has
  not controlled anything, and would sail through a repeat run.
- The schedule tests pass twenty runs in a row.

The repeat run alone would leave about one untouched tree in three
hundred looking fixed, so it is the third check here rather than the
only one.
"""

import ast
import io
import shutil
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, PRISTINE, SCHEDULE_TEST,  # noqa: E402
                     SCHEDULING_MODULE, copy_tree, dotted, emit, parse,
                     read, relative, require_pytest, run_pytest,
                     scratch_dir, tail, test_files, touches_module)

CID = "c7"
RUNS = 20

TOKENS = ("flaky", "rerun", "retries", "--reruns")
CODE_SUFFIXES = (".py", ".toml", ".cfg", ".ini", ".txt", ".yml", ".yaml",
                 ".json", ".sh")
CONTROL_HINTS = ("freeze_time", "freezegun", "time_machine", "time-machine",
                 "monkeypatch.setattr", "mock.patch", "patch.object",
                 "FakeClock", "fake_clock", "frozen_time")


def code_text(path):
    """A file's content with comments and Python strings taken out."""
    if path.suffix != ".py":
        return read(path)
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(read(path)).readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            out.append(tok.string)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return read(path)
    return " ".join(out)


def retry_additions(tree):
    hits = []
    for path in Path(tree).rglob("*"):
        if not path.is_file() or path.suffix not in CODE_SUFFIXES:
            continue
        if any(p in (".git", "__pycache__", ".drill") for p in path.parts):
            continue
        lowered = code_text(path).lower()
        for token in TOKENS:
            if token in lowered:
                hits.append("%s in %s" % (token, relative(tree, path)))
    return hits


def clock_parameters(path):
    """{function name: index of its `now` argument} for a module."""
    node = parse(path)
    out = {}
    if node is None:
        return out
    for sub in ast.walk(node):
        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names = [a.arg for a in sub.args.args]
            if "now" in names:
                out[sub.name] = names.index("now")
    return out


def schedule_tests(scratch):
    """The delivered test files that stand in for tests/test_schedule.py."""
    named = scratch / SCHEDULE_TEST
    if named.is_file():
        return [named]
    by_name = [p for p in test_files(scratch) if "schedule" in p.name]
    if by_name:
        return by_name
    out = []
    for path in test_files(scratch):
        node = parse(path)
        if node is not None and touches_module(node, SCHEDULING_MODULE):
            out.append(path)
    return out


def uncontrolled_calls(path, clocks):
    node = parse(path)
    if node is None:
        return ["%s does not parse" % path.name]
    bad = []
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        name = dotted(sub.func).split(".")[-1]
        if name not in clocks:
            continue
        index = clocks[name]
        if any(kw.arg == "now" for kw in sub.keywords):
            continue
        if len(sub.args) > index:
            continue
        bad.append("%s(...) on line %d takes a `now` argument and was not "
                   "given one" % (name, sub.lineno))
    return bad


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    added = retry_additions(scratch)
    if added:
        emit(CID, FAIL,
             "retry machinery was added rather than the clock controlled: %s"
             % "; ".join(sorted(set(added))[:4]))

    targets = schedule_tests(scratch)
    if not targets:
        emit(CID, FAIL,
             "no schedule test survives in the delivered tree; deleting the "
             "flaky test is not fixing it")

    clocks = clock_parameters(PRISTINE / (SCHEDULING_MODULE + ".py"))
    for path in targets:
        text = read(path)
        if any(hint in text for hint in CONTROL_HINTS):
            continue
        bad = uncontrolled_calls(path, clocks)
        if bad:
            emit(CID, FAIL,
                 "%s still reads the ambient clock: %s"
                 % (relative(scratch, path), "; ".join(bad[:3])))

    work, copy = copy_tree(scratch, "drill-dt-c7-")
    try:
        paths = [relative(scratch, p) for p in targets]
        for attempt in range(1, RUNS + 1):
            code, output = run_pytest(copy, *paths)
            if code is None:
                emit(CID, FAIL, "could not run the schedule tests: %s"
                                % tail(output))
            if code == 5:
                emit(CID, FAIL, "the schedule tests collected nothing: %s"
                                % ", ".join(paths))
            if code != 0:
                emit(CID, FAIL,
                     "%s exits %d on run %d of %d: %s"
                     % (", ".join(paths), code, attempt, RUNS, tail(output)))
        emit(CID, PASS,
             "%s supplies its own clock, adds no retry machinery and passes "
             "%d runs in a row" % (", ".join(paths), RUNS))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
