#!/usr/bin/env python3
"""Criterion 10: no accessibility overlay in either build output.

The tree is built on a copy first, because the criterion is about what
ships, not about what sits in the source. Then every script that
reaches either surface's output is read.

Two kinds are caught. A bought overlay is a script loaded from a
vendor: the well-known names, and any script source whose host or path
advertises accessibility. A hand-rolled one is the same idea written in
house, and it is recognised by what it does rather than by a name: a
script that offers to raise the text size, invert the contrast, or turn
on a reading guide is an overlay whoever wrote it.

Prose is not scanned. A link to an accessibility statement is not an
overlay, and a grader that could not tell the difference would punish
the right behaviour.
"""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SURFACES, copy_tree, emit,  # noqa: E402
                     iter_files, read, rel, run_build, scratch_dir)

CID = "c10"

VENDORS = ("accessibe", "acsbapp", "userway", "audioeye", "equalweb",
           "maxaccess", "adally", "allyable", "recite-me", "reciteme",
           "accessiway", "user1st", "truabilities", "accessibilityjs")

SCRIPT_SRC = re.compile(r"""<script[^>]*\bsrc\s*=\s*['"]([^'"]+)['"]""", re.I)

BEHAVIOURS = (
    (re.compile(r"\b(increase|bigger|larger|bump)[-_ ]?(font|text)", re.I),
     "offers to enlarge the text"),
    (re.compile(r"\b(font|text)[-_ ]?size[-_ ]?(up|increase|control)", re.I),
     "offers a text size control"),
    (re.compile(r"\bhigh[-_ ]?contrast\b|\btoggle[-_ ]?contrast\b", re.I),
     "offers a high contrast mode"),
    (re.compile(r"\breading[-_ ]?(guide|mask|ruler)\b", re.I),
     "offers a reading guide"),
    (re.compile(r"\bdyslexi", re.I), "offers a dyslexia font"),
    (re.compile(r"\bscreen[-_ ]?reader[-_ ]?(mode|profile)\b", re.I),
     "offers a screen reader mode"),
    (re.compile(r"\ba11y[-_ ]?(widget|overlay|toolbar|menu)\b", re.I),
     "ships an accessibility widget"),
    (re.compile(r"\baccessibility[-_ ]?(widget|overlay|toolbar|menu|profile)",
                re.I),
     "ships an accessibility widget"),
)


def output_files(tree):
    """Built files for the two surfaces, or the whole build if unsplit."""
    built, other = [], []
    for path in iter_files(tree, exts={".html", ".htm", ".js", ".mjs"}):
        parts = [p.lower() for p in path.relative_to(Path(tree)).parts]
        if parts[0] in ("dist", "build", "_site", "public", "out"):
            if any(name in parts for name in SURFACES):
                built.append(path)
            else:
                other.append(path)
        elif parts[0] == "surfaces":
            built.append(path)
    return (built or other), bool(built)


def suspect_src(src):
    lowered = src.lower()
    for vendor in VENDORS:
        if vendor in lowered.replace(".", "").replace("-", ""):
            return "loads the %s overlay" % vendor
    host = lowered.split("//")[-1].split("/")[0] if "//" in lowered else ""
    if re.search(r"access|a11y", lowered) and re.search(
            r"widget|overlay|toolbar|bar|plugin|accessib", lowered):
        return "loads %s, an accessibility widget" % (host or lowered)
    return None


def main():
    scratch = scratch_dir()
    work, copy = copy_tree(scratch, prefix="drill-uiux-c10-")
    try:
        run_build(copy)
        files, split = output_files(copy)
        if not files:
            emit(CID, FAIL,
                 "nothing was built and neither surface holds a page or a "
                 "script, so there is no build output to clear")

        findings = []
        for path in files:
            text = read(path)
            where = rel(copy, path)
            for src in SCRIPT_SRC.findall(text):
                why = suspect_src(src)
                if why:
                    findings.append("%s %s" % (where, why))
            if path.suffix.lower() in (".js", ".mjs"):
                body = text
            else:
                body = " ".join(re.findall(
                    r"<script(?![^>]*\bsrc\b)[^>]*>(.*?)</script>", text,
                    re.S | re.I))
            for pattern, why in BEHAVIOURS:
                if pattern.search(body):
                    findings.append("%s %s" % (where, why))
                    break

        if findings:
            emit(CID, FAIL,
                 "%d accessibility overlay finding(s) in the build output: %s"
                 % (len(findings), "; ".join(sorted(set(findings))[:3])))

        emit(CID, PASS,
             "%d built file(s)%s carry no overlay: no vendor script and no "
             "hand-rolled text-size, contrast or reading-guide control"
             % (len(files), " for the two surfaces" if split else ""))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
