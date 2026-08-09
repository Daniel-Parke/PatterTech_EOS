#!/usr/bin/env python3
"""Criterion 2: a `## Topology` section that assigns a topology per stage.

The criterion asks for one topology from the card's ten for extraction
and one for the merge step. Extraction is held to exactly one: a stage
carrying two names is a shortlist, and the pack's record shape says one
per stage, not a list of candidates.

The merge stage is held to at least one, because criterion 3 licenses a
composed answer there in as many words, a sequential pipeline
terminating in a human checkpoint. Reading "exactly one" strictly at
the merge step would fail the answer the next criterion asks for.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, distinct, emit, require_output,  # noqa: E402
                     section, split_front_matter, stage_clauses,
                     topologies_in)

CID = "c2"


def resolve(rel, body, cid=CID):
    """Return the stage clauses and their topologies, or fail `cid`.

    Criterion 3 asks the same question of the same section, so it reads
    the stages through this function and reports under its own id.
    """
    text = section(body, "Topology")
    if text is None:
        emit(cid, FAIL,
             "%s has no level-two heading `## Topology`" % rel)
    extraction, merge = stage_clauses(text)
    extraction_names = distinct(
        [n for clause in extraction for n in topologies_in(clause)])
    merge_names = distinct(
        [n for clause in merge for n in topologies_in(clause)])
    return text, extraction, extraction_names, merge, merge_names


def main():
    _, rel, raw, prose = require_output(CID)
    _fm, body = split_front_matter(prose)
    _text, extraction, extraction_names, merge, merge_names = resolve(rel,
                                                                      body)

    problems = []
    if not extraction:
        problems.append("nothing in the section names the extraction stage")
    elif not extraction_names:
        problems.append("the extraction stage names no topology from the "
                        "card's ten")
    elif len(extraction_names) > 1:
        problems.append("the extraction stage names %d topologies (%s), which "
                        "is a shortlist rather than a choice"
                        % (len(extraction_names), ", ".join(extraction_names)))

    if not merge:
        problems.append("nothing in the section names the merge or "
                        "pull-request stage")
    elif not merge_names:
        problems.append("the merge stage names no topology from the card's "
                        "ten")

    if problems:
        emit(CID, FAIL, "%s `## Topology`: %s" % (rel, "; ".join(problems)))
    emit(CID, PASS,
         "%s assigns %s to extraction and %s to the merge and pull-request "
         "stage" % (rel, extraction_names[0], ", ".join(merge_names)))


if __name__ == "__main__":
    main()
