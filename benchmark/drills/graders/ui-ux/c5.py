#!/usr/bin/env python3
"""Criterion 5: six WebAIM failure classes, each asserted on its own.

Two questions. Are there six separate assertions, one per class, which
is read from the test names. And does each of them actually bite,
which is read by breaking that one thing on a copy of the tree and
requiring the suite to go red.

The six probes are the failures themselves, in their plainest form: an
image with no alternative, a field with no label, a link with no text,
a button with no text, a page with no declared language, and a palette
flattened to one colour so no pair can reach any contrast ratio. A
suite that stays green under one of those is not asserting that class,
whatever its test is called.

Every probe runs on a copy. The delivered tree is never written to.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SURFACES, emit, green_suite,  # noqa: E402
                     html_pages, iter_files, read, rel, run_build,
                     scratch_dir, short, suite_fails_with, token_source)

CID = "c5"

CLASSES = (
    ("contrast", ("contrast",)),
    ("image alt text", ("alt", "image")),
    ("form labels", ("label",)),
    ("empty links", ("link",)),
    ("empty buttons", ("button",)),
    ("page language", ("lang", "language")),
)

TEST_NAME = re.compile(
    r"""(?:^\s*(?:async\s+)?def\s+(test\w+)|"""
    r"""\b(?:it|test)\s*\(\s*['"]([^'"]+)['"])""", re.M)

PROBE_MARK = "drill-probe"


def test_names(scratch):
    names = []
    for path in iter_files(scratch, exts={".py", ".js", ".mjs", ".ts"}):
        parts = [p.lower() for p in path.relative_to(scratch).parts]
        if not any("test" in p or "spec" in p for p in parts):
            continue
        for match in TEST_NAME.finditer(read(path)):
            label = match.group(1) or match.group(2) or ""
            if label:
                names.append((rel(scratch, path), label.lower()))
    return names


def surface_page(tree):
    for name in SURFACES:
        pages = html_pages(tree, name)
        if pages:
            return pages[0]
    return None


def inject(tree, markup):
    page = surface_page(tree)
    if page is None:
        return None
    text = read(page)
    if "</body>" in text:
        text = text.replace("</body>", "  %s\n</body>" % markup, 1)
    else:
        text = text + "\n" + markup + "\n"
    page.write_text(text, encoding="utf-8")
    run_build(tree)
    return "%s into %s" % (markup, rel(tree, page))


def drop_lang(tree):
    touched = []
    for name in SURFACES:
        for page in html_pages(tree, name):
            text = read(page)
            stripped = re.sub(r"""\slang\s*=\s*['"][^'"]*['"]""", "", text)
            if stripped != text:
                page.write_text(stripped, encoding="utf-8")
                touched.append(rel(tree, page))
    if not touched:
        return None
    run_build(tree)
    return "removed lang from %s" % ", ".join(touched[:3])


def flatten_colour(tree, note):
    """One colour everywhere, so no pair can reach any contrast ratio."""
    flat = "#f4f4f4"
    source = token_source(tree)
    changed = 0
    if source.is_file():
        try:
            doc = json.loads(read(source))
        except ValueError:
            doc = None
        if doc is not None:
            def walk(node):
                nonlocal changed
                if isinstance(node, dict):
                    value = node.get("$value")
                    if isinstance(value, str) and value.strip().startswith("#"):
                        node["$value"] = flat
                        changed += 1
                    for child in node.values():
                        walk(child)
                elif isinstance(node, list):
                    for child in node:
                        walk(child)
            walk(doc)
            if changed:
                source.write_text(json.dumps(doc, indent=2) + "\n",
                                  encoding="utf-8")
    if not changed:
        for path in iter_files(tree, exts={".css", ".scss"}):
            text = read(path)
            flattened = re.sub(r"#[0-9a-fA-F]{3,8}\b", flat, text)
            if flattened != text:
                path.write_text(flattened, encoding="utf-8")
                changed += 1
    if not changed:
        return None
    ok, _, why = run_build(tree)
    if not ok:
        note["build"] = why
        return None
    return "flattened %d colour value(s) to %s" % (changed, flat)


PROBES = (
    ("image alt text",
     lambda tree, note: inject(tree, '<img src="%s.png">' % PROBE_MARK)),
    ("form labels",
     lambda tree, note: inject(
         tree, '<form><input type="text" name="%s"></form>' % PROBE_MARK)),
    ("empty links",
     lambda tree, note: inject(tree, '<a href="/%s"></a>' % PROBE_MARK)),
    ("empty buttons",
     lambda tree, note: inject(tree, '<button type="button"></button>')),
    ("page language", lambda tree, note: drop_lang(tree)),
    ("contrast", flatten_colour),
)


def main():
    scratch = scratch_dir()
    if surface_page(scratch) is None:
        emit(CID, FAIL, "no HTML page under surfaces/service/ or "
                        "surfaces/dashboard/ to assert anything about")

    names = test_names(scratch)
    if not names:
        emit(CID, FAIL, "no tests found: nothing named like a test file "
                        "declares a test")
    unclaimed = []
    claimed = {}
    for label, words in CLASSES:
        hits = [n for _, n in names if any(w in n for w in words)]
        if hits:
            claimed[label] = hits[0]
        else:
            unclaimed.append(label)
    if unclaimed:
        emit(CID, FAIL,
             "%d of the six WebAIM failure classes have no test of their "
             "own: %s. Found %d test(s): %s"
             % (len(unclaimed), ", ".join(unclaimed), len(names),
                ", ".join(sorted({n for _, n in names})[:6])))
    if len(set(claimed.values())) < 6:
        emit(CID, FAIL,
             "the six classes map onto %d distinct test(s), so they are not "
             "individually asserted: %s"
             % (len(set(claimed.values())), sorted(set(claimed.values()))))

    argv, label, why = green_suite(scratch)
    if argv is None:
        emit(CID, FAIL, why)

    survived = []
    for name, probe in PROBES:
        note = {}
        red, what, detail = suite_fails_with(
            scratch, lambda tree, p=probe, n=note: p(tree, n),
            prefix="drill-uiux-c5-")
        if red is None:
            if note.get("build"):
                emit(CID, FAIL,
                     "the %s probe could not be applied because the tree "
                     "failed to rebuild after it: %s"
                     % (name, short(note["build"])))
            emit(CID, FAIL,
                 "the %s probe could not be applied: %s" % (name, detail))
        if not red:
            survived.append(name)

    if survived:
        emit(CID, FAIL,
             "the suite stays green after %s injected into a delivered page, "
             "so %s %s asserted by any test that runs"
             % (" and ".join(survived), " and ".join(survived),
                "is not" if len(survived) == 1 else "are not"))

    emit(CID, PASS,
         "six named tests (%s) and all six probes turn the suite red: "
         "%s bite" % (", ".join(sorted(set(claimed.values())))[:180],
                      ", ".join(n for n, _ in PROBES)))


if __name__ == "__main__":
    main()
