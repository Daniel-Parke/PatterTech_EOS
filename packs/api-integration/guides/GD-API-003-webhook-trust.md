---
summary: How is an inbound webhook trusted: bare-body HMAC, a signed triple, RFC 9421 message signatures, or an asymmetric or provider-native scheme?
kind: guide
authority: advisory
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0123, EV-0125, EV-0126, EV-0034, EV-0039]
review: on-change-of:EV-0125
type: guide
tags: [security, money, arch]
---

# GD-API-003: how is an inbound webhook trusted?

## The question

A webhook is an unauthenticated HTTP request from the open internet that
asks your service to believe something happened. The fork is what makes
it believable. The failure that decides it is not the forged delivery,
which most teams do think about, but the replayed one: a genuine signed
delivery captured and sent again, which every signature scheme without a
timestamp accepts forever.

## It depends on

- Are you receiving someone else's scheme, or emitting your own?
- Does the delivery move money, grant access or change state you cannot
  undo?
- Do intermediaries rewrite headers or re-encode the body in transit?
- How do you rotate the secret without dropping deliveries?

## Options

### A. Bare-body HMAC with a static shared secret

GitHub's shape: HMAC-SHA256 over the raw body, one header, one secret
(EV-0126). Buys: minimal, understood, implementable in the standard
library in ten lines. Costs: no timestamp, so no replay window and no
natural idempotency key; rotation means accepting two secrets by hand
for a window.

### B. Signed triple with a versioned prefix

Sign `id.timestamp.payload` rather than the payload alone, with a
versioned scheme prefix and support for several signatures in one header
(EV-0125). Buys: the id is an idempotency key, the timestamp is a replay
window, the prefix and multi-signature header give zero-downtime key
rotation and an upgrade path from HMAC to ed25519. Costs: the consumer
must reconstruct the base string exactly; the tolerance value is left to
you; the specification is vendor-originated despite its neutral name.

### C. RFC 9421 HTTP message signatures

Canonicalise an explicit, ordered list of covered components so signer
and verifier build byte-identical input despite lawful intermediary
rewriting, binding `created`, `expires` and `nonce` (EV-0123). Buys: the
rigorous general answer, and the only one that survives proxies that
legitimately rewrite. Costs: a canonicalisation library on both sides,
heavier than a single HMAC, and thin adoption outside standards-minded
estates.

### D. Asymmetric or provider-native, taken as given

Accept ed25519, mTLS or whatever the provider ships, and wrap it in an
adapter. Buys: no negotiation with a vendor who will not change, and
with asymmetric keys the receiver holds no forging secret. Costs: you
inherit their gaps, and every provider is different, so a consumer
library special-cases per provider. There is no convergence in the field
(EV-0125).

## Decision rule

- Receiving from a third party: you take their scheme, usually A or D,
  and you add what it lacks. A replay window and an idempotency store on
  the delivery id are yours to build even when the provider omits them.
- Emitting webhooks: B.
- Machine-to-machine inside an estate with proxies that rewrite: C.
- Money-touching or access-granting deliveries: B or C, plus the
  idempotency store, plus BR-5's four parameters. A without a timestamp
  is not enough on its own.

Non-negotiable under every option, from BR-4: verify over the raw bytes
before any parse, compare in constant time, and bound the timestamp.
Wrap the provider in an owned adapter rather than importing their SDK
across the codebase, per
`packs/architecture/guides/WG-ARCH-007-vendor-seams.md`. The
surrounding controls, secret storage, SSRF on any URL the payload
carries, and log redaction, come from the security-privacy pack
(EV-0034, EV-0039).

## Default

B for anything we emit, five-minute tolerance. The provider's scheme
for anything we receive, behind an adapter, with our own replay window
and delivery-id idempotency store on top. Verification uses the standard
library, not a vendor SDK.

## Worked rulings

- **Venture B (2026, argued, inherited here)**: raw protocol for
  webhooks, standard-library HMAC-SHA256, idempotency keys, no provider
  SDKs, recorded in its own architecture ADR. See
  `packs/architecture/guides/WG-ARCH-007-vendor-seams.md` and
  `registry/stacks/STACK-fastapi-postgres.md`.
- **Nothing in the estate emits webhooks yet**, so option B is a
  default without a ruling behind it. The first venture to emit should
  argue it properly.
