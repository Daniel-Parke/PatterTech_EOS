---
summary: The four decisions an idempotency header does not make, and how they are settled on money-touching paths
kind: recipe
scope: estate
sources: [EV-0133, EV-0127, EV-0132]
type: example
tags: [money, state]
---

# Reference: the four idempotency parameters

Level 3 detail behind BR-5. A header name is the easy part and settles
nothing. Four decisions remain, and Stripe's documentation is the
clearest specification of them (EV-0133).

## 1. What is stored

The status code and the body of the first attempt, including a 5xx. A
replay returns the stored response rather than re-running the work.
Storing only success is the common shortcut and it is wrong: a client
that retries after a timeout has no way to know whether the first
attempt landed, which is the entire point of the key.

The sharp edge: caching a 500 means a client looping on the same key
receives that failure forever. Retry-with-a-new-key is therefore part of
the contract and belongs in the API documentation, not in a support
thread.

## 2. How long it is retained

At least 24 hours (EV-0133). After the retention window the same key
starts a fresh request, which means a client retrying after a long
outage will genuinely charge twice. Retention is chosen against the
client's plausible retry horizon, not against storage cost. For webhook
receivers, retention outlives the provider's retry schedule.

## 3. What happens on key reuse with different parameters

An error, not a silent overwrite and not a silent replay of the original
response. The stored request is fingerprinted, and a mismatch is
reported as a mismatch. Silently returning the first response to a
different request is how a customer gets charged for the wrong thing and
nobody sees an error anywhere.

## 4. What happens under concurrency

A request that conflicts with a concurrently executing request under the
same key is not cached, and is safe to retry. Caching a
still-in-flight attempt produces a stored answer that never matches what
actually happened.

## Scope and header name

Idempotency applies to POST and PATCH. GET, PUT and DELETE are
idempotent by definition, so a key adds nothing there (EV-0133).

The header name is `Idempotency-Key` as a house default. The IETF draft
carrying that name has never reached RFC and its window has expired
(EV-0127), and Azure mandates the OASIS Repeatable Requests headers
instead (EV-0132). Cite it as de facto. A venture on a platform that
mandates otherwise follows the platform and records the deviation.

## Where the key comes from

The client generates it, which is the point: retry safety becomes an
explicit contract term the caller controls rather than server-side
guesswork (EV-0127). A server that generates the key has not built
idempotency, it has built a request id.

## Money-touching paths

On any path that charges, refunds or transfers, all four parameters are
written down next to the endpoint and are covered by a test that issues
the same key twice and asserts one effect. The endpoint activates the
money factor in `kernel/POLICY_SPEC.md`, floor R2, and executing the
movement is manual-only at the guard. The pack requires the machinery to
be correct; it never authorises the agent to fire it.

## Minimum store shape

Key, request fingerprint, state (in-flight, complete), stored status
code, stored body, created timestamp, expiry timestamp. The state column
is what distinguishes the concurrency case from the replay case, and
omitting it is the usual cause of a double effect under retry storms.
