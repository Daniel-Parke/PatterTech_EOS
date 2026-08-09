#!/usr/bin/env python3
"""Criterion 8: constant-time comparison, and no `==` on a digest.

FRAG-04 and FRAG-05. Two halves, both required: one of the constant-time
comparisons has to be called on the webhook path, and no equality
operator may be applied to a signature or digest anywhere in the webhook
sources.

Called, not mentioned. An earlier version of this grader searched the
file for the string `compare_digest`, so a docstring promising constant
time comparison satisfied it while the handler compared nothing. Python
is read with `ast`: the call has to be a call, and it has to sit in a
function the handler path reaches, whether directly, through a helper,
through a decorator or through a before-request hook. A helper nothing
mentions is dead code, and dead code compares nothing.

The digest half is read the same way. `expected = hmac.new(...)
.hexdigest()` makes `expected` a digest whatever it is called, so
`expected == sent` is caught even though neither name says signature. A
signature compared against `None` or an empty string is a presence
check and is left alone.

Other languages fall back to a textual scan with comments and string
literals removed, and the reason says so. Test files are not read at
all: a test asserting constant-time comparison is not a handler
performing one.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, const_time_calls, digest_compares,  # noqa: E402
                     emit, function_index, handler_sources,
                     module_level_names, pre_hook_functions, python_files,
                     reachable_functions, route_handlers, scratch_dir,
                     strip_comments)

CID = "c8"

TEXT_CONST_TIME = (
    ("hmac.compare_digest", re.compile(r"compare_digest\s*\(", re.I)),
    ("crypto.timingSafeEqual", re.compile(r"timingsafeequal\s*\(", re.I)),
    ("secure_compare", re.compile(r"secure_compare\s*\(", re.I)),
    ("hash_equals", re.compile(r"hash_equals\s*\(", re.I)),
)
TEXT_BAD = re.compile(
    r"[\w.\[\]\"']*(signature|digest|hmac)[\w.\[\]\"']*\s*[!=]==?|"
    r"[!=]==?\s*[\w.\[\]\"']*(signature|digest|hmac)", re.I)


def python_verdict(scratch, webhook_rels):
    """(found, offences, notes) read from the syntax tree."""
    parsed, broken = python_files(scratch)
    index = function_index(parsed)
    wired = module_level_names(parsed)

    roots = set()
    entries = 0
    for rel, tree, _text in parsed:
        if rel not in webhook_rels:
            continue
        for fn, decorators in route_handlers(tree):
            entries += 1
            roots.add(fn.name)
            for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", decorators):
                if token in index:
                    roots.add(token)
        for hook in pre_hook_functions(tree):
            entries += 1
            roots.add(hook.name)
    roots |= {name for name in index if name in wired}
    reachable = reachable_functions(roots, index)

    found, dead, offences = [], [], []
    for rel, tree, _text in parsed:
        if rel not in webhook_rels:
            continue
        for name, defs in index.items():
            for def_rel, node in defs:
                if def_rel != rel:
                    continue
                for pos, called in const_time_calls(node):
                    row = "%s line %d, in %s()" % (rel, pos[0], name)
                    if name in reachable or not entries:
                        found.append((called, row))
                    else:
                        dead.append((called, row))
                for pos, label in digest_compares(node):
                    offences.append("%s line %d compares %s with an equality "
                                    "operator" % (rel, pos[0], label))
    return (found, dead, offences,
            [rel for rel, _why in broken if rel in webhook_rels], entries)


def main():
    scratch = scratch_dir()
    sources = handler_sources(scratch)
    if not sources:
        emit(CID, FAIL,
             "no webhook handler source in the tree: nothing outside the "
             "tests mentions a webhook, a signature or an HMAC")

    webhook_rels = {rel for rel, _path, _text in sources}
    found, dead, offences, broken, entries = python_verdict(scratch,
                                                            webhook_rels)
    if broken:
        emit(CID, FAIL,
             "%s does not parse as Python, so what it compares cannot be "
             "read" % ", ".join(broken))

    textual = []
    for rel, path, text in sources:
        if path.suffix.lower() == ".py":
            continue
        textual.append(rel)
        code = strip_comments(rel, text)
        for label, pattern in TEXT_CONST_TIME:
            match = pattern.search(code)
            if match:
                found.append((label, "%s (read textually, not parsed)" % rel))
                break
        for match in TEXT_BAD.finditer(code):
            offences.append("%s compares %r with an equality operator (read "
                            "textually, not parsed)"
                            % (rel, " ".join(match.group(0).split())))

    if not found:
        where = ", ".join(r for r, _, _ in sources[:4])
        if dead:
            detail = ("%s is called at %s, but nothing on the webhook handler "
                      "path calls that function and nothing mentions it, so "
                      "no comparison happens when an event arrives"
                      % (dead[0][0], dead[0][1]))
        else:
            detail = ("no call to hmac.compare_digest, crypto.timingSafeEqual, "
                      "secure_compare or hash_equals in %s. A mention in a "
                      "comment or a docstring is not a call" % where)
        if offences:
            detail += "; and %s" % offences[0]
        emit(CID, FAIL, detail)
    if offences:
        emit(CID, FAIL,
             "%s is called at %s, but %s, which leaks the digest a byte at a "
             "time" % (found[0][0], found[0][1], offences[0]))

    note = (" (%s read textually rather than parsed)"
            % ", ".join(sorted(set(textual)))) if textual else ""
    if not entries:
        note += (" No route handler or before-request hook could be picked "
                 "out of the Python sources, so the call was not traced to "
                 "one")
    emit(CID, PASS,
         "%s calls %s on the handler path, and no signature or digest is "
         "compared with == or !=%s" % (found[0][1], found[0][0], note))


if __name__ == "__main__":
    main()
