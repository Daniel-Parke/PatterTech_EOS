#!/usr/bin/env python3
"""Criterion 6: both /orders operations return problem+json on errors.

Every 4xx, 5xx and default response on POST /orders and GET /orders has
to offer application/problem+json. Offering it alongside another media
type is allowed and said so in the reason; offering only
application/json is the FRAG-01 failure the criterion is aimed at.

An error response that declares no content at all is a failure too: a
status code with no body shape is not a problem document.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SPEC_REL, emit, load_spec,  # noqa: E402
                     operation, orders_path, resolve, scratch_dir)

CID = "c6"

PROBLEM = "application/problem+json"
WILDCARD = re.compile(r"^[45]XX$", re.I)


def is_error(code):
    code = str(code).strip()
    if code.lower() == "default" or WILDCARD.match(code):
        return True
    return code[:1] in ("4", "5") and code.isdigit()


def check(doc, key, method, item):
    op = operation(item, method)
    if op is None:
        return None, "%s declares no %s %s" % (SPEC_REL, method.upper(), key)
    responses = op.get("responses")
    if not isinstance(responses, dict):
        return None, "%s %s declares no responses" % (method.upper(), key)
    errors = {c: r for c, r in responses.items() if is_error(c)}
    if not errors:
        return None, ("%s %s declares no error responses at all, so it "
                      "cannot say how it reports one"
                      % (method.upper(), key))
    bad = []
    extra = []
    for code, response in sorted(errors.items(), key=lambda kv: str(kv[0])):
        response = resolve(doc, response)
        content = (response or {}).get("content")
        if not isinstance(content, dict) or not content:
            bad.append("%s declares no content" % code)
            continue
        types = [str(t) for t in content]
        if PROBLEM not in types:
            bad.append("%s uses %s" % (code, ", ".join(types)))
        elif len(types) > 1:
            extra.append("%s also offers %s"
                         % (code, ", ".join(t for t in types
                                            if t != PROBLEM)))
    if bad:
        return None, "%s %s: %s" % (method.upper(), key, "; ".join(bad))
    detail = "%s %s (%s)" % (method.upper(), key,
                             ", ".join(sorted(str(c) for c in errors)))
    if extra:
        detail += " [%s]" % "; ".join(extra)
    return detail, None


def main():
    scratch = scratch_dir()
    doc = load_spec(CID, scratch)
    key, item = orders_path(doc)
    if item is None:
        emit(CID, FAIL, "%s declares no order collection path" % SPEC_REL)

    good, problems = [], []
    for method in ("post", "get"):
        detail, why = check(doc, key, method, item)
        if why:
            problems.append(why)
        else:
            good.append(detail)
    if problems:
        emit(CID, FAIL, "; ".join(problems))
    emit(CID, PASS,
         "every error response on %s uses %s" % (" and ".join(good), PROBLEM))


if __name__ == "__main__":
    main()
