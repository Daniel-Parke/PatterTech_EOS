#!/usr/bin/env python3
"""Criterion 3: one shared component module, and no forked copies.

Two halves. Both surfaces must reach for interactive components at the
same path outside themselves, and neither surface may carry a component
implementation of its own.

What counts as a reference is deliberately broad: a Python import, a JS
import or require, a module script tag, a stylesheet link. What counts
as a component implementation inside a surface is deliberately narrow,
because a page needs some glue and calling that a forked component
would be a finding invented by the grader. A surface file is a
component implementation when it exports the six-state manifest, when
it defines a custom element, when it handles two or more named keys
inside a function of its own, or when its name collides with a
component in the shared module.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, KEY_NAMES, PASS, SURFACES, component_files,  # noqa: E402
                     emit, missing_surfaces, outward_references, read, rel,
                     scratch_dir, shared_module_roots, states_manifest,
                     surface_files)

CID = "c3"

DEFINES = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?"
                     r"(?:def|class|function|const|let|var)\s+\w+", re.M)
CUSTOM_ELEMENT = re.compile(r"customElements\.define")
CODE_EXTS = {".py", ".js", ".mjs", ".ts", ".jsx", ".tsx"}


def surface_component_implementations(scratch, name, shared_names):
    """Files inside one surface that implement a component themselves."""
    found = []
    for path in surface_files(scratch, name):
        text = read(path)
        where = rel(scratch, path)
        if path.suffix.lower() in CODE_EXTS and path.stem in shared_names:
            found.append("%s duplicates the shared component %s"
                         % (where, path.stem))
            continue
        if states_manifest(text)[0] is not None:
            found.append("%s exports its own states manifest" % where)
            continue
        if CUSTOM_ELEMENT.search(text):
            found.append("%s defines a custom element" % where)
            continue
        keys = [k for k in KEY_NAMES
                if ('"%s"' % k) in text or ("'%s'" % k) in text]
        if len(keys) >= 2 and DEFINES.search(text):
            found.append("%s handles %s in a function of its own"
                         % (where, ", ".join(keys[:3])))
    return found


def main():
    scratch = scratch_dir()
    absent = missing_surfaces(scratch)
    if absent:
        emit(CID, FAIL, "no surface at %s"
             % ", ".join("surfaces/%s/" % n for n in absent))

    roots, refs = {}, {}
    for name in SURFACES:
        refs[name] = outward_references(scratch, name)
        roots[name] = shared_module_roots(scratch, refs[name])

    shared = {}
    for candidate in sorted(set(roots["service"]) & set(roots["dashboard"])):
        files = component_files(scratch, [Path(scratch) / candidate])
        if files:
            shared[candidate] = files
    if not shared:
        reached = {n: sorted(roots[n]) for n in SURFACES}
        emit(CID, FAIL,
             "the two surfaces share no component module: service reaches "
             "%s and dashboard reaches %s, and no directory both reach holds "
             "a component"
             % (reached["service"] or "nothing outside itself",
                reached["dashboard"] or "nothing outside itself"))
    if len(shared) > 1:
        emit(CID, FAIL,
             "components come from %d shared paths (%s); the criterion asks "
             "for one" % (len(shared), ", ".join(sorted(shared))))

    root = list(shared)[0]
    components = shared[root]
    shared_names = {p.stem for p in components}

    per_surface = {}
    for name in SURFACES:
        used = sorted(p.stem for p in components if p.resolve() in refs[name])
        per_surface[name] = used
        if not used:
            emit(CID, FAIL,
                 "surfaces/%s/ does not import any component from %s/, so "
                 "the two surfaces do not in fact share one module"
                 % (name, root))

    duplicates = []
    for name in SURFACES:
        duplicates += surface_component_implementations(scratch, name,
                                                        shared_names)
    if duplicates:
        emit(CID, FAIL,
             "%d component implementation(s) inside the surfaces: %s"
             % (len(duplicates), "; ".join(duplicates[:3])))

    emit(CID, PASS,
         "both surfaces import components from %s/ (%d component file(s)); "
         "service uses %s, dashboard uses %s, and neither surface implements "
         "a component of its own"
         % (root, len(components), ", ".join(per_surface["service"]),
            ", ".join(per_surface["dashboard"])))


if __name__ == "__main__":
    main()
