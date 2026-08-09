#!/usr/bin/env python3
"""Criterion 3: the output pins which prompt and which model produced it.

The hash is checked by string equality against the digest of
prompt.txt, so a truncated fingerprint does not count: a prefix cannot
be recomputed by a reader holding the file. Both the digest of the
bytes on disk and the digest of the text with line endings normalised
are accepted, because a tree checked out on Windows carries CRLF and a
solution that hashed what it read is not wrong for it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, digests, emit, find_keys,  # noqa: E402
                     json_strings, require_report, scratch_dir, walk)

CID = "c3"


def prompt_file(scratch):
    for path in walk(scratch, {".txt"}):
        if path.name == "prompt.txt":
            return path
    return None


def main():
    scratch = scratch_dir()
    prompt = prompt_file(scratch)
    if prompt is None:
        emit(CID, FAIL,
             "prompt.txt is not in the delivered tree, so the identity the "
             "report should be pinning no longer exists")

    run = require_report(CID, scratch)
    strings = json_strings(run.report)
    wanted = digests(prompt)

    names = [s for s in strings if "prompt.txt" in s.replace("\\", "/")]
    hashed = [s for s in strings
              if any(d in s for d in wanted) or s in wanted]
    models = [(p, v) for p, _, v in find_keys(run.report,
                                              lambda n: "model" in n)
              if isinstance(v, str) and v.strip()]

    missing = []
    if not names:
        missing.append("no field names the prompt template file")
    if not hashed:
        near = [s for s in strings
                if len(s) >= 8 and any(d.startswith(s) for d in wanted)]
        if near:
            missing.append(
                "the prompt hash is recorded as %r, a prefix rather than the "
                "digest, so a reader cannot check it by recomputing"
                % near[0])
        else:
            missing.append(
                "no field carries the content hash of prompt.txt (%s...)"
                % sorted(wanted)[0][:16])
    if not models:
        missing.append("no model identifier field")

    if missing:
        emit(CID, FAIL, "%s: %s" % (run.rel, "; ".join(missing)))

    emit(CID, PASS,
         "%s records the template %r, its digest, and model %s=%r"
         % (run.rel, names[0], models[0][0], models[0][1]))


if __name__ == "__main__":
    main()
