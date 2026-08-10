#!/usr/bin/env python3
"""Criterion 3: the hardcoded-string oracle.

The spec renders the form under the pseudo-locale and looks for the
literal `Try again` in the DOM. A string that never went through the
lookup is the one thing a pseudo-locale cannot disguise, which is why
that check is the oracle for the whole class.

This grader reads the source instead of a rendered DOM, and asks the
same question one step earlier: is there a literal in the components
that a user would read? Three shapes count.

- a JSX text node carrying a word. `{t("x")}` is an expression and is
  fine; `Try again` between two tags is not.
- a user-facing attribute set to a quoted string: placeholder, title,
  alt, aria-label and their kin.
- the literal `Try again` anywhere under the application source, which
  the spec names outright.

Attributes that are not read out, `href`, `type`, `autoComplete` and
the rest, are left alone. So is punctuation-only text, which is
furniture rather than copy.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, app_files, emit, jsx_roots,  # noqa: E402
                     read, rel, scratch_dir, strip_comments)

CID = "c3"

ORACLE = "try again"

SPOKEN_ATTRS = {"placeholder", "title", "alt", "aria-label", "arialabel",
                "aria-placeholder", "aria-description", "aria-valuetext",
                "aria-roledescription", "label", "summary"}

# Tags whose text is not read by a person.
QUIET_TAGS = {"script", "style", "code", "pre", "svg", "path", "symbol",
              "title", "head", "meta", "link"}

WORD = re.compile(r"[A-Za-z]{2,}")
ENTITY = re.compile(r"&[#\w]+;")


def spoken_text(node):
    out = []
    for text in node.texts():
        clean = ENTITY.sub(" ", text)
        if WORD.search(clean):
            out.append(" ".join(clean.split())[:60])
    return out


def main():
    scratch = scratch_dir()
    roots = jsx_roots(scratch)
    if not roots:
        emit(CID, FAIL, "no source file carries markup to read")

    offences = []
    for _, root in roots:
        for node in root.elements():
            if node.tag.lower() in QUIET_TAGS:
                continue
            quiet = any(a.tag.lower() in QUIET_TAGS for a in node.ancestors())
            if quiet:
                continue
            for text in spoken_text(node):
                offences.append("%s renders the literal %r"
                                % (node.where(), text))
            for name, (kind, value) in sorted(node.attrs.items()):
                if name.lower() not in SPOKEN_ATTRS:
                    continue
                if kind != "string" or not WORD.search(value):
                    continue
                offences.append("%s sets %s to the literal %r"
                                % (node.where(), name, value[:40]))

    oracle = []
    for path in app_files(scratch):
        text = strip_comments(read(path))
        if ORACLE in text.lower():
            oracle.append(rel(scratch, path))

    if oracle:
        emit(CID, FAIL,
             "the literal \"Try again\" is still in the source at %s, so it "
             "reaches the DOM under any locale"
             % ", ".join(sorted(set(oracle))))
    if offences:
        unique = sorted(set(offences))
        emit(CID, FAIL,
             "%d hardcoded string(s) never pass through the lookup: %s"
             % (len(unique), "; ".join(unique[:4])))

    emit(CID, PASS,
         "no literal \"Try again\" under the application source, and no JSX "
         "text node or spoken attribute in %d file(s) carries a word that "
         "skipped the lookup" % len(roots))


if __name__ == "__main__":
    main()
