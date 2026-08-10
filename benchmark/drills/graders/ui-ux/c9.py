#!/usr/bin/env python3
"""Criterion 9: the two surfaces measurably differ.

The pluralism claim is only worth something if the surfaces diverge, so
this grader measures rather than reads. For each surface it collects
every stylesheet the surface's pages actually link, resolves the custom
properties those stylesheets define, and reads three things off the
result: the base type size, the set of type steps, and the set of
spacing values. The component inventory comes from what each surface
imports out of the shared module.

Three differences are required, one per measure, plus a stated
threshold somewhere in the written record: the spec asks for the
surfaces to differ *by a stated threshold*, and a repository that
diverges by accident has not stated anything.

The measurement is a source-level one. It reads declared values, not
what an engine computes after the cascade, and a surface that hides its
divergence behind a media query or a runtime class will read as
narrower here than it is.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SURFACES, component_files, emit,  # noqa: E402
                     iter_files, missing_surfaces, outward_references, read,
                     referenced_files, rel, scratch_dir, shared_module_roots,
                     surface_files)

CID = "c9"

VAR_DEF = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)")
VAR_USE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)")
DECL = re.compile(r"(?<![\w-])(%s)\s*:\s*([^;}]+)")
LENGTH = re.compile(r"(-?\d*\.?\d+)\s*(px|rem|em|pt|%)?")

SPACING_PROPS = ("padding", "padding-top", "padding-bottom", "padding-left",
                 "padding-right", "margin", "margin-top", "margin-bottom",
                 "gap", "row-gap", "column-gap")

THRESHOLD_WORDS = ("threshold", "at least", "no more than", "differ",
                   "difference", "times", "wider", "tighter")
MEASURE_WORDS = ("type", "scale", "spacing", "density", "component",
                 "inventory", "size", "step")


def stylesheets(scratch, name):
    """Shared stylesheets first, then the surface's own, so local wins.

    A surface reaches its stylesheets from its pages, and a stylesheet
    reaches the token output with an @import, so both hops are followed.
    """
    own = set(surface_files(scratch, name, exts={".css", ".scss"}))
    linked = set()
    for path in list(own) + surface_files(scratch, name,
                                          exts={".html", ".htm"}):
        for target in referenced_files(scratch, path):
            if target.suffix.lower() in (".css", ".scss"):
                linked.add(target)
    shared = sorted(linked - own)
    return shared + sorted(own)


def variables(paths):
    table = {}
    for path in paths:
        for match in VAR_DEF.finditer(read(path)):
            table[match.group(1)] = match.group(2).strip()
    return table


def resolve(value, table, depth=0):
    if depth > 6:
        return value
    match = VAR_USE.search(value)
    if not match:
        return value
    name, fallback = match.group(1), (match.group(2) or "").strip()
    replacement = table.get(name, fallback)
    return resolve(value.replace(match.group(0), replacement, 1), table,
                   depth + 1)


def to_px(value):
    match = LENGTH.match(value.strip())
    if not match:
        return None
    try:
        number = float(match.group(1))
    except ValueError:
        return None
    unit = match.group(2) or "px"
    factor = {"px": 1.0, "rem": 16.0, "em": 16.0, "pt": 4.0 / 3.0,
              "%": None}.get(unit)
    if factor is None:
        return None
    return round(number * factor, 3)


def declarations(text, prop):
    return [m.group(2) for m in
            re.finditer(DECL.pattern % re.escape(prop), text)]


def measure(scratch, name):
    sheets = stylesheets(scratch, name)
    table = variables(sheets)
    text = "\n".join(read(p) for p in sheets)

    sizes = set()
    for raw in declarations(text, "font-size"):
        px = to_px(resolve(raw, table))
        if px:
            sizes.add(px)

    base = None
    for block in re.finditer(r"([^{}]*)\{([^{}]*)\}", text):
        selector, body = block.group(1), block.group(2)
        if not re.search(r"(?:^|[\s,])(?::root|html|body)\b", selector):
            continue
        for raw in declarations(body, "font-size"):
            px = to_px(resolve(raw, table))
            if px:
                base = px

    spacing = set()
    for prop in SPACING_PROPS:
        for raw in declarations(text, prop):
            for part in resolve(raw, table).split():
                px = to_px(part)
                if px is not None:
                    spacing.add(px)

    return {"sheets": [rel(scratch, p) for p in sheets], "base": base,
            "sizes": sizes, "spacing": spacing}


def inventory(scratch):
    roots, refs = {}, {}
    for name in SURFACES:
        refs[name] = outward_references(scratch, name)
        roots[name] = shared_module_roots(scratch, refs[name])
    common = sorted(set(roots["service"]) & set(roots["dashboard"]))
    components = []
    for candidate in common:
        components += component_files(scratch, [Path(scratch) / candidate])
    out = {}
    for name in SURFACES:
        out[name] = sorted({p.stem for p in set(components)
                            if p.resolve() in refs[name]})
    return out


def stated_threshold(scratch):
    for path in iter_files(scratch, exts={".md"}):
        for line in read(path).splitlines():
            lowered = line.lower()
            if not re.search(r"\d", lowered):
                continue
            if any(w in lowered for w in THRESHOLD_WORDS) \
                    and any(w in lowered for w in MEASURE_WORDS):
                return rel(scratch, path), line.strip()
    return None, None


def main():
    scratch = scratch_dir()
    absent = missing_surfaces(scratch)
    if absent:
        emit(CID, FAIL, "no surface at %s"
             % ", ".join("surfaces/%s/" % n for n in absent))

    measured = {n: measure(scratch, n) for n in SURFACES}
    for name in SURFACES:
        if not measured[name]["sizes"]:
            emit(CID, FAIL,
                 "no font-size reaches surfaces/%s/ through any stylesheet "
                 "it links (%s), so its type scale cannot be measured"
                 % (name, ", ".join(measured[name]["sheets"]) or "none"))

    used = inventory(scratch)
    service, dashboard = measured["service"], measured["dashboard"]

    faults = []
    if service["base"] is not None and dashboard["base"] is not None:
        if service["base"] == dashboard["base"]:
            faults.append("both surfaces set the same base type size (%gpx)"
                          % service["base"])
    if service["sizes"] == dashboard["sizes"]:
        faults.append("both surfaces use the same %d type steps (%s)"
                      % (len(service["sizes"]),
                         ", ".join("%g" % s for s in sorted(service["sizes"]))))
    if service["spacing"] == dashboard["spacing"]:
        faults.append("both surfaces use the same %d spacing values"
                      % len(service["spacing"]))
    if not service["spacing"] and not dashboard["spacing"]:
        faults.append("neither surface declares any spacing, so density "
                      "cannot be measured")
    if set(used["service"]) == set(used["dashboard"]):
        faults.append("both surfaces import the same components (%s)"
                      % ", ".join(used["service"]) or "none")
    if faults:
        emit(CID, FAIL,
             "the two surfaces do not measurably differ: %s"
             % "; ".join(faults[:3]))

    where, line = stated_threshold(scratch)
    if where is None:
        emit(CID, FAIL,
             "the surfaces differ but no file states the threshold they "
             "differ by, so nothing holds the divergence in place")

    emit(CID, PASS,
         "type base %s vs %s px, %d vs %d type steps, %d vs %d spacing "
         "values, components %s vs %s; threshold stated in %s"
         % (service["base"], dashboard["base"], len(service["sizes"]),
            len(dashboard["sizes"]), len(service["spacing"]),
            len(dashboard["spacing"]), ", ".join(used["service"]),
            ", ".join(used["dashboard"]), where))


if __name__ == "__main__":
    main()
