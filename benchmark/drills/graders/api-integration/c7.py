#!/usr/bin/env python3
"""Criterion 7: nothing parses the body before the signature is checked.

FRAG-05. The handler has to authenticate the raw bytes it was sent, so
a JSON parse standing in front of the signature check means unverified
input reached the parser.

The check is a comparison, and only a comparison: a constant-time
comparison call, or an equality comparison of a digest. Computing a
digest is not checking one. An earlier version of this grader accepted
`hmac.new` and `hexdigest` as evidence of a check, and passed a handler
that computed the expected digest, threw it away and parsed the body,
which is the exact defect the criterion exists to catch.

Python handlers are read with `ast`, so the order is the order of the
statements in the function, and a call the handler makes is followed
into the function it names, because a check performed by a helper is
still performed before the parse.

Two verdicts are deliberately not a pass and not a fail. A handler that
hands the raw bytes to a verifier this tree does not contain, a library
call, cannot be settled by reading this tree, and neither can a handler
written in a language this grader cannot order statements in. Both
report unsettled, which the runner records as manual and which blocks a
green drill.
"""

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, digest_computations,  # noqa: E402
                     dotted, emit, function_index, handler_functions,
                     handler_sources, opaque_verifiers, own_nodes, position,
                     pre_hook_functions, python_files, scratch_dir,
                     verification_event, verifying_names)

CID = "c7"

PARSE_NAMES = re.compile(
    r"(^|\.)(loads|load|get_json|from_json|parse_raw|model_validate_json|"
    r"json_body|parse)$", re.I)
PARSE_ATTR = re.compile(r"^(request|req|flask\.request|ctx\.request)\.json$",
                        re.I)


def first_parse(nodes):
    best = None
    for node in nodes:
        hit = None
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name and PARSE_NAMES.search(name) and "json" in name.lower():
                hit = name
            elif name and name.lower().endswith(("get_json", "parse_raw",
                                                 "model_validate_json")):
                hit = name
        elif isinstance(node, ast.Attribute):
            name = dotted(node)
            if PARSE_ATTR.match(name or ""):
                hit = name
        if hit and (best is None or position(node) < best[0]):
            best = (position(node), hit)
    return best


def verdict_for(rel, tree, text, index, verifying):
    """(state, detail) for one Python file, or (None, None) when silent.

    State is PASS, FAIL or UNSETTLED.
    """
    hook_check = None
    for hook in pre_hook_functions(tree):
        found = verification_event(hook, verifying)
        if found:
            hook_check = "%s() checks it first" % hook.name
            break

    seen = None
    for fn, _decorators in handler_functions(tree, text):
        nodes = own_nodes(fn)
        parse = first_parse(nodes)
        if parse is None:
            continue
        check = verification_event(fn, verifying)
        if check is None and hook_check:
            seen = (PASS, "%s: %s() parses with %s, and a before-request hook "
                          "in the same file %s"
                    % (rel, fn.name, parse[1], hook_check))
            continue
        if check is None:
            opaque = [row for row in opaque_verifiers(fn, index)
                      if row[0] < parse[0]]
            if opaque:
                return UNSETTLED, (
                    "%s: %s() calls %s at line %d before parsing with %s at "
                    "line %d, and that function is not defined in this tree, "
                    "so whether it compares the signature cannot be settled "
                    "by reading the tree"
                    % (rel, fn.name, opaque[0][1], opaque[0][0][0], parse[1],
                       parse[0][0]))
            digests = digest_computations(fn)
            if digests:
                return FAIL, (
                    "%s: %s() computes a digest with %s at line %d and never "
                    "compares it with anything, then parses the body with %s "
                    "at line %d. Computing a digest is not checking one"
                    % (rel, fn.name, digests[0][1], digests[0][0][0],
                       parse[1], parse[0][0]))
            return FAIL, (
                "%s: %s() parses the body with %s at line %d and nothing in "
                "it, or in anything it calls, compares a signature"
                % (rel, fn.name, parse[1], parse[0][0]))
        if check[0] > parse[0] and not hook_check:
            return FAIL, (
                "%s: %s() parses the body with %s at line %d, before the "
                "signature check %s at line %d"
                % (rel, fn.name, parse[1], parse[0][0], check[1],
                   check[0][0]))
        seen = (PASS, "%s: %s() checks the signature at line %d with %s, then "
                      "parses with %s at line %d"
                % (rel, fn.name, check[0][0], check[1], parse[1],
                   parse[0][0]))
    return seen if seen else (None, None)


def main():
    scratch = scratch_dir()
    sources = handler_sources(scratch)
    if not sources:
        emit(CID, FAIL,
             "no webhook handler source in the tree: nothing outside the "
             "tests mentions a webhook, a signature or an HMAC")

    webhook_rels = {rel for rel, _path, _text in sources}
    parsed, broken = python_files(scratch)
    for rel, why in broken:
        if rel in webhook_rels:
            emit(CID, FAIL, "%s does not parse as Python: %s" % (rel, why))

    index = function_index(parsed)
    verifying = verifying_names(index)

    passes = []
    for rel, tree, text in parsed:
        if rel not in webhook_rels:
            continue
        state, detail = verdict_for(rel, tree, text, index, verifying)
        if state == FAIL:
            emit(CID, FAIL, detail)
        if state == UNSETTLED:
            emit(CID, UNSETTLED, detail)
        if state == PASS:
            passes.append(detail)

    others = sorted(rel for rel, _p, _t in sources
                    if not rel.lower().endswith(".py"))
    if passes:
        note = ("" if not others else
                ". %s also mentions a webhook and was not ordered, because "
                "statement order in it cannot be settled by a textual scan"
                % ", ".join(others[:3]))
        emit(CID, PASS, "%s%s" % ("; ".join(passes[:3]), note))

    if others:
        emit(CID, UNSETTLED,
             "the webhook source in this tree is %s, and statement order in "
             "those files cannot be settled by a textual scan: a helper "
             "defined below the handler would read as late and one defined "
             "above as early, whatever either of them does. Read it by hand"
             % ", ".join(others[:4]))

    emit(CID, FAIL,
         "found %d webhook source file(s) (%s) but no handler that reads the "
         "request body, so there is no ordering to judge and no verified "
         "receiver either"
         % (len(sources), ", ".join(r for r, _, _ in sources[:4])))


if __name__ == "__main__":
    main()
