#!/usr/bin/env python3
"""Criterion 5: the accessibility audit, and what a script can honestly
settle about it.

Read the criterion's own three sentences separately, because they are
not equally checkable from here.

1. "Automated platform accessibility audit runs in the test suite over
   every screen and fails on any violation." Running a real platform
   audit needs an emulator, a device and the platform test runner. This
   grader does not have those. What it can settle is whether an audit is
   wired into the suite at all, and it fails a tree where nothing is.
2. "Every item it cannot decide appears in A11Y_MANUAL.md with a written
   verdict, and that file's count equals the audit's undecided count."
   The equality is only checkable when the audit leaves a machine
   readable record of what it could not decide. Where one is in the
   tree, the counts are compared and a mismatch fails. Where none is,
   the grader says so in its reason rather than passing silently over
   it.
3. "A static check asserts no unlabelled interactive element and
   explicit marking of decoration." This one is fully settleable and is
   the part with teeth: every screen is scanned, every control has to
   carry a name or contain one, and every image has to be marked one way
   or the other.

So a pass here means parts 2 and 3 hold and part 1 exists, not that a
platform audit was watched running green. The reason string says which.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_named, has_prop,  # noqa: E402
                     iter_files, jsx_elements, read, rel, scratch_dir)

CID = "c5"

MANUAL_FILE = "A11Y_MANUAL.md"

SOURCE = {".js", ".jsx", ".ts", ".tsx"}
TEST_NAME = re.compile(r"(\.|[-_])test\.(c|m)?jsx?$|(\.|[-_])test\.tsx?$",
                       re.I)
RN_IMPORT = re.compile(r"""from\s+['"]react-native['"]""")

INTERACTIVE = {"Pressable", "TouchableOpacity", "TouchableHighlight",
               "TouchableWithoutFeedback", "TouchableNativeFeedback",
               "Button", "Switch", "TextInput", "Slider", "Picker",
               "SegmentedControl"}
DECORATIVE = {"Image", "ImageBackground", "Svg", "Icon"}

LABEL_PROPS = ("accessibilityLabel", "aria-label", "accessibilityLabelledBy",
               "aria-labelledby", "title")
MARKING_PROPS = ("accessibilityLabel", "aria-label", "alt", "aria-hidden",
                 "accessibilityElementsHidden", "importantForAccessibility",
                 "accessibilityRole", "role", "accessible")

HEADING_ITEM = re.compile(r"^#{3,6}\s+\S")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s+\S|\d+[.)]\s+\S)")
AUDIT_WORD = re.compile(r"accessib|a11y", re.I)


def screens(scratch):
    out = []
    for path in iter_files(scratch, suffixes=SOURCE):
        name = path.relative_to(scratch).as_posix()
        if TEST_NAME.search(name):
            continue
        text = read(path)
        if RN_IMPORT.search(text):
            out.append((name, text))
    return out


def violations(scratch):
    unlabelled, unmarked = [], []
    for name, text in screens(scratch):
        for tag, attrs, body in jsx_elements(text):
            if tag in INTERACTIVE:
                labelled = any(has_prop(attrs, p) for p in LABEL_PROPS)
                if not labelled and "<Text" not in body:
                    unlabelled.append("%s <%s>" % (name, tag))
            if tag in DECORATIVE:
                if not any(has_prop(attrs, p) for p in MARKING_PROPS):
                    unmarked.append("%s <%s>" % (name, tag))
    return unlabelled, unmarked


def audit_in_suite(scratch):
    found = []
    for path in iter_files(scratch, suffixes=SOURCE | {".mjs", ".cjs"}):
        name = path.relative_to(scratch).as_posix()
        if not TEST_NAME.search(name):
            continue
        if AUDIT_WORD.search(read(path)):
            found.append(name)
    return found


def undecided_counts(scratch):
    """Machine readable records of what an audit could not decide."""
    found = []
    for path in iter_files(scratch, suffixes={".json"}):
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        stack = [doc]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                for key, value in node.items():
                    if str(key).lower() in ("undecided", "needs_review",
                                            "needsreview", "manual"):
                        if isinstance(value, list):
                            found.append((rel(scratch, path), len(value)))
                        elif isinstance(value, int):
                            found.append((rel(scratch, path), value))
                    stack.append(value)
            elif isinstance(node, list):
                stack.extend(node)
    return found


def main():
    scratch = scratch_dir()

    found = screens(scratch)
    if not found:
        emit(CID, FAIL,
             "no screen source found: nothing in the tree imports from "
             "react-native, so there are no screens to audit")

    unlabelled, unmarked = violations(scratch)
    if unlabelled or unmarked:
        parts = []
        if unlabelled:
            parts.append("%d interactive element(s) with no name and no text "
                         "inside them (%s)"
                         % (len(unlabelled), "; ".join(unlabelled[:4])))
        if unmarked:
            parts.append("%d image(s) marked neither meaningful nor "
                         "decorative (%s)"
                         % (len(unmarked), "; ".join(unmarked[:4])))
        emit(CID, FAIL,
             "the static check finds %s across %d screen file(s)"
             % (", and ".join(parts), len(found)))

    audits = audit_in_suite(scratch)
    if not audits:
        emit(CID, FAIL,
             "the %d screen file(s) pass the static check, but no test in "
             "the suite mentions accessibility at all, so nothing audits "
             "them" % len(found))

    manual = find_named(scratch, MANUAL_FILE)
    if not manual:
        emit(CID, FAIL,
             "no %s, so whatever the audit could not decide has no written "
             "verdict" % MANUAL_FILE)
    text = read(manual[0])
    # One item per third-level heading where the file is written that
    # way, and one per bullet otherwise. Counting both would double
    # every item in a file that gives each one a heading and a list.
    items = [line for line in text.splitlines() if HEADING_ITEM.match(line)]
    if not items:
        items = [line for line in text.splitlines() if LIST_ITEM.match(line)]
    if not items:
        emit(CID, FAIL,
             "%s lists no items" % rel(scratch, manual[0]))
    if "verdict" not in text.lower():
        emit(CID, FAIL,
             "%s lists %d item(s) and records no verdict on any of them; the "
             "criterion asks for a written verdict, not a list of things to "
             "look at" % (rel(scratch, manual[0]), len(items)))

    counts = undecided_counts(scratch)
    matched = [c for c in counts if c[1] == len(items)]
    if counts and not matched:
        emit(CID, FAIL,
             "%s carries %d item(s) and the audit record says %s; the "
             "criterion is that the two counts are equal"
             % (rel(scratch, manual[0]), len(items),
                ", ".join("%d in %s" % (n, where) for where, n in counts[:3])))

    tail = ("its count matches the audit record in %s" % matched[0][0]
            if matched else
            "no machine readable audit record of undecided items was found, "
            "so the count could not be compared with one")

    emit(CID, PASS,
         "%d screen file(s) carry a name on every control and an explicit "
         "marking on every image, %s audits them, %s lists %d item(s) with "
         "verdicts, and %s"
         % (len(found), audits[0], rel(scratch, manual[0]), len(items), tail))


if __name__ == "__main__":
    main()
