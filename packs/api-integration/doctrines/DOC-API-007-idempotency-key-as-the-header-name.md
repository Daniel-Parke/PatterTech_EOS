---
summary: Idempotency-Key as the header name.
type: doctrine
tags: [eos]
id: DOC-API-007
statement: Idempotency-Key as the header name.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0127, EV-0132]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

cited as de facto. The
  IETF draft has never reached RFC (EV-0127) and Azure mandates a
  different family (EV-0132), so this is a house choice, not a standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:003`, lines 145-147, SHA-256 `f6ad0163a7a6f55e8760fae6050fb8ae6b7906094de9529b2267a6d671e5b8b8`.
