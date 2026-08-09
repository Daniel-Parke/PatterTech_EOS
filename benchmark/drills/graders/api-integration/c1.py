#!/usr/bin/env python3
"""Criterion 1: api/openapi.yaml parses as valid OpenAPI 3.x.

Structural, not a full 3.1 schema validation: no validator is assumed
present, so this reads the document and asserts the shape every OpenAPI
3 document must have, which is what the criterion turns on. A document
that satisfies this and still breaks a strict validator would be a gap,
and the reason string says what was checked so the gap is visible.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SPEC_REL, YamlError, emit,  # noqa: E402
                     load_yaml, scratch_dir, spec_path)

CID = "c1"

METHODS = ("get", "put", "post", "delete", "options", "head", "patch",
           "trace")


def main():
    scratch = scratch_dir()
    path = spec_path(scratch)
    if not path.is_file():
        emit(CID, FAIL, "no %s in the delivered tree" % SPEC_REL)
    try:
        doc = load_yaml(path)
    except YamlError as exc:
        emit(CID, FAIL, "%s does not parse: %s" % (SPEC_REL, exc))
    if not isinstance(doc, dict):
        emit(CID, FAIL, "%s is not a mapping at the top level" % SPEC_REL)

    version = str(doc.get("openapi", "")).strip()
    if not version:
        emit(CID, FAIL, "%s has no `openapi` version key, so it is not an "
                        "OpenAPI document" % SPEC_REL)
    if not version.startswith("3."):
        emit(CID, FAIL, "%s declares openapi %r, which is not 3.x"
                        % (SPEC_REL, version))

    info = doc.get("info")
    if not isinstance(info, dict):
        emit(CID, FAIL, "%s has no `info` object" % SPEC_REL)
    for key in ("title", "version"):
        if not str(info.get(key, "")).strip():
            emit(CID, FAIL, "%s: info.%s is missing" % (SPEC_REL, key))

    paths = doc.get("paths")
    if not isinstance(paths, dict) or not paths:
        emit(CID, FAIL, "%s declares no paths" % SPEC_REL)

    operations = 0
    for name, item in paths.items():
        if not isinstance(item, dict):
            emit(CID, FAIL, "%s: path %s is not an object" % (SPEC_REL, name))
        for method in METHODS:
            op = item.get(method)
            if op is None:
                continue
            if not isinstance(op, dict):
                emit(CID, FAIL, "%s: %s %s is not an operation object"
                                % (SPEC_REL, method.upper(), name))
            responses = op.get("responses")
            if not isinstance(responses, dict) or not responses:
                emit(CID, FAIL, "%s: %s %s declares no responses"
                                % (SPEC_REL, method.upper(), name))
            operations += 1
    if not operations:
        emit(CID, FAIL, "%s declares paths but no operations" % SPEC_REL)

    emit(CID, PASS,
         "%s parses as OpenAPI %s with %d path(s) and %d operation(s), each "
         "carrying responses" % (SPEC_REL, version, len(paths), operations))


if __name__ == "__main__":
    main()
