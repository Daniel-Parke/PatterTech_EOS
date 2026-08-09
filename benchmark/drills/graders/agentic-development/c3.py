#!/usr/bin/env python3
"""Criterion 3: the choices are the right ones.

Extraction must be fan-out/fan-in. The merge and pull-request stage
must reach a human checkpoint, either as the checkpoint alone or as a
sequential pipeline terminating in one.

A wrapper the card licenses by composition, event-driven resumable, is
allowed to sit alongside the merge answer, because the brief asks for a
run that survives a restart and the card says topologies stack. What is
refused there is a parallel shape, fan-out/fan-in or
orchestrator-worker, because several agents writing one report file is
the failure the brief is built around.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import FAIL, PASS, emit, require_output  # noqa: E402
from _common import split_front_matter  # noqa: E402
from c2 import resolve  # noqa: E402

CID = "c3"

WANT_EXTRACTION = "fan-out/fan-in"
WANT_MERGE = "human checkpoint"
REFUSED_AT_MERGE = ("fan-out/fan-in", "orchestrator-worker")


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    _text, _ec, extraction_names, _mc, merge_names = resolve(rel, body,
                                                             cid=CID)

    problems = []
    if WANT_EXTRACTION not in extraction_names:
        problems.append(
            "extraction is %s, not %s"
            % (", ".join(extraction_names) or "unassigned", WANT_EXTRACTION))

    if WANT_MERGE not in merge_names:
        problems.append(
            "the merge and pull-request stage is %s and never reaches a %s"
            % (", ".join(merge_names) or "unassigned", WANT_MERGE))
    parallel = [n for n in merge_names if n in REFUSED_AT_MERGE]
    if parallel:
        problems.append(
            "the merge stage is %s, so more than one agent writes the shared "
            "report" % ", ".join(parallel))

    if problems:
        emit(CID, FAIL, "%s: %s" % (rel, "; ".join(problems)))
    emit(CID, PASS,
         "%s selects %s for extraction and reaches a human checkpoint at the "
         "merge and pull-request stage (%s)"
         % (rel, WANT_EXTRACTION, ", ".join(merge_names)))


if __name__ == "__main__":
    main()
