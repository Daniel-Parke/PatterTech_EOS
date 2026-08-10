#!/usr/bin/env python3
"""Criterion 2: a pseudo-locale exists, and nothing is pinned to a box.

The spec phrases the second half as a measurement: render the form
under the pseudo-locale at 360px and find no element whose `scrollWidth`
exceeds its `clientWidth`. Measuring that needs a bundler, an installed
dependency tree and a browser, and criterion 9 requires these graders to
run with no network, so this grader does not claim to have measured it.

What it settles instead:

- a pseudo-locale catalogue exists, covers every key of the source
  catalogue, and expands the text. A pseudo-locale that does not expand
  cannot show a layout break, so coverage and expansion are the part of
  the criterion that has any force on its own.
- no element that renders a translated string sits inside a box pinned
  to a fixed pixel width or height, or clipped by `overflow: hidden`
  with `white-space: nowrap`. That is the defect the fixture plants and
  the only way this fixture can overflow at 360px: a control sized to
  the English word rather than to its content.

A pass here therefore reads: the pseudo-locale is real, and no fixed
box remains for it to break. It does not read: a browser looked.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, base_catalogue, class_names,  # noqa: E402
                     css_rules, emit, expansion, is_pseudo_tag, jsx_roots,
                     other_catalogues, rel, scratch_dir, selector_classes,
                     t_calls)

CID = "c2"

MIN_EXPANSION = 1.2
PX = re.compile(r"(\d+(?:\.\d+)?)px")
PINNING = ("width", "height", "min-height")


def pinned_classes(scratch):
    """class name -> [(selector, declaration)] that pins a box."""
    out = {}
    for selector, decls, path in css_rules(scratch):
        bad = []
        for prop in PINNING:
            value = decls.get(prop, "")
            if PX.fullmatch(value.strip()):
                bad.append("%s: %s" % (prop, value.strip()))
        if decls.get("white-space", "").strip() == "nowrap" and \
                decls.get("overflow", "").strip() == "hidden":
            bad.append("white-space: nowrap with overflow: hidden")
        if not bad:
            continue
        for name in selector_classes(selector):
            out.setdefault(name, []).append(
                (selector, "; ".join(bad), rel(scratch, path)))
    return out


def renders_copy(node):
    if any(t_calls(expr) for expr in node.exprs()):
        return True
    return any(re.search(r"[A-Za-z]{2}", text) for text in node.texts())


def inline_pin(node):
    kind, value = node.attrs.get("style", (None, ""))
    if kind is None:
        return None
    for prop in PINNING:
        match = re.search(r"%s\s*:\s*([^,}\n]+)" % prop, value)
        if match and (PX.search(match.group(1)) or
                      re.fullmatch(r"\s*\d+\s*", match.group(1))):
            return "style %s: %s" % (prop, match.group(1).strip())
    return None


def main():
    scratch = scratch_dir()
    code, path, base = base_catalogue(scratch)
    if base is None:
        emit(CID, FAIL, "no message catalogue found")

    others = other_catalogues(scratch, path)
    tagged = [o for o in others if is_pseudo_tag(o[0])]
    grown = [o for o in others if expansion(base, o[2]) >= MIN_EXPANSION]
    candidates = tagged or grown
    if not candidates:
        emit(CID, FAIL,
             "no pseudo-locale: %d other catalogue(s) alongside %s and none "
             "carries a pseudo tag or expands the source text"
             % (len(others), rel(scratch, path)))

    best = None
    for cand in candidates:
        missing = [k for k in base if k not in cand[2]]
        ratio = expansion(base, cand[2])
        if not missing and ratio >= MIN_EXPANSION:
            best = (cand, ratio)
            break
        if best is None:
            best = (cand, ratio)
    (pcode, ppath, pflat), ratio = best
    missing = [k for k in base if k not in pflat]
    if missing:
        emit(CID, FAIL,
             "the pseudo-locale %s is missing %d of %d keys, so the form "
             "renders source text where it is thin: %s"
             % (rel(scratch, ppath), len(missing), len(base),
                ", ".join(sorted(missing)[:5])))
    if ratio < MIN_EXPANSION:
        emit(CID, FAIL,
             "the pseudo-locale %s averages %.2f of the source length; a "
             "pseudo-locale that does not expand cannot show a layout break"
             % (rel(scratch, ppath), ratio))

    pinned = pinned_classes(scratch)
    offences = []
    for _, root in jsx_roots(scratch):
        for node in root.elements():
            if not renders_copy(node):
                continue
            inline = inline_pin(node)
            if inline:
                offences.append("%s is pinned by %s" % (node.where(), inline))
            chain = [node] + list(node.ancestors())
            for owner in chain:
                for name in sorted(class_names(owner)):
                    for selector, why, where in pinned.get(name, []):
                        offences.append(
                            "%s renders copy inside .%s, and %s in %s sets %s"
                            % (node.where(), name, selector, where, why))
    if offences:
        unique = sorted(set(offences))
        emit(CID, FAIL,
             "%d element(s) that render translated text are pinned to a "
             "fixed box, which is what overflows at 360px: %s"
             % (len(unique), "; ".join(unique[:4])))

    emit(CID, PASS,
         "%s covers all %d keys at %.2f times the source length, and no "
         "element that renders translated text is pinned to a fixed pixel "
         "box. The 360px scrollWidth measurement itself needs a browser and "
         "was not run here"
         % (rel(scratch, ppath), len(base), ratio))


if __name__ == "__main__":
    main()
