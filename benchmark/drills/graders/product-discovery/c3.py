#!/usr/bin/env python3
"""Criterion 3: signals are stated in the grammar and cite real sources.

`## Signal` carries at least one line in

    - signal: <observation> | threshold: <what counts> | source: <artefact>

and every `source:` value in the section names a file of the frozen
fixture. The second half is the one that bites: a signal whose source is
an instrument nobody has built is a signal nobody will ever read.

Two readings made explicit. Lines are the folded ones, so a source
citation wrapped at seventy-two columns still counts, per the note in
`_common`. And a source value may carry a qualifier beside the filename,
because "support_export.csv, tag=stock-accuracy" is a more precise
citation than the bare name, not a worse one; what fails is a token that
looks like a filename and is not in the fixture, or a value with no
fixture file in it at all.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, LOOKS_LIKE_A_FILE, PASS, RECORD,  # noqa: E402
                     clip, emit, fixture_files, is_fixture_file,
                     logical_lines, record_text, scratch_dir, section,
                     sections)

CID = "c3"

GRAMMAR = re.compile(r"^- signal: .+ \| threshold: .+ \| source: .+$")
SOURCE = re.compile(r"source:\s*([^|]+)", re.I)


def tokens(value):
    return [t.strip().strip("`'\"()[]").rstrip(".,;:")
            for t in re.split(r"[\s,;]+", value) if t.strip()]


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)
    files = fixture_files(CID)

    body = section(text, "Signal")
    if body is None:
        headings = [h for h in sections(text)]
        emit(CID, FAIL,
             "%s has no section headed exactly `## Signal`; its level-two "
             "headings are %s"
             % (RECORD, ", ".join(repr(h) for h in headings) or "none"))

    lines = [line for line in logical_lines(body) if line.strip()]
    matching = [line for line in lines if GRAMMAR.match(line.strip())]
    if not matching:
        bullets = [line for line in lines if line.strip().startswith("-")]
        emit(CID, FAIL,
             "no line under `## Signal` matches "
             "`- signal: … | threshold: … | source: …`; %s"
             % ("the section's bullets are: %s"
                % " / ".join(clip(b, 100) for b in bullets[:3])
                if bullets else "the section carries no bullets at all"))

    cited = []
    for line in lines:
        for match in SOURCE.finditer(line):
            value = match.group(1).strip()
            if not value:
                emit(CID, FAIL,
                     "an empty `source:` under `## Signal`: %s" % clip(line))
            named = [t for t in tokens(value) if is_fixture_file(t, files)]
            invented = [t for t in tokens(value)
                        if LOOKS_LIKE_A_FILE.match(t)
                        and not is_fixture_file(t, files)]
            if invented:
                emit(CID, FAIL,
                     "`source: %s` names %s, which is not a file of the "
                     "fixture; the fixture holds %s"
                     % (clip(value, 80),
                        ", ".join(repr(t) for t in invented),
                        ", ".join(files)))
            if not named:
                emit(CID, FAIL,
                     "`source: %s` names no file of the fixture, so the "
                     "signal cites something that does not exist; the "
                     "fixture holds %s" % (clip(value, 80), ", ".join(files)))
            cited.extend(named)

    emit(CID, PASS,
         "%d signal line(s) in the grammar and %d source citation(s), every "
         "one a fixture file: %s"
         % (len(matching), len(cited),
            ", ".join(sorted(set(cited)))))


if __name__ == "__main__":
    main()
