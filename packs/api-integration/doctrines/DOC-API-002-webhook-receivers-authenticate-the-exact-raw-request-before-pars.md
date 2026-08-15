---
summary: Webhook receivers authenticate the exact raw request before parsing, reject stale deliveries, and process accepted deliveries idempotently against a pinned payload version.
type: doctrine
tags: [eos]
id: DOC-API-002
statement: Webhook receivers authenticate the exact raw request before parsing, reject stale deliveries, and process accepted deliveries idempotently against a pinned payload version.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [receives_webhooks]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0125, EV-0126, EV-0161]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:requirements:002, packs/architecture/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5, BR-4]
---

# DOC-API-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

### `packs/api-integration/PACK.md:requirements:002`

The signature is
computed over the exact bytes received, compared in constant time
(`hmac.compare_digest`, `crypto.timingSafeEqual` or `secure_compare`),
and rejected outside a numeric timestamp tolerance. A framework that
hands the handler a parsed object has already destroyed the bytes the
signature covers (EV-0126, EV-0125). Prevents: forged deliveries and
replayed deliveries, both of which are free to an attacker otherwise.
The ADR-0008 audit left this one alone even though EV-0126 is vendor
documentation: verifying the authenticity of an inbound message is a
security floor, and a floor stays binding whatever its basis field says.

### `packs/architecture/PACK.md:requirements:003`

No framework body
parsing ahead of verification, non-zero replay tolerance, idempotency
keys on the handler, and the payload version pinned. Evidence: Stripe
webhook documentation (EV-0161), paraphrased. Prevents: a forged or
replayed event accepted as truth, and the specific defect where
middleware re-serialises the body and destroys the signature. The
ADR-0008 audit left this one alone even though its only source is
vendor documentation: verifying the authenticity of an inbound message
is a security floor, and a floor stays binding whatever its basis field
says. This is BR-4 of `packs/api-integration/PACK.md`, stated in both
because the two packs activate on different triggers and a floor cannot
depend on which one fired. The mechanics belong to that pack and are
not repeated here: the order of operations, the tolerance, rotation and
the provider variance that defeats one implementation are in
`packs/api-integration/refs/webhook-verification.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:requirements:002`, lines 103-112, SHA-256 `fbb048f113f2f59e6c40ff5d43591a05955f4824b402d6c8f9f7d051750bcf71`.
- `packs/architecture/PACK.md:requirements:003`, lines 122-137, SHA-256 `51a8d955b9c6ffdf1b4cba58816b3696c9907d0e31bed1915ddd83d40355ed70`.
