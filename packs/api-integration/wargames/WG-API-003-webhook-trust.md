---
id: WG-API-003
summary: How is an inbound webhook trusted: bare-body HMAC, a signed triple, RFC 9421 message signatures, or an asymmetric or provider-native scheme?
kind: wargame
type: wargame
tags: [arch, eos, money, security, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-API-003, DOC-API-002]
applies_when: [exposes_service_boundary]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0123, EV-0125, EV-0126, EV-0034, EV-0039]
review: on-change-of:EV-0125
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-API-003: how is an inbound webhook trusted?

## Decision question and stakes

A webhook is an unauthenticated HTTP request from the open internet that
asks your service to believe something happened. The fork is what makes
it believable. The failure that decides it is not the forged delivery,
which most teams do think about, but the replayed one: a genuine signed
delivery captured and sent again, which every signature scheme without a
timestamp accepts forever.

## Doctrines or coverage gap under pressure

- `DOC-API-003` (binding): Money-touching mutating endpoints define all four idempotency parameters, not just a header.
- `DOC-API-002` (binding): Webhook receivers authenticate the exact raw request before parsing, reject stale deliveries, and process accepted deliveries idempotently against a pinned payload version.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Are you receiving someone else's scheme, or emitting your own?
- Does the delivery move money, grant access or change state you cannot
  undo?
- Do intermediaries rewrite headers or re-encode the body in transit?
- How do you rotate the secret without dropping deliveries?

Applicability is `exposes_service_boundary`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Bare-body HMAC with a static shared secret

Assume `A. Bare-body HMAC with a static shared secret` was selected and the outcome failed. Test this option's stated failure mechanism first: no timestamp, so no replay window and no natural idempotency key; rotation means accepting two secrets by hand for a window.

### Premortem for B. Signed triple with a versioned prefix

Assume `B. Signed triple with a versioned prefix` was selected and the outcome failed. Test this option's stated failure mechanism first: the consumer must reconstruct the base string exactly; the tolerance value is left to you; the specification is vendor-originated despite its neutral name.

### Premortem for C. RFC 9421 HTTP message signatures

Assume `C. RFC 9421 HTTP message signatures` was selected and the outcome failed. Test this option's stated failure mechanism first: a canonicalisation library on both sides, heavier than a single HMAC, and thin adoption outside standards-minded estates.

### Premortem for D. Asymmetric or provider-native, taken as given

Assume `D. Asymmetric or provider-native, taken as given` was selected and the outcome failed. Test this option's stated failure mechanism first: you inherit their gaps, and every provider is different, so a consumer library special-cases per provider. There is no convergence in the field (EV-0125).

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
`packs/architecture/wargames/WG-ARCH-007-vendor-seams.md`. The
surrounding controls, secret storage, SSRF on any URL the payload
carries, and log redaction, come from the security-privacy pack
(EV-0034, EV-0039).

## Safe default

B for anything we emit, five-minute tolerance. The provider's scheme
for anything we receive, behind an adapter, with our own replay window
and delivery-id idempotency store on top. Verification uses the standard
library, not a vendor SDK.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Are you receiving someone else's scheme, or emitting your own?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B for anything we emit, five-minute tolerance. The provider's scheme for anything we receive, behind an adapter, with our own replay window and delivery-id idempotency store on top. Verification uses the standard library, not a vendor SDK.

**Exit condition:** Stop or roll back the selected branch when no timestamp, so no replay window and no natural idempotency key; rotation means accepting two secrets by hand for a window, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Are you receiving someone else's scheme, or emitting your own?

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Are you receiving someone else's scheme, or emitting your own?** and **Does the delivery move money, grant access or change state you cannot undo?** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
