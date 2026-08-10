#!/usr/bin/env python3
"""Criterion 6: no rollback step, and a kill switch that is real.

The grep half is stricter than it looks and softer than it reads. The
criterion says the file contains no rollback step and that a grep
asserts the absence of rollback wording. Taken at the letter, a runbook
saying "there is no rollback on a client, the lever is the flag" fails
for using the word, which would fail exactly the answer the criterion
wants. So a line carrying rollback wording is only a finding when it is
not a denial: "roll back to the previous build" fails, "we cannot roll
back" does not. Every rollback line the grader accepts is named in its
reason, so the judgement is visible rather than buried.

The kill switch half is settled by turning it off. A flag named in the
runbook has to exist in the shipped flag configuration, has to be one
this delivery added rather than one the fixture already carried, has to
be named in a test, and the suite has to stay green with it off. That
last is the criterion's own words: with the flag off, the previous path
still passes its tests.
"""

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, copy_tree, emit,  # noqa: E402
                     find_named, frozen_scenario, iter_files,
                     node_available, read, rel, require_green_suite,
                     run_suite, scratch_dir)

CID = "c6"

RELEASE = "RELEASE.md"

ROLLBACK = re.compile(
    r"roll[ -]?back|roll(?:ed|ing|s)?\s+(?:it\s+)?back|"
    r"revert(?:ing|s|ed)?\s+(?:the\s+)?(?:release|build|version)|"
    r"downgrad(?:e|ing)", re.I)
DENIAL = re.compile(
    r"\b(?:no|not|never|cannot|can't|cannot|without|impossible|instead|"
    r"nothing|none|forbid|refuse|rather than|there is no|do not|don't|"
    r"unavailable|forward[- ]only)\b", re.I)

KILL_SWITCH = re.compile(r"kill[ -]?switch", re.I)

TEST_NAME = re.compile(r"(\.|[-_])test\.(c|m)?jsx?$|(\.|[-_])test\.tsx?$",
                       re.I)
FLAG_PATH = re.compile(r"flag", re.I)
OFF_POSITION = re.compile(r"\bfalse\b|\boff\b|disabl|unreachable", re.I)


def rollback_lines(text):
    """(offending, denied) lines carrying rollback wording."""
    offending, denied = [], []
    for number, line in enumerate(text.splitlines(), 1):
        if not ROLLBACK.search(line):
            continue
        (denied if DENIAL.search(line) else offending).append(
            (number, line.strip()))
    return offending, denied


def flag_files(root):
    return [p for p in iter_files(root, suffixes={".json"})
            if FLAG_PATH.search(p.relative_to(root).as_posix())]


def flag_names(path):
    """Flag names in one configuration file, with where the switch sits.

    Two shapes: a name keyed straight to a boolean, and a name keyed to
    an object carrying `enabled` or `default`.
    """
    try:
        doc = json.loads(read(path))
    except ValueError:
        return {}
    if not isinstance(doc, dict):
        return {}
    out = {}
    for name, value in doc.items():
        if isinstance(value, bool):
            out[name] = (name,)
        elif isinstance(value, dict):
            for key in ("enabled", "default", "on", "value", "active"):
                if isinstance(value.get(key), bool):
                    out[name] = (name, key)
                    break
    return out


def delivered_flags(scratch):
    out = {}
    for path in flag_files(scratch):
        for name, where in flag_names(path).items():
            out.setdefault(name, (path, where))
    return out


def fixture_flags():
    base = frozen_scenario()
    if not base.is_dir():
        return set()
    names = set()
    for path in flag_files(base):
        names |= set(flag_names(path))
    return names


def flag_off_keeps_the_suite_green(scratch, path, where):
    work, tree = copy_tree(scratch, "drill-nat-c6-")
    try:
        require_green_suite(CID, tree, "the kill switch")
        target = tree / path.relative_to(scratch)
        doc = json.loads(read(target))
        node = doc
        for step in where[:-1]:
            node = node[step]
        node[where[-1]] = False
        target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        code, output, counts = run_suite(tree)
        if code == 0:
            return True, ("the suite still passes (%d tests) with the flag "
                          "off" % counts.get("tests", 0))
        return False, ("the suite fails (%d of %d tests) with the flag off, "
                       "so turning the new behaviour off takes the previous "
                       "path down with it: %s"
                       % (counts.get("fail", 0), counts.get("tests", 0),
                          " ".join(output.split())[-240:]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    scratch = scratch_dir()

    found = find_named(scratch, RELEASE)
    if not found:
        emit(CID, FAIL, "no %s in the delivered tree" % RELEASE)
    path = found[0]
    text = read(path)

    offending, denied = rollback_lines(text)
    if offending:
        emit(CID, FAIL,
             "%s carries %d rollback step(s): %s"
             % (rel(scratch, path), len(offending),
                "; ".join("line %d, %r" % row for row in offending[:3])))

    if not KILL_SWITCH.search(text):
        emit(CID, FAIL,
             "%s names no kill switch; with no way back the flag is the "
             "only lever, and the runbook does not mention one"
             % rel(scratch, path))

    delivered = delivered_flags(scratch)
    if not delivered:
        emit(CID, FAIL,
             "%s talks about a kill switch and no flag configuration in the "
             "tree carries one" % rel(scratch, path))

    shipped = fixture_flags()
    named = [n for n in delivered if n in text]
    fresh = [n for n in named if n not in shipped]
    if not named:
        emit(CID, FAIL,
             "%s names none of the %d flag(s) the tree configures (%s), so "
             "the kill switch it promises has no switch"
             % (rel(scratch, path), len(delivered),
                ", ".join(sorted(delivered)[:5])))
    if not fresh:
        emit(CID, FAIL,
             "the only flag(s) %s names (%s) are the ones the project "
             "already had; nothing new was put behind a switch"
             % (rel(scratch, path), ", ".join(sorted(named))))

    flag = sorted(fresh)[0]
    # A test that only switches the flag on is not exercising a kill
    # switch, so a test that also puts it in the off position is
    # reported ahead of one that does not.
    tested = []
    for path in iter_files(scratch):
        name = path.relative_to(scratch).as_posix()
        if not TEST_NAME.search(name):
            continue
        text_of = read(path)
        if flag not in text_of:
            continue
        tested.append((0 if OFF_POSITION.search(text_of) else 1, name))
    tested = [name for _, name in sorted(tested)]
    if not tested:
        emit(CID, FAIL,
             "no test names %r, so nothing exercises the kill switch" % flag)

    note = ("no rollback step (%d denial%s of one), a kill switch on %r, "
            "exercised by %s"
            % (len(denied), "" if len(denied) == 1 else "s", flag, tested[0]))

    if not node_available():
        emit(CID, UNSETTLED,
             "%s, but Node is not installed here so the suite was not run "
             "with the flag off" % note)

    config, where = delivered[flag]
    good, message = flag_off_keeps_the_suite_green(scratch, config, where)
    if not good:
        emit(CID, FAIL, "%s, but %s" % (note, message))
    emit(CID, PASS, "%s, and %s" % (note, message))


if __name__ == "__main__":
    main()
