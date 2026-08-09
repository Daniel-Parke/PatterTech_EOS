#!/usr/bin/env python3
"""Criterion 7: a states manifest per component, and a test that walks it.

The manifest half is a read: every shared component exports a literal
naming focus, hover, active, disabled, loading and error.

The test half is the interesting one. A test that hard-codes the six
names and asserts six renders looks identical, from the outside, to a
test that walks the manifest, right up until a component adds a state
and nobody notices. So the probe adds a seventh state to one
component's manifest, a state nothing can render, and requires the
suite to go red. Only a test that reads the manifest can fail that.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, STATE_NAMES, SURFACES,  # noqa: E402
                     component_files, emit, green_suite, missing_surfaces,
                     outward_references, read, rel, run_build, scratch_dir,
                     shared_module_roots, states_manifest, suite_fails_with)

CID = "c7"

PROBE_STATE = "drillprobe"


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


def add_state(tree):
    for path in shared_components(tree):
        text = read(path)
        whole, inner = states_manifest(text)
        if whole is None:
            continue
        for quote in ('"', "'"):
            needle = "%serror%s" % (quote, quote)
            if needle in whole:
                patched = whole.replace(
                    needle, "%s, %s%s%s" % (needle, quote, PROBE_STATE, quote),
                    1)
                path.write_text(text.replace(whole, patched, 1),
                                encoding="utf-8")
                run_build(tree)
                return "added a seventh state to the manifest in %s" \
                    % rel(tree, path)
    return None


def main():
    scratch = scratch_dir()
    absent = missing_surfaces(scratch)
    if absent:
        emit(CID, FAIL, "no surface at %s"
             % ", ".join("surfaces/%s/" % n for n in absent))

    components = shared_components(scratch)
    if not components:
        emit(CID, FAIL,
             "no shared component found, so there is no states manifest to "
             "look for")

    missing = []
    for path in components:
        text = read(path)
        whole, inner = states_manifest(text)
        if whole is None:
            absent_states = [s for s in STATE_NAMES
                             if ('"%s"' % s) not in text.lower()
                             and ("'%s'" % s) not in text.lower()]
            missing.append("%s (no manifest naming %s)"
                           % (rel(scratch, path),
                              ", ".join(absent_states) or "all six together"))
    if missing:
        emit(CID, FAIL,
             "%d of %d shared component(s) export no states manifest naming "
             "all six states: %s"
             % (len(missing), len(components), "; ".join(missing[:3])))

    argv, label, why = green_suite(scratch)
    if argv is None:
        emit(CID, FAIL, why)

    red, what, detail = suite_fails_with(scratch, add_state,
                                         prefix="drill-uiux-c7-")
    if red is None:
        emit(CID, FAIL, "the states probe could not be applied: %s" % detail)
    if not red:
        emit(CID, FAIL,
             "the suite stays green after a seventh state was %s, so no test "
             "walks the manifest: the state tests are a hard-coded list and "
             "will not notice a component that grows one" % what)

    emit(CID, PASS,
         "%d shared component(s) export a manifest naming all six states, "
         "and the suite goes red when one manifest grows a state nothing "
         "renders" % len(components))


if __name__ == "__main__":
    main()
