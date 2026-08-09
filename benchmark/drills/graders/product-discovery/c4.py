#!/usr/bin/env python3
"""Criterion 4: all four risks are retired, each with an answer in it.

`## Risks` carries exactly four bullets, one opening `- value:`, one
`- usability:`, one `- feasibility:` and one `- viability:`, each with at
least twenty further characters. Twenty characters is not a quality bar
and does not pretend to be one; it is the length below which a line
cannot be anything but "assumed fine". The one this is really watching
is viability, the risk a solo operator skips.

The order of the four is not enforced. The frozen criterion lists them
in the template's order and does not require it, and the pack advises
writing viability first, so a record that follows that advice must not
be failed for it.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, RECORD, clip, emit, logical_lines,  # noqa: E402
                     record_text, scratch_dir, section, sections)

CID = "c4"

RISKS = ("value", "usability", "feasibility", "viability")
MIN_BODY = 20

BULLET = re.compile(r"^-\s*([A-Za-z]+)\s*:\s*(.*)$")


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)

    body = section(text, "Risks")
    if body is None:
        headings = [h for h in sections(text)]
        emit(CID, FAIL,
             "%s has no section headed exactly `## Risks`; its level-two "
             "headings are %s"
             % (RECORD, ", ".join(repr(h) for h in headings) or "none"))

    bullets = [line.strip() for line in logical_lines(body)
               if line.strip().startswith("-")]
    if len(bullets) != len(RISKS):
        emit(CID, FAIL,
             "`## Risks` carries %d bullet(s) and the grammar is exactly "
             "four, one per risk: %s"
             % (len(bullets),
                " / ".join(clip(b, 60) for b in bullets) or "none"))

    found = {}
    for line in bullets:
        m = BULLET.match(line)
        if not m:
            emit(CID, FAIL,
                 "a risk line is not in the `- <risk>: <answer>` grammar: %s"
                 % clip(line))
        label = m.group(1).lower()
        if label not in RISKS:
            emit(CID, FAIL,
                 "`- %s:` is not one of the four risks %s"
                 % (m.group(1), ", ".join(RISKS)))
        if label in found:
            emit(CID, FAIL, "`- %s:` appears twice under `## Risks`" % label)
        found[label] = m.group(2).strip()

    missing = [r for r in RISKS if r not in found]
    if missing:
        emit(CID, FAIL,
             "`## Risks` never answers %s" % ", ".join(missing))

    thin = [r for r in RISKS if len(found[r]) < MIN_BODY]
    if thin:
        emit(CID, FAIL,
             "%s carries fewer than %d characters after the label: %s"
             % (", ".join("`- %s:`" % r for r in thin), MIN_BODY,
                " / ".join("%s=%r" % (r, found[r]) for r in thin)))

    emit(CID, PASS,
         "all four risks answered, shortest is `- %s:` at %d characters"
         % min(((r, len(found[r])) for r in RISKS), key=lambda p: p[1]))


if __name__ == "__main__":
    main()
