#!/usr/bin/env python3
"""Criterion 3: the old field name is still resolvable.

The change request renames orders[].ref to orders[].reference. A client
that has not been rebuilt still asks for `ref`, so the criterion allows
two honest endings: keep `ref` in the schema marked deprecated, or
carry a version identifier so the old shape is still served somewhere.

Both halves are required. A tree that never renamed anything satisfies
"ref is still there" trivially, and grading that as a pass would score
doing nothing as backwards compatibility, so the rename has to have
happened before the compatibility question is asked at all.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SPEC_REL, emit, load_spec,  # noqa: E402
                     properties_maps, scratch_dir, version_signals)

CID = "c3"


def main():
    scratch = scratch_dir()
    doc = load_spec(CID, scratch)

    ref_props = []
    reference_props = []
    for owner, props in properties_maps(doc):
        if "ref" in props:
            ref_props.append(props["ref"])
        if "reference" in props:
            reference_props.append(props["reference"])

    if not reference_props:
        if ref_props:
            emit(CID, FAIL,
                 "%s still calls the field `ref` in %d schema(s) and has no "
                 "`reference` property anywhere: the rename the change "
                 "request asked for has not been made"
                 % (SPEC_REL, len(ref_props)))
        emit(CID, FAIL,
             "%s has neither a `ref` nor a `reference` property; the order "
             "reference field is not in the document" % SPEC_REL)

    deprecated = [p for p in ref_props
                  if isinstance(p, dict) and p.get("deprecated") is True]
    if deprecated:
        emit(CID, PASS,
             "`reference` is in the document and `ref` is kept alongside it "
             "with deprecated: true, so a client that has not been rebuilt "
             "still resolves")

    signals = version_signals(doc)
    if ref_props and signals:
        kind, detail = signals[0]
        emit(CID, PASS,
             "`reference` is in the document, `ref` is still present, and a "
             "%s (%s) serves the old shape" % (kind, detail))

    if ref_props:
        emit(CID, FAIL,
             "`ref` is still in the document but it is not marked "
             "deprecated: true and there is no version identifier serving "
             "the old shape, so nothing tells a consumer the field is going "
             "away")
    emit(CID, FAIL,
         "`ref` has been removed outright and replaced by `reference`: every "
         "client that has not been rebuilt breaks on the next deploy, and "
         "nothing in the document says so")


if __name__ == "__main__":
    main()
