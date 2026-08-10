#!/usr/bin/env python3
"""Criterion 2: the decision validates against the pack's schema.

Plus the two fields the criterion singles out: a `practice` drawn from
the three named anchors, and a `condition` that is not empty. The schema
already carries both, and they are re-checked by name so that a failure
here says which of the two went missing rather than handing back a list
of paths.

The schema is read from the pack rather than from a copy beside this
grader. Criterion 2 says "the pack's pricing decision schema", so if the
pack changes its schema the drill grades the new one. Where the schema
cannot be found or holds a keyword this validator does not implement,
the criterion is unsettled rather than passed: a validator that skips
what it does not understand reports a document as valid that it never
checked.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISION, FAIL, PASS, SCHEMA_REL,  # noqa: E402
                     UNSETTLED, Unsupported, decision_doc, emit, pack_schema,
                     scratch_dir, validate)

CID = "c2"

PRACTICES = ("value-informed", "competition-informed", "cost-informed")


def main():
    scratch = scratch_dir()
    doc = decision_doc(CID, scratch)
    schema = pack_schema(CID)

    try:
        errors = validate(doc, schema)
    except Unsupported as exc:
        emit(CID, UNSETTLED,
             "the pack's schema uses %s, which this grader does not "
             "implement, so %s was not validated" % (exc, DECISION))

    practice = doc.get("practice")
    condition = doc.get("condition")
    if practice not in PRACTICES:
        errors.append(
            "practice is %r; the three anchors are %s"
            % (practice, ", ".join(PRACTICES)))
    if not isinstance(condition, str) or not condition.strip():
        errors.append(
            "condition is empty; a practice with no condition beside it is "
            "not a decision anyone can argue with later")

    if errors:
        emit(CID, FAIL,
             "%s fails the schema at %s: %s%s"
             % (DECISION, SCHEMA_REL, "; ".join(errors[:6]),
                "" if len(errors) <= 6 else
                " (and %d more)" % (len(errors) - 6)))
    emit(CID, PASS,
         "%s validates against %s; practice %r with a condition of %d "
         "characters" % (DECISION, SCHEMA_REL, practice,
                         len(condition.strip())))


if __name__ == "__main__":
    main()
