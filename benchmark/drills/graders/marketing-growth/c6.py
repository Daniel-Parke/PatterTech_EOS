#!/usr/bin/env python3
"""Criterion 6: unsubscribing suppresses, and the send path fails closed.

Run in this order, on a throwaway copy of the tree: send to a live
address and expect it to work, post the unsubscribe URI for that same
address, find the address in the suppression store, then send again and
expect a non-zero exit.

The first step matters as much as the last. A send script that refuses
everything would satisfy "a later send attempt exits non-zero" while
being useless, so the grader proves the address was sendable before the
unsubscribe and unsendable after it.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ADDRESS_RE, FAIL, PASS, all_files, emit,  # noqa: E402
                     find_script, headers_of, messages, read, run,
                     scratch_dir, work_copy)

CID = "c6"

URI_RE = re.compile(r"<\s*(https://[^>\s]+)\s*>")


def recipient(path, uri):
    """The address an unsubscribe URI acts on, or the message's own To."""
    parts = urlparse(uri)
    hit = ADDRESS_RE.search(unquote(parts.query + " " + parts.path))
    if hit:
        return hit.group(0)
    for value in headers_of(path).get("to", []):
        hit = ADDRESS_RE.search(value)
        if hit:
            return hit.group(0)
    return None


def pairs(scratch):
    out = []
    for path in messages(scratch):
        for value in headers_of(path).get("list-unsubscribe", []):
            match = URI_RE.search(value)
            if not match:
                continue
            uri = match.group(1)
            who = recipient(path, uri)
            if who:
                out.append((path.relative_to(scratch).as_posix(), who, uri))
            break
    return out


def holders(tree, address):
    return {p.relative_to(tree).as_posix() for p in all_files(tree)
            if address.lower() in read(p).lower()}


def main():
    scratch = scratch_dir()
    candidates = pairs(scratch)
    if not candidates:
        emit(CID, FAIL, "no message carries an unsubscribe URI with a "
                        "recipient this grader can act on; criterion 5 is "
                        "where the headers are reported")

    send = find_script(scratch, "send")
    unsub = find_script(scratch, "unsubscribe")
    if send is None:
        emit(CID, FAIL, "no send script in the tree")
    if unsub is None:
        emit(CID, FAIL, "no unsubscribe script in the tree")
    rel_send = send.relative_to(scratch).as_posix()
    rel_unsub = unsub.relative_to(scratch).as_posix()

    with work_copy(scratch) as tree:
        chosen = None
        refusals = []
        for rel, address, uri in candidates:
            code, out = run(tree / rel_send, [address], tree)
            if code == 0:
                chosen = (rel, address, uri)
                break
            refusals.append("%s -> exit %s" % (address, code))
        if chosen is None:
            emit(CID, FAIL,
                 "%s refuses every address in the sequence before any "
                 "unsubscribe, so nothing can be shown to change: %s"
                 % (rel_send, "; ".join(refusals[:3])))

        rel, address, uri = chosen
        before = holders(tree, address)

        code, out = run(tree / rel_unsub, ["post", uri], tree)
        if code != 0:
            emit(CID, FAIL, "%s refused a valid unsubscribe URI from %s "
                            "(exit %s)" % (rel_unsub, rel, code))

        after = holders(tree, address)
        stores = [p for p in after if "suppress" in p.lower()]
        appeared = sorted(after - before)
        if not stores and not appeared:
            emit(CID, FAIL,
                 "the POST returned success but %s appears in no suppression "
                 "store afterwards; files holding it are unchanged: %s"
                 % (address, ", ".join(sorted(before)[:4]) or "none"))
        where = stores[0] if stores else appeared[0]

        code, out = run(tree / rel_send, [address], tree)
        if code == 0:
            emit(CID, FAIL,
                 "%s still sends to %s after it was suppressed in %s"
                 % (rel_send, address, where))

    emit(CID, PASS,
         "%s was sendable, the POST from %s wrote it to %s, and %s then "
         "exited %d rather than sending"
         % (address, rel, where, rel_send, code))


if __name__ == "__main__":
    main()
