---
summary: The verification order, tolerance, rotation and replay controls a webhook receiver needs, with the provider variance that defeats a single implementation
kind: recipe
scope: estate
sources: [EV-0125, EV-0126, EV-0123, EV-0034, EV-0039]
type: example
tags: [security, money]
---

# Reference: verifying an inbound webhook

Level 3 detail behind BR-4 and
`packs/api-integration/wargames/WG-API-003-webhook-trust.md`. Read this
when writing or reviewing a receiver.

## The order of operations

The order is the whole requirement. Every step before the last is a
rejection, and none of them touch parsed data.

1. Read the raw body as bytes. Not the framework's parsed object, not a
   re-serialised copy. A parsed object has already lost the byte
   sequence the signature covers (EV-0126).
2. Read the signature and timestamp headers.
3. Reject if the timestamp is outside the tolerance window. Estate
   default five minutes. No source fixes a number (EV-0125), so this one
   is ours and is open to argument.
4. Rebuild the signed base string exactly as the provider specifies. For
   the triple scheme that is the delivery id, the timestamp and the raw
   payload joined by full stops (EV-0125). For a bare-body scheme it is
   the raw payload alone (EV-0126).
5. Compute the HMAC and compare in constant time. Python
   `hmac.compare_digest`, Node `crypto.timingSafeEqual`, Ruby
   `secure_compare`. Never `==` on the digest.
6. Only now parse the body.
7. Look up the delivery id in the idempotency store. Already seen means
   acknowledge and stop.
8. Do the work, then record the delivery id.

## A receiver in the shape we want

```python
import hashlib
import hmac
import time

TOLERANCE_SECONDS = 300  # estate choice, see WG-API-003

def verify(raw_body: bytes, delivery_id: str, timestamp: str,
           signature: str, secret: bytes) -> bool:
    try:
        sent_at = int(timestamp)
    except ValueError:
        return False
    if abs(time.time() - sent_at) > TOLERANCE_SECONDS:
        return False
    base = b".".join([delivery_id.encode(), timestamp.encode(), raw_body])
    expected = hmac.new(secret, base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

The signature check returns a boolean and does nothing else. Parsing,
dispatch and business logic sit behind the caller's rejection.

## Key rotation without dropped deliveries

A versioned signature prefix and a header that can carry several
signatures let a sender publish under both the old and the new key
during a rotation window, so a receiver that knows either one keeps
working (EV-0125). A receiver should therefore accept a set of
candidate secrets, not a single one, and should compare against each in
constant time rather than short-circuiting on the first mismatch.

The same mechanism carries an algorithm upgrade: `v1` for HMAC-SHA256
and `v1a` for ed25519 in the Standard Webhooks scheme, so a sender can
move to asymmetric keys without a flag day.

## Replay, idempotency and the money case

A timestamp window bounds replay; it does not prevent it. Two deliveries
of the same event inside the window are both valid signatures. The
delivery id is the idempotency key, and the receiver must store it with
the same care as BR-5 demands of an idempotency store: what was stored,
for how long, and what happens on a repeat.

For money-touching receivers the store is not optional and the retention
outlives the provider's retry schedule, which is usually measured in
days rather than hours. Firing the money movement itself is manual-only
at the guard (`kernel/GUARD_SPEC.md`), whatever the receiver decides.

## Provider variance, and why an adapter is required

There is no convergence (EV-0125). GitHub signs the bare body with no
timestamp header at all (EV-0126); Stripe and Slack each ship different
header names, base strings and prefixes. A single receiver cannot be
written once, so each provider gets a small adapter that produces the
raw body, the delivery id, the timestamp and the candidate signatures,
and one shared verifier consumes that structure. RFC 9421 is the
rigorous alternative where both sides are ours and intermediaries
rewrite headers in transit (EV-0123).

## Surrounding controls

Secret storage, log redaction, and SSRF on any URL the payload carries
belong to the security-privacy pack (EV-0034, EV-0039). Two habits worth
naming here anyway: never log the raw signature header alongside the
body, and never fetch a URL from a webhook payload without the same
allowlist you would apply to user input.
