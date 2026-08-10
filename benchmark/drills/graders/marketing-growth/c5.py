#!/usr/bin/env python3
"""Criterion 5: one-click unsubscribe, headers and token both.

The headers are read off the delivered messages. The token half is
exercised through the command the repository documents,
`unsubscribe.py post <uri>`, which stands in for the POST a mailbox
provider makes. A valid URI must be accepted and the same URI with one
character of its token changed must be refused.
"""

import re
import string
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_script, headers_of,  # noqa: E402
                     messages, run, scratch_dir, work_copy)

CID = "c5"

POST_VALUE = "list-unsubscribe=one-click"
TOKEN_KEYS = ("t", "token", "sig", "signature", "k", "key", "hmac", "mac",
              "nonce", "code", "id")

URI_RE = re.compile(r"<\s*(https://[^>\s]+)\s*>")
H_TAG_RE = re.compile(r"(?:^|;)\s*h\s*=\s*([^;]+)", re.I)


def dkim_headers(values):
    """Every header name inside the h= tag of any DKIM signature."""
    names = set()
    for value in values:
        match = H_TAG_RE.search(value)
        if not match:
            continue
        for name in match.group(1).split(":"):
            cleaned = re.sub(r"\s+", "", name).lower()
            if cleaned:
                names.add(cleaned)
    return names


def tamper(uri):
    """The same URI with one character of its opaque part changed."""
    parts = urlparse(uri)
    query = parse_qsl(parts.query, keep_blank_values=True)
    if query:
        index = next((i for i, (k, _) in enumerate(query)
                      if k.lower() in TOKEN_KEYS), len(query) - 1)
        key, value = query[index]
        if value:
            query[index] = (key, flip(value))
            return urlunparse(parts._replace(query=urlencode(query)))
    if parts.path.strip("/"):
        segments = parts.path.split("/")
        segments[-1] = flip(segments[-1])
        return urlunparse(parts._replace(path="/".join(segments)))
    return flip(uri)


def flip(text):
    for i in range(len(text) - 1, -1, -1):
        ch = text[i]
        if ch in string.ascii_letters + string.digits:
            swap = "b" if ch.lower() == "a" else "a"
            if ch.isdigit():
                swap = "7" if ch != "7" else "3"
            elif ch.isupper():
                swap = swap.upper()
            return text[:i] + swap + text[i + 1:]
    return text + "x"


def main():
    scratch = scratch_dir()
    msgs = messages(scratch)
    if len(msgs) < 3:
        emit(CID, FAIL, "found %d message file(s) in the sequence, expected "
                        "three" % len(msgs))

    faults, uris = [], []
    for path in msgs:
        rel = path.relative_to(scratch).as_posix()
        head = headers_of(path)
        unsub = head.get("list-unsubscribe", [])
        uri = None
        for value in unsub:
            match = URI_RE.search(value)
            if match:
                uri = match.group(1)
                break
        if not unsub:
            faults.append("%s carries no List-Unsubscribe" % rel)
        elif uri is None:
            faults.append("%s has List-Unsubscribe with no HTTPS URI (%r)"
                          % (rel, unsub[0][:60]))
        else:
            uris.append((rel, uri))

        post = head.get("list-unsubscribe-post", [])
        if not post:
            faults.append("%s carries no List-Unsubscribe-Post" % rel)
        elif re.sub(r"\s+", "", post[0]).lower() != POST_VALUE:
            faults.append("%s has List-Unsubscribe-Post: %r, not "
                          "List-Unsubscribe=One-Click" % (rel, post[0][:40]))

        signed = dkim_headers(head.get("dkim-signature", []))
        if not signed:
            faults.append("%s carries no DKIM-Signature with an h= tag" % rel)
        else:
            for name in ("list-unsubscribe", "list-unsubscribe-post"):
                if name not in signed:
                    faults.append("%s does not sign %s, so it can be "
                                  "stripped in transit" % (rel, name))
    if faults:
        emit(CID, FAIL, "%d header fault(s): %s"
                        % (len(faults), "; ".join(faults[:5])))

    script = find_script(scratch, "unsubscribe")
    if script is None:
        emit(CID, FAIL, "headers are right but there is no unsubscribe "
                        "script, so no token can be checked")

    rel_script = script.relative_to(scratch).as_posix()
    rel, uri = uris[0]
    forged = tamper(uri)
    if forged == uri:
        emit(CID, FAIL, "the unsubscribe URI in %s carries nothing to tamper "
                        "with: %s" % (rel, uri))

    with work_copy(scratch) as tree:
        good_rc, good_out = run(tree / rel_script, ["post", uri], tree)
        bad_rc, bad_out = run(tree / rel_script, ["post", forged], tree)

    if good_rc is None:
        emit(CID, FAIL, "%s would not run: %s" % (rel_script, good_out[:200]))
    if good_rc != 0:
        emit(CID, FAIL, "a valid unsubscribe URI was refused: %s exited %d "
                        "(%s)" % (rel_script, good_rc,
                                  good_out.strip()[-160:] or "no output"))
    if bad_rc == 0:
        emit(CID, FAIL, "a tampered token was accepted: %s exited 0 on %s"
                        % (rel_script, forged))

    emit(CID, PASS,
         "%d messages carry List-Unsubscribe with an HTTPS URI and "
         "List-Unsubscribe-Post, both inside the DKIM h= list; %s accepted "
         "the valid URI and refused the tampered one with exit %d"
         % (len(msgs), rel_script, bad_rc))


if __name__ == "__main__":
    main()
