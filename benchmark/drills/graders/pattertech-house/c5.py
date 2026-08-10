#!/usr/bin/env python3
"""Criterion 5: the animation whitelist.

A static parse of the CSS the page actually loads. Every property
declared inside a `@keyframes` block must be one of

    opacity, transform, filter, box-shadow, text-shadow,
    background-position

and any block animating `background-position` must be referenced by
exactly one rule whose iteration count is 1, so a paint-heavy gesture
is a single event rather than a loop.

`animation-timing-function` is allowed inside a keyframe block and
ignored: it is per-keyframe easing, not a property being animated.
Everything else counts, custom properties included, because a
registered custom property drives a paint just as a named one does.

This is the load-bearing criterion. A surface can pass every visible
rule and still repaint on every frame because somebody moved a gradient
to make a rule travel, and that is the failure no reviewer catches by
eye.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_css, declarations, emit,  # noqa: E402
                     find_section, keyframe_blocks, page_css, parse_html,
                     read, require_page, scratch_dir, service_titles,
                     top_level_rules)

CID = "c5"

WHITELIST = {"opacity", "transform", "filter", "box-shadow", "text-shadow",
             "background-position"}
IGNORED = {"animation-timing-function"}
TIME = re.compile(r"^[\d.]+m?s$")


def iteration_count(body):
    """The iteration count a rule sets, by longhand or by shorthand."""
    count = None
    for prop, value in declarations("{" + body + "}"):
        value = value.strip().lower()
        if prop == "animation-iteration-count":
            count = value.split(",")[0].strip()
        elif prop == "animation":
            for token in value.split(",")[0].split():
                if token == "infinite":
                    count = "infinite"
                elif re.match(r"^\d+(\.\d+)?$", token) and not TIME.match(token):
                    count = token
    return count


def references(body, name):
    for prop, value in declarations("{" + body + "}"):
        if prop in ("animation", "animation-name") and \
                re.search(r"(^|[\s,])%s([\s,]|$)" % re.escape(name),
                          value.strip().lower()):
            return True
    return False


def main():
    scratch = scratch_dir()
    page = require_page(CID, scratch)
    root = parse_html(read(page))
    if find_section(root, service_titles(scratch)) is None:
        emit(CID, FAIL,
             "no element carries all the offering titles, so the services "
             "section was never built and there is no animation to whitelist")

    sheets = page_css(scratch)
    if not sheets:
        emit(CID, FAIL, "the page loads no stylesheet, so no CSS was built")
    css = all_css(scratch)

    blocks = keyframe_blocks(css)
    offences = []
    animated = {}
    for name, body in blocks:
        props = {p for p, _ in declarations(body)} - IGNORED
        animated[name] = props
        for prop in sorted(props):
            if prop not in WHITELIST:
                offences.append("@keyframes %s animates %s" % (name, prop))
    if offences:
        emit(CID, FAIL,
             "%d keyframe property/properties are off the whitelist: %s"
             % (len(offences), "; ".join(offences[:5])))

    rules = top_level_rules(css)
    for name, props in sorted(animated.items()):
        if "background-position" not in props:
            continue
        using = [(sel, body) for sel, body in rules if references(body, name)]
        if len(using) != 1:
            emit(CID, FAIL,
                 "@keyframes %s animates background-position and is "
                 "referenced by %d rule(s); the whitelist allows it only as a "
                 "single referenced one-shot" % (name, len(using)))
        count = iteration_count(using[0][1])
        if count not in ("1", "1.0"):
            emit(CID, FAIL,
                 "@keyframes %s animates background-position and %s runs it "
                 "with an iteration count of %s, not 1"
                 % (name, using[0][0], count or "none declared"))

    if not blocks:
        emit(CID, PASS,
             "the page loads %d stylesheet(s) and declares no @keyframes, so "
             "nothing is animated" % len(sheets))
    emit(CID, PASS,
         "%d keyframe block(s) animate only %s"
         % (len(blocks),
            ", ".join(sorted(set().union(*animated.values()))) or "nothing"))


if __name__ == "__main__":
    main()
