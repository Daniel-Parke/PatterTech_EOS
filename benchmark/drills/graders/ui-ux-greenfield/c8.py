#!/usr/bin/env python3
"""Criterion 8: the six cheap failure classes each carry their own assertion.

Contrast, image alternative text, form labels, empty links, empty
buttons and declared page language. The word the criterion turns on is
"own": one scanner run that happens to cover all six is not six
assertions, so the grader matches each class to a *distinct* test unit
and fails if two classes can only be satisfied by the same one.

A test unit is a `def test_...` in Python or a `test(...)` or `it(...)`
block in JavaScript, and it must carry an assertion rather than only a
name.

What this settles is that six separate assertions exist and what each
one is about. It does not run them, and a passing verdict here is not a
claim that the surface is free of those six defects; criterion 7 is
where a defect is measured rather than counted.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, read, rel, scratch_dir, walk  # noqa: E402

CID = "c8"

TEST_SUFFIXES = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"}
TEST_DIRS = {"tests", "test", "spec", "specs", "__tests__", "e2e", "checks"}
TEST_NAME = re.compile(r"(^test_|_test$|\.test$|\.spec$|^test$|^conftest$)",
                       re.I)

ASSERT_CUES = ("expect(", "assert", "tobe", "tohave", "toequal", "tocontain",
               "should", "ok(", "equal(")

CLASSES = {
    "contrast": lambda t: "contrast" in t,
    "image alternative text": lambda t: (
        re.search(r"\balt\b|alternative text", t)
        and re.search(r"\bimg\b|\bimage", t)),
    "form labels": lambda t: re.search(r"\blabel", t) and not re.search(
        r"aria-labelledby only", t),
    "empty links": lambda t: (
        re.search(r"\blink|\banchor|querySelectorAll\('a'|\ba\[href", t)
        and re.search(r"empty|\btext\b|accessible name|\bname\b", t)),
    "empty buttons": lambda t: (
        re.search(r"\bbutton", t)
        and re.search(r"empty|\btext\b|accessible name|\bname\b", t)),
    "declared page language": lambda t: (
        re.search(r"\blang\b|language", t)
        and re.search(r"\bhtml\b|document|\bpage\b", t)),
}


def test_files(scratch):
    out = []
    for path in walk(scratch, TEST_SUFFIXES):
        parts = [p.lower() for p in path.parts[:-1]]
        if any(part in TEST_DIRS for part in parts) \
                or TEST_NAME.search(path.stem) \
                or ".spec." in path.name.lower() \
                or ".test." in path.name.lower():
            out.append(path)
    return out


def units(path, text):
    """(name, body) for every test unit in a file."""
    found = []
    if path.suffix.lower() == ".py":
        marks = [m for m in re.finditer(r"^\s*def\s+(test_\w+)\s*\(",
                                        text, re.M)]
    else:
        marks = [m for m in re.finditer(
            r"^\s*(?:async\s+)?(?:test|it)\s*(?:\.\w+)?\s*\(\s*"
            r"[`'\"](.+?)[`'\"]", text, re.M)]
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        found.append((mark.group(1), text[mark.start():end]))
    return found


def assign(classes, candidates, used=None, chosen=None):
    """Match every class to a distinct unit, or return None."""
    used = used or set()
    chosen = chosen or {}
    if not classes:
        return chosen
    head, rest = classes[0], classes[1:]
    for key in candidates.get(head, []):
        if key in used:
            continue
        got = assign(rest, candidates, used | {key},
                     dict(chosen, **{head: key}))
        if got is not None:
            return got
    return None


def main():
    scratch = scratch_dir()
    files = test_files(scratch)
    if not files:
        emit(CID, FAIL,
             "no test file in the delivered tree, so none of the six cheap "
             "failure classes carries an assertion")

    all_units = []
    for path in files:
        text = read(path)
        for name, body in units(path, text):
            blob = (name + " " + body).lower()
            if not any(cue in blob for cue in ASSERT_CUES):
                continue
            all_units.append(("%s::%s" % (rel(scratch, path), name), blob))
    if not all_units:
        emit(CID, FAIL,
             "%d test file(s) but no test unit carrying an assertion"
             % len(files))

    candidates = {}
    for label, matches in CLASSES.items():
        candidates[label] = [key for key, blob in all_units if matches(blob)]

    missing = [label for label in CLASSES if not candidates[label]]
    if missing:
        emit(CID, FAIL,
             "%d of the six classes have no assertion of their own: %s "
             "(%d test unit(s) inspected)"
             % (len(missing), ", ".join(sorted(missing)), len(all_units)))

    order = sorted(CLASSES, key=lambda label: len(candidates[label]))
    match = assign(order, candidates)
    if match is None:
        shared = {label: candidates[label] for label in CLASSES}
        emit(CID, FAIL,
             "the six classes cannot be matched to six distinct assertions; "
             "they collapse onto the same unit(s): %s"
             % "; ".join("%s -> %s" % (k, ", ".join(v[:2]))
                         for k, v in sorted(shared.items())))

    emit(CID, PASS,
         "each of the six classes has its own assertion: %s"
         % "; ".join("%s in %s" % (label, match[label])
                     for label in sorted(match)))


if __name__ == "__main__":
    main()
