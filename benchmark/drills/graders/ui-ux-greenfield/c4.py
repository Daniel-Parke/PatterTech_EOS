#!/usr/bin/env python3
"""Criterion 4: the palette derives from the client's navy and white.

Read from the delivered styles, tokens and markup, never from the
client's brand book: a grader that scanned `docs/brand.md` would pass
an untouched repository, because the navy is written there already.

Both halves are checked. The palette must reach the client's navy, on
hue rather than on an exact string so a derived ladder of tints and
shades counts, and it must carry a white or near-white ground. Then the
barred families: any warm accent, and any cream ground. Red is not
barred, because an error state in a clinical tool needs one and the
drill bars warmth, not danger.

The criterion is keyed to the client's brand, not to distance from the
PatterTech house. A navy clinical palette passes here; so would a cream
editorial one on the brief that asked for cream.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (CLIENT_NAVY, FAIL, MARKUP_SUFFIXES, PASS,  # noqa: E402
                     SCRIPT_SUFFIXES, STYLE_SUFFIXES, colours_in, emit, hcl,
                     hex_of, read, rel, scratch_dir, walk)

CID = "c4"

NAVY_HUE = hcl(CLIENT_NAVY)[0]
HUE_TOLERANCE = 22.0


def is_navy(rgb):
    hue, chroma, light = hcl(rgb)
    return (abs(hue - NAVY_HUE) <= HUE_TOLERANCE and chroma >= 0.06
            and light <= 0.50)


def is_ground(rgb):
    _, chroma, light = hcl(rgb)
    return light >= 0.90 and chroma <= 0.06


def is_warm_accent(rgb):
    hue, chroma, light = hcl(rgb)
    return 15.0 <= hue <= 65.0 and chroma >= 0.15 and 0.18 <= light <= 0.88


def is_cream(rgb):
    hue, chroma, light = hcl(rgb)
    return 20.0 <= hue <= 70.0 and chroma >= 0.035 and light >= 0.85


def palette_files(scratch):
    files = walk(scratch, STYLE_SUFFIXES | MARKUP_SUFFIXES | SCRIPT_SUFFIXES)
    for path in walk(scratch, {".json", ".yaml", ".yml", ".toml"}):
        if colours_in(read(path)):
            files.append(path)
    return files


def main():
    scratch = scratch_dir()
    seen = {}
    for path in palette_files(scratch):
        for written, rgb in colours_in(read(path)):
            seen.setdefault(rgb, (written, rel(scratch, path)))
    if not seen:
        emit(CID, FAIL,
             "no delivered palette: no colour value appears in any "
             "stylesheet, token file, markup or script in the tree")

    warm = [(hex_of(c), seen[c][1]) for c in seen if is_warm_accent(c)]
    cream = [(hex_of(c), seen[c][1]) for c in seen if is_cream(c)]
    if warm:
        emit(CID, FAIL,
             "%d warm accent(s) in the palette, which the client's brand "
             "notes rule out: %s"
             % (len(warm), ", ".join("%s in %s" % w for w in warm[:5])))
    if cream:
        emit(CID, FAIL,
             "%d cream value(s) in the palette, which the client's brand "
             "notes rule out: %s"
             % (len(cream), ", ".join("%s in %s" % c for c in cream[:5])))

    navies = [hex_of(c) for c in seen if is_navy(c)]
    grounds = [hex_of(c) for c in seen if is_ground(c)]
    if not navies:
        emit(CID, FAIL,
             "nothing in the palette derives from the client's navy %s: no "
             "value sits within %g degrees of its hue at any depth. Found %s"
             % (hex_of(CLIENT_NAVY), HUE_TOLERANCE,
                ", ".join(sorted(hex_of(c) for c in seen)[:8])))
    if not grounds:
        emit(CID, FAIL,
             "the palette carries the client's navy (%s) but no white or "
             "near-white ground" % ", ".join(sorted(navies)[:4]))

    emit(CID, PASS,
         "%d colour value(s), %d derived from the client's navy (%s) and %d "
         "white or near-white (%s), with no warm accent and no cream ground"
         % (len(seen), len(navies), ", ".join(sorted(navies)[:4]),
            len(grounds), ", ".join(sorted(grounds)[:3])))


if __name__ == "__main__":
    main()
