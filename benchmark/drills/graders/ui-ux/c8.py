#!/usr/bin/env python3
"""Criterion 8: one philosophy per surface, cited, and schema-checked.

`DESIGN_DECISIONS.md` is split into blocks at its headings and each
block is attributed to the surface it names. A surface's block must
name exactly one philosophy from the pack's list and carry at least one
evidence id. The two surfaces must not land on the same philosophy: the
whole point of recording a choice per surface is that the answer can
differ, and a file naming the same option twice records a house style
rather than a decision.

The schema half is settled by removing the evidence ids from one
surface's block on a copy and requiring the delivered suite to go red.
A schema file that nothing runs is a template, not a check.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SURFACES, emit, green_suite,  # noqa: E402
                     iter_files, read, rel, scratch_dir, suite_fails_with)

CID = "c8"

RECORD = "DESIGN_DECISIONS.md"

PHILOSOPHIES = {
    "content-first public service": ("content-first", "content first"),
    "dense enterprise": ("dense enterprise",),
    "consumer and lifestyle, expressive": ("consumer and lifestyle",
                                           "expressive"),
    "editorial": ("editorial",),
    "conversion-led landing": ("conversion-led", "conversion led"),
    "data-heavy dashboard": ("data-heavy", "data heavy"),
    "mobile-native, platform-conformant": ("mobile-native",
                                           "platform-conformant"),
    "restrained minimal": ("restrained minimal",),
}

EVIDENCE = re.compile(r"\bEV-\d{3,5}\b")
HEADING = re.compile(r"^#{1,6}\s+.*$", re.M)


def blocks(text):
    out, current, buffer = [], "", []
    for line in text.splitlines():
        if HEADING.match(line):
            if buffer:
                out.append((current, "\n".join(buffer)))
            current, buffer = line, [line]
        else:
            buffer.append(line)
    if buffer:
        out.append((current, "\n".join(buffer)))
    return out


def surface_blocks(text):
    found = {name: [] for name in SURFACES}
    for heading, body in blocks(text):
        lowered = body.lower()
        hits = [n for n in SURFACES if n in lowered]
        if len(hits) == 1:
            found[hits[0]].append(body)
        elif len(hits) == 2 and heading:
            head = heading.lower()
            named = [n for n in SURFACES if n in head]
            if len(named) == 1:
                found[named[0]].append(body)
    return {n: "\n".join(v) for n, v in found.items()}


def philosophies_in(text):
    lowered = text.lower()
    return sorted(name for name, words in PHILOSOPHIES.items()
                  if any(w in lowered for w in words))


DECISION_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*|_)?\s*"
    r"(?:philosophy|choice|chosen|decision|option taken|takes)\b", re.I)
RUNNER_UP = re.compile(
    r"runner[- ]?up|rejected|turned down|considered|instead of|not taken|"
    r"would have|alternative", re.I)


def chosen_philosophy(block):
    """The philosophy a block records as its choice, or None.

    A record that names the runner-up is doing the right thing, so the
    grader looks first for a line that states the decision, and only
    falls back to counting names once the lines discussing what was not
    chosen are set aside.
    """
    for line in block.splitlines():
        if DECISION_LINE.match(line) and not RUNNER_UP.search(line):
            named = philosophies_in(line)
            if len(named) == 1:
                return named[0], None
            if len(named) > 1:
                head = [n for n in named if n != "restrained minimal"]
                if len(head) == 1:
                    return head[0], None
    kept = "\n".join(line for line in block.splitlines()
                     if not RUNNER_UP.search(line))
    named = philosophies_in(kept)
    if len(named) > 1:
        head = [n for n in named if n != "restrained minimal"]
        named = head or named
    if len(named) == 1:
        return named[0], None
    if not named:
        return None, "names no philosophy from the pack's list"
    return None, ("names %d philosophies (%s) and no line states which one "
                  "was taken" % (len(named), ", ".join(named)))


def strip_evidence(tree):
    path = Path(tree) / RECORD
    if not path.is_file():
        return None
    text = read(path)
    stripped = EVIDENCE.sub("", text)
    if stripped == text:
        return None
    path.write_text(stripped, encoding="utf-8")
    return "removed every evidence id from %s" % RECORD


def main():
    scratch = scratch_dir()
    path = Path(scratch) / RECORD
    if not path.is_file():
        emit(CID, FAIL, "no %s at the root of the tree" % RECORD)

    text = read(path)
    per_surface = surface_blocks(text)
    empty = [n for n in SURFACES if not per_surface[n].strip()]
    if empty:
        emit(CID, FAIL,
             "%s has no section naming the %s surface, so the record covers "
             "one surface at best"
             % (RECORD, " or ".join(empty)))

    chosen, problems = {}, []
    for name in SURFACES:
        block = per_surface[name]
        pick, why = chosen_philosophy(block)
        if pick is None:
            problems.append("the %s section %s" % (name, why))
            continue
        chosen[name] = pick
        if not EVIDENCE.search(block):
            problems.append("the %s section cites no evidence id (EV-nnnn) "
                            "for %s" % (name, pick))
    if problems:
        emit(CID, FAIL, "%s: %s" % (RECORD, "; ".join(problems[:3])))

    if len(set(chosen.values())) < 2:
        emit(CID, FAIL,
             "both surfaces are recorded as %s, so the record does not name "
             "one philosophy per surface, it names a house style"
             % list(chosen.values())[0])

    schemas = [rel(scratch, p) for p in iter_files(scratch)
               if "schema" in p.name.lower()]
    if not schemas:
        emit(CID, FAIL,
             "no schema file anywhere in the tree, so nothing validates %s"
             % RECORD)

    argv, label, why = green_suite(scratch)
    if argv is None:
        emit(CID, FAIL, why)

    red, what, detail = suite_fails_with(scratch, strip_evidence,
                                         prefix="drill-uiux-c8-")
    if red is None:
        emit(CID, FAIL, "the schema probe could not be applied: %s" % detail)
    if not red:
        emit(CID, FAIL,
             "the suite stays green after every evidence id was removed from "
             "%s, so %s is a template nothing checks"
             % (RECORD, ", ".join(schemas[:2])))

    emit(CID, PASS,
         "service takes %s and dashboard takes %s, each with an evidence id, "
         "and %s goes red when the ids are removed"
         % (chosen["service"], chosen["dashboard"], ", ".join(schemas[:2])))


if __name__ == "__main__":
    main()
