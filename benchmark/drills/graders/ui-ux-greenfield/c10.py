#!/usr/bin/env python3
"""Criterion 10: nothing animates reading matter or a numeric field.

Every animation and transition declaration in the delivered styles is
read, its selector is split into compounds, and each compound is asked
whether it reaches reading matter (paragraphs, lists, tables, notes,
the document body, the universal selector) or a numeric field (an
input, an output, or anything named for a dose, an amount or a figure).

A declaration whose value is `none`, `0s` or `initial` is not an
animation, so the usual global reduced-motion kill block does not trip
this. Inline `style` attributes are read too, because a transition
written into the markup is still a transition.

Scope limit: CSS and inline styles. A script calling `element.animate`
is not read, so an animation built entirely in JavaScript would pass
here. That is a hole in the check and not a permission in the drill.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, MARKUP_SUFFIXES, PASS, STYLE_SUFFIXES,  # noqa: E402
                     css_declarations, css_rules, emit, read, rel,
                     scratch_dir, walk)

CID = "c10"

MOVING = ("animation", "animation-name", "animation-duration",
          "transition", "transition-property", "transition-duration")
INERT = ("none", "0s", "0ms", "initial", "unset", "revert", "inherit", "")

READING_TAGS = {"p", "li", "ul", "ol", "dl", "dt", "dd", "td", "th", "table",
                "tr", "tbody", "thead", "tfoot", "caption", "blockquote",
                "figcaption", "small", "article", "main", "body", "html",
                "h1", "h2", "h3", "h4", "h5", "h6", "label", "legend"}
READING_WORDS = re.compile(r"prose|reading|paragraph|\bnote\b|body-?text|"
                           r"working", re.I)

NUMERIC_TAGS = {"input", "output", "meter", "progress"}
NUMERIC_WORDS = re.compile(r"\bnum|dose|dosage|amount|qty|quantity|tabular|"
                           r"digit|\bmg\b|figure|weight|strength", re.I)

COMPOUND = re.compile(r"[^\s>+~]+")


def targets(selector):
    """(reading matter, numeric field) for one selector."""
    hits = set()
    for compound in COMPOUND.findall(selector):
        if compound in (">", "+", "~"):
            continue
        if compound.strip() == "*":
            hits.add("reading matter (the universal selector)")
            hits.add("numeric fields (the universal selector)")
            continue
        tag = re.match(r"^[a-zA-Z][\w-]*", compound)
        name = tag.group(0).lower() if tag else ""
        if name in READING_TAGS:
            hits.add("reading matter (%s)" % name)
        if name in NUMERIC_TAGS:
            hits.add("a numeric field (%s)" % name)
        if re.search(r"\[type\s*=\s*[\"']?number", compound, re.I) or \
                re.search(r"\[inputmode", compound, re.I):
            hits.add("a numeric field (%s)" % compound)
        rest = compound[len(name):]
        if READING_WORDS.search(rest):
            hits.add("reading matter (%s)" % compound)
        if NUMERIC_WORDS.search(rest):
            hits.add("a numeric field (%s)" % compound)
    return sorted(hits)


def moving(decls):
    for prop in MOVING:
        value = decls.get(prop)
        if value is None:
            continue
        cleaned = value.replace("!important", "").strip().lower()
        if cleaned in INERT:
            continue
        if prop.endswith("duration") and re.fullmatch(r"0(\.0+)?(s|ms)",
                                                      cleaned):
            continue
        return prop, value
    return None


def style_blocks(text):
    return re.findall(r"<style[^>]*>(.*?)</style>", text, re.S | re.I)


def inline_styles(text):
    out = []
    for m in re.finditer(r"<([a-zA-Z][\w-]*)([^>]*)style\s*=\s*\"([^\"]*)\"",
                         text):
        tag, attrs, style = m.group(1), m.group(2), m.group(3)
        classes = re.search(r"class\s*=\s*\"([^\"]*)\"", attrs)
        ident = re.search(r"id\s*=\s*\"([^\"]*)\"", attrs)
        selector = tag.lower()
        if classes:
            selector += "." + ".".join(classes.group(1).split())
        if ident:
            selector += "#" + ident.group(1)
        out.append((selector, css_declarations(style)))
    return out


def main():
    scratch = scratch_dir()
    sheets = walk(scratch, STYLE_SUFFIXES)
    pages = walk(scratch, MARKUP_SUFFIXES)
    rules = []
    for path in sheets:
        for selector, decls, context in css_rules(read(path)):
            rules.append((rel(scratch, path), selector, decls))
    for path in pages:
        text = read(path)
        for block in style_blocks(text):
            for selector, decls, context in css_rules(block):
                rules.append((rel(scratch, path), selector, decls))
        for selector, decls in inline_styles(text):
            rules.append((rel(scratch, path), selector + " (inline)", decls))

    if not rules:
        emit(CID, FAIL,
             "no delivered stylesheet or style block, so the tree carries no "
             "surface to hold to this")

    offences = []
    animated = 0
    for where, selector, decls in rules:
        found = moving(decls)
        if not found:
            continue
        animated += 1
        prop, value = found
        for part in selector.split(","):
            hit = targets(part.strip())
            if hit:
                offences.append("%s: %r sets %s: %s, which reaches %s"
                                % (where, part.strip(), prop, value[:40],
                                   " and ".join(hit)))
    if offences:
        emit(CID, FAIL,
             "%d animated rule(s) reach reading matter or a numeric field: %s"
             % (len(offences), "; ".join(offences[:3])))

    emit(CID, PASS,
         "%d rule(s) across %d file(s), %d of them animated, and none reaches "
         "reading matter or a numeric field"
         % (len(rules), len(sheets) + len(pages), animated))


if __name__ == "__main__":
    main()
