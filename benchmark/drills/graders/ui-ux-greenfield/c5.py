#!/usr/bin/env python3
"""Criterion 5: the type stack names the client's face or a stated substitute.

The client's grotesque is licensed for print only, which the brand
notes say plainly, so both routes are open: name Almsford Grotesk in
the stack, or name what stands in for it and why. A substitute with no
reason written down fails, because the next reader cannot tell a
licensing decision from an accident.

The second clause is absolute: no serif display face anywhere in a
delivered stack. That is checked against a list of families and against
the `serif` and `ui-serif` keywords, tokenised so that `sans-serif`
never trips it.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (CLIENT_TYPEFACE, FAIL, PASS, emit,  # noqa: E402
                     font_stacks, read, rel, scratch_dir, text_files)

CID = "c5"

GENERIC = {"sans-serif", "serif", "monospace", "cursive", "fantasy",
           "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace",
           "ui-rounded", "inherit", "initial", "unset", "revert", "emoji",
           "math", "fangsong", "none", "auto"}

SERIF_KEYWORDS = {"serif", "ui-serif"}

SERIF_FAMILIES = {
    "georgia", "times", "times new roman", "garamond", "eb garamond",
    "adobe garamond", "apple garamond", "playfair display", "playfair",
    "merriweather", "lora", "charter", "baskerville", "libre baskerville",
    "didot", "bodoni", "bodoni moda", "source serif", "source serif pro",
    "source serif 4", "pt serif", "noto serif", "ibm plex serif", "spectral",
    "crimson", "crimson text", "crimson pro", "freight", "tiempos",
    "iowan old style", "palatino", "palatino linotype", "book antiqua",
    "cambria", "constantia", "minion", "minion pro", "caslon",
    "adobe caslon", "hoefler text", "sabon", "utopia", "droid serif",
    "literata", "newsreader", "vollkorn", "cardo", "domine", "bitter",
    "rockwell", "clarendon", "chaparral", "big caslon", "superclarendon",
}

REASON_CUES = ("because", "reason", "licen", "instead", "substitut",
               "stand-in", "stands in", "not available", "print only",
               "no web", "unavailable", "we cannot ship", "in place of")


def named_families(stacks):
    out = {}
    for path, _, families in stacks:
        for family in families:
            out.setdefault(family.lower(), (family, path))
    return out


def serif_hits(stacks):
    hits = []
    for path, raw, families in stacks:
        for family in families:
            low = family.lower().strip()
            if low in SERIF_KEYWORDS or low in SERIF_FAMILIES \
                    or low.endswith(" slab") or low.startswith("serif "):
                hits.append((path, raw, family))
    return hits


def paragraphs(text):
    return [" ".join(block.split())
            for block in re.split(r"\n\s*\n", text) if block.strip()]


def substitute_statement(scratch, families):
    """A written reason naming a delivered family, or None."""
    candidates = {name: shown for name, (shown, _) in families.items()
                  if name not in GENERIC or name == "system-ui"}
    for path in text_files(scratch):
        for block in paragraphs(read(path)):
            low = block.lower()
            if not any(cue in low for cue in REASON_CUES):
                continue
            hit = next((shown for name, shown in candidates.items()
                        if name in low), None)
            if hit is None:
                continue
            if CLIENT_TYPEFACE.lower() in low or "substitut" in low \
                    or "instead" in low or "licen" in low:
                return rel(scratch, path), hit, block[:160]
    return None


def main():
    scratch = scratch_dir()
    stacks = font_stacks(scratch)
    if not stacks:
        emit(CID, FAIL,
             "no type stack delivered: no font-family declaration or font "
             "token in any stylesheet, markup or script")

    serifs = serif_hits(stacks)
    if serifs:
        path, raw, family = serifs[0]
        emit(CID, FAIL,
             "%s asks for the serif face %r in the stack %r; the brief rules "
             "out a serif display face"
             % (rel(scratch, path), family, raw[:80]))

    families = named_families(stacks)
    if CLIENT_TYPEFACE.lower() in families:
        _, path = families[CLIENT_TYPEFACE.lower()]
        emit(CID, PASS,
             "%s names the client's %s in the stack, and no delivered stack "
             "asks for a serif face"
             % (rel(scratch, path), CLIENT_TYPEFACE))

    stated = substitute_statement(scratch, families)
    if stated is None:
        shown = sorted({shown for shown, _ in families.values()})
        emit(CID, FAIL,
             "the stacks name %s, neither the client's %s nor a substitute "
             "with a written reason for it"
             % (", ".join(shown[:6]) or "nothing", CLIENT_TYPEFACE))

    where, family, quote = stated
    emit(CID, PASS,
         "%s substitutes %s with a reason (%r), and no delivered stack asks "
         "for a serif face" % (where, family, quote))


if __name__ == "__main__":
    main()
