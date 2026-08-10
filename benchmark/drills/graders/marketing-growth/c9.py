#!/usr/bin/env python3
"""Criterion 9: the growth record names its choices and labels its numbers.

The option lists are read from the pack's own guides rather than copied
here, because the criterion says "from the pack list" and a second copy
in a grader would drift. Where the pack is not on the machine the
criterion is unsettled, not failed: nothing was compared.

The number check is a heuristic and is stated as one. It looks at lines
that state a conversion or a lift as a percentage and asks for the
literal token UNVERIFIED or a named holdout on the same line, or failing
that in the same paragraph. A figure stated some other way can slip
past it.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, all_files, emit,  # noqa: E402
                     read, repo_root, scratch_dir)

CID = "c9"

DOC = "growth_decisions.md"

PHILOSOPHY_GUIDE = ("packs/marketing-growth/guides/"
                    "GD-MKTG-001-growth-philosophy.md")
MEASUREMENT_GUIDE = ("packs/marketing-growth/guides/"
                     "GD-MKTG-003-effect-measurement.md")

OPTION = re.compile(r"^#{2,4}\s+([A-Z])\.\s+(.+?)\s*$", re.M)
EVIDENCE = re.compile(r"\bEV-\d{3,4}\b")
FIGURE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|per cent|percent|pp\b)", re.I)
CLAIM = re.compile(r"\b(conversion|converts?|converted|convert|lift|uplift|"
                   r"open rate|click rate|click-through|ctr|cvr)\b", re.I)
LABELLED = re.compile(r"UNVERIFIED|holdout|hold-out", re.I)


def options(rel):
    text = read(repo_root() / rel)
    if not text:
        return None
    return [m.group(2).strip() for m in OPTION.finditer(text)]


def flatten(text):
    return re.sub(r"\s+", " ", text).casefold()


def sections(text):
    """(heading, body) blocks, the preamble carried under an empty head."""
    out, head, body = [], "", []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            out.append((head, "\n".join(body)))
            head, body = line.strip("# ").strip(), []
        else:
            body.append(line)
    out.append((head, "\n".join(body)))
    return out


def named_in(text, names):
    flat = flatten(text)
    return [n for n in names if flatten(n) in flat]


def cited(text, name):
    """Is there an evidence id in a block that names this choice?"""
    for head, body in sections(text):
        block = head + "\n" + body
        if flatten(name) in flatten(block) and EVIDENCE.search(block):
            return True
    return False


def paragraphs(text):
    return re.split(r"\n\s*\n", text)


def bare_figures(text):
    """Lines stating a conversion or lift with no holdout and no token."""
    out = []
    for block in paragraphs(text):
        block_labelled = bool(LABELLED.search(block))
        for line in block.splitlines():
            if not FIGURE.search(line) or not CLAIM.search(line):
                continue
            if LABELLED.search(line) or block_labelled:
                continue
            out.append(line.strip()[:80])
    return out


def main():
    scratch = scratch_dir()
    found = [p for p in all_files(scratch) if p.name.lower() == DOC]
    if not found:
        emit(CID, FAIL, "no GROWTH_DECISIONS.md in the tree, so no "
                        "philosophy, measurement plan or lawful basis is on "
                        "the record")
    doc = found[0]
    rel = doc.relative_to(scratch).as_posix()
    text = read(doc)

    philosophies = options(PHILOSOPHY_GUIDE)
    measurements = options(MEASUREMENT_GUIDE)
    if not philosophies or not measurements:
        emit(CID, UNSETTLED,
             "the pack guides are not on this machine (%s, %s), so the "
             "choices in %s were compared against nothing"
             % (PHILOSOPHY_GUIDE, MEASUREMENT_GUIDE, rel))

    chosen = named_in(text, philosophies)
    measured = named_in(text, measurements)
    if not chosen:
        emit(CID, FAIL, "%s names no philosophy from the pack list: %s"
                        % (rel, "; ".join(philosophies)))
    if not measured:
        emit(CID, FAIL, "%s names no measurement method from the pack list: "
                        "%s" % (rel, "; ".join(measurements)))

    uncited = [n for n in (chosen[0], measured[0]) if not cited(text, n)]
    if uncited:
        emit(CID, FAIL,
             "%s states %s with no evidence id beside it; the pack expects "
             "at least one EV id per choice"
             % (rel, " and ".join("%r" % n for n in uncited)))

    bare = bare_figures(text)
    if bare:
        emit(CID, FAIL,
             "%d stated figure(s) carry neither a holdout nor the UNVERIFIED "
             "token: %s" % (len(bare), " | ".join(bare[:4])))

    emit(CID, PASS,
         "%s chooses %r and %r, cites evidence for each, and no conversion "
         "or lift figure escapes without a holdout or UNVERIFIED"
         % (rel, chosen[0], measured[0]))


if __name__ == "__main__":
    main()
