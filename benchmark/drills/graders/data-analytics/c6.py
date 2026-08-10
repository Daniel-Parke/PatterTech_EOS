#!/usr/bin/env python3
"""Criterion 6: the fact grain is declared in words.

The drill asks for the grain "in words", and for the grain string to
name one row per what. So the check is the sentence, not a `grain:` key
with a type next to it: "one row per completed checkout" is the whole
point, and "one row per row" is not.

Files identical to the scenario's own copy are read past, so a grain
sentence has to be something the delivery wrote.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, read, rel, scenario_root,  # noqa: E402
                     scratch_dir, walk)

CID = "c6"

SUFFIXES = (".md", ".markdown", ".txt", ".rst", ".yml", ".yaml", ".json",
            ".sql", ".py")
GRAIN = re.compile(r"one\s+row\s+per\s+([A-Za-z][A-Za-z0-9_ '-]{2,60})", re.I)
# A grain that names nothing. "One row per row" is a tautology and "one
# row per record" is the same tautology in a coat.
VAGUE = {"row", "rows", "record", "records", "line", "lines", "item",
         "items", "thing", "things", "entry", "entries", "unit", "units"}


def delivered(scratch):
    base = scenario_root()
    for path in walk(scratch, SUFFIXES):
        relative = rel(scratch, path)
        if base is not None:
            original = base / relative
            if original.is_file():
                try:
                    if original.read_bytes() == path.read_bytes():
                        continue
                except OSError:
                    pass
        yield relative, read(path)


def main():
    scratch = scratch_dir()
    vague = []
    for relative, text in delivered(scratch):
        for match in GRAIN.finditer(text):
            phrase = " ".join(match.group(1).split())
            head = phrase.split()[0].lower().strip("'-")
            if head in VAGUE and len(phrase.split()) == 1:
                vague.append((relative, phrase))
                continue
            names_grain = "grain" in text.lower()
            emit(CID, PASS,
                 "%s declares the grain in words: %r%s"
                 % (relative, "one row per " + phrase,
                    "" if names_grain else
                    " (the word 'grain' is not used, but the sentence is "
                    "the declaration the criterion asks for)"))
    if vague:
        emit(CID, FAIL,
             "%s says %r, which names nothing: a grain has to say one row "
             "per what" % (vague[0][0], "one row per " + vague[0][1]))
    emit(CID, FAIL,
         "no file the delivery wrote declares a fact grain: nothing says "
         "\"one row per ...\"")


if __name__ == "__main__":
    main()
