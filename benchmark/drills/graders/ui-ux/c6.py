#!/usr/bin/env python3
"""Criterion 6: the keyboard tests assert keys, not rendering.

The drill names the failure this catches: keyboard tests that assert a
component rendered and never press a key. So the grader does not read
the tests for good intentions. It renames every key the shared
behaviour layer answers to, on a copy, and requires the suite to go
red. A suite that survives having Escape renamed was not testing
Escape.

The focus half is probed the same way, by rewriting every outline
declaration in the delivered stylesheets to `outline: none`. That is a
source-level reading of what the spec calls computed styles: it settles
whether a test notices focus styling disappearing, which is the part
that fails silently in review. It does not settle what a browser
actually paints, and the reason string says so on a pass.

Every probe runs on a copy. The delivered tree is never written to.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, KEY_NAMES, PASS, SURFACES, component_files,  # noqa: E402
                     emit, green_suite, iter_files, missing_surfaces,
                     outward_references, read, rel, run_build, scratch_dir,
                     shared_module_roots, suite_fails_with)

CID = "c6"

RENAMED = "Meta+Drill"


def shared_components(scratch):
    roots = {}
    for name in SURFACES:
        roots[name] = shared_module_roots(scratch,
                                          outward_references(scratch, name))
    common = sorted(set(roots["service"]) & set(roots["dashboard"]))
    found = []
    for candidate in common:
        found += component_files(scratch, [Path(scratch) / candidate])
    return sorted(set(found))


def test_files(tree):
    out = []
    for path in iter_files(tree, exts={".py", ".js", ".mjs", ".ts"}):
        parts = [p.lower() for p in path.relative_to(Path(tree)).parts]
        if any("test" in p or "spec" in p for p in parts):
            out.append(path)
    return out


def rename_keys(tree):
    touched, renamed = [], 0
    for path in shared_components(tree):
        text = read(path)
        out = text
        for key in KEY_NAMES:
            for quote in ('"', "'"):
                needle = "%s%s%s" % (quote, key, quote)
                if needle in out:
                    out = out.replace(needle, "%s%s%s"
                                      % (quote, RENAMED, quote))
                    renamed += 1
        if out != text:
            path.write_text(out, encoding="utf-8")
            touched.append(rel(tree, path))
    if not touched:
        return None
    run_build(tree)
    return "renamed %d key literal(s) in %s" % (renamed, ", ".join(touched[:3]))


PY_HANDLER = re.compile(
    r"^([ \t]*)def\s+(on_key|onkey|on_keydown|handle_key|handlekey|press)"
    r"\s*\(\s*([^)]*)\)\s*:[ \t]*\n", re.M | re.I)
JS_HANDLER = re.compile(
    r"^([ \t]*)(?:export\s+)?function\s+"
    r"(onKey|on_key|onKeyDown|handleKey|press)\s*\(\s*([^)]*)\)\s*\{",
    re.M)


def deaden_handlers(tree):
    """Make every key handler a no-op without touching the key maps.

    This is the sharper half of the probe. Renaming the keys catches a
    suite that never presses one, but a test asserting `"Enter" in KEYS`
    also goes red under it while proving nothing about behaviour. An
    early return leaves every declaration in place and takes away only
    the state change, so only a test that pressed a key and looked at
    what happened can notice.
    """
    touched = []
    for path in shared_components(tree):
        text = read(path)

        def first_arg(raw):
            head = raw.split(",")[0].strip().split("=")[0].strip()
            return head if re.match(r"^\w+$", head or "") else "None"

        def py(match):
            return "%s%s%s    return %s\n" % (
                match.group(0), match.group(1), "",
                first_arg(match.group(3)))

        def js(match):
            return "%s\n%s    return %s;" % (
                match.group(0), match.group(1), first_arg(match.group(3)))

        out = PY_HANDLER.sub(py, text)
        out = JS_HANDLER.sub(js, out)
        if out != text:
            path.write_text(out, encoding="utf-8")
            touched.append(rel(tree, path))
    if not touched:
        return None
    run_build(tree)
    return "made the key handler in %s do nothing" % ", ".join(touched[:3])


def blind_focus(tree):
    touched = 0
    for path in iter_files(tree, exts={".css", ".scss"}):
        parts = [p.lower() for p in path.relative_to(Path(tree)).parts]
        if parts[0] in ("dist", "build", "_site", "out"):
            continue
        text = read(path)
        out = re.sub(r"outline\s*:\s*[^;}]+", "outline: none", text)
        if out != text:
            path.write_text(out, encoding="utf-8")
            touched += 1
    if not touched:
        return None
    run_build(tree)
    return "rewrote every outline declaration in %d stylesheet(s) to none" \
        % touched


def main():
    scratch = scratch_dir()
    absent = missing_surfaces(scratch)
    if absent:
        emit(CID, FAIL, "no surface at %s"
             % ", ".join("surfaces/%s/" % n for n in absent))

    components = shared_components(scratch)
    if not components:
        emit(CID, FAIL,
             "no shared interactive component found, so there is no keyboard "
             "contract to test")

    keyed = [p for p in components
             if any(('"%s"' % k) in read(p) or ("'%s'" % k) in read(p)
                    for k in KEY_NAMES)]
    if not keyed:
        emit(CID, FAIL,
             "none of the %d shared component file(s) names a key, so no "
             "component states which keys it answers to"
             % len(components))

    tests = test_files(scratch)
    body = " ".join(read(p).lower() for p in tests)
    untested = [p.stem for p in keyed if p.stem.lower() not in body
                and p.stem.replace("_", "").lower() not in body.replace("_", "")]
    if untested:
        emit(CID, FAIL,
             "no test names %s, so %d of %d interactive component(s) have no "
             "keyboard test at all"
             % (", ".join(untested[:3]), len(untested), len(keyed)))
    if not any("key" in rel(scratch, p).lower() or "key" in read(p).lower()
               for p in tests):
        emit(CID, FAIL, "no test mentions a key at all")

    argv, label, why = green_suite(scratch)
    if argv is None:
        emit(CID, FAIL, why)

    red, what, detail = suite_fails_with(scratch, rename_keys,
                                         prefix="drill-uiux-c6-keys-")
    if red is None:
        emit(CID, FAIL, "the key-renaming probe could not be applied: %s"
                        % detail)
    if not red:
        emit(CID, FAIL,
             "the suite stays green after the shared behaviour layer had "
             "every key renamed (%s), so the keyboard tests assert that a "
             "component rendered and never that a key did anything" % what)

    deadened = "no key handler to neuter, so only the renaming probe ran"
    red, what, detail = suite_fails_with(scratch, deaden_handlers,
                                         prefix="drill-uiux-c6-dead-")
    if red is False:
        emit(CID, FAIL,
             "the suite stays green after %s, so the keyboard tests assert "
             "that the keys are declared and never that pressing one changes "
             "anything" % what)
    if red is True:
        deadened = "and red again when the handler is made a no-op"

    red, what, detail = suite_fails_with(scratch, blind_focus,
                                         prefix="drill-uiux-c6-focus-")
    if red is None:
        emit(CID, FAIL,
             "no stylesheet in the delivered tree declares an outline, so "
             "nothing states a visible focus style (%s)" % detail)
    if not red:
        emit(CID, FAIL,
             "the suite stays green after %s, so no test asserts a visible "
             "focus style" % what)

    emit(CID, PASS,
         "%d interactive component(s) named in the tests; the suite goes red "
         "when the shared keys are renamed, %s, and again when focus outlines "
         "are removed. Focus is read from the delivered stylesheets, not from "
         "a browser's computed styles, which this grader cannot reach"
         % (len(keyed), deadened))


if __name__ == "__main__":
    main()
