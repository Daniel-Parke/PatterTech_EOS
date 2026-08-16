---
summary: Schema-derived property tests against the contract.
type: doctrine
tags: [eos]
id: DOC-API-010
statement: Schema-derived property tests against the contract.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0091, EV-0143]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0143,
  1.4 to 4.5 times more unique defects than the next-best fuzzer across
  sixteen services; preprint, authors evaluating their own tool), plus
  consumer-driven contract tests where two teams share a boundary
  (EV-0091).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:006`, lines 154-158, SHA-256 `021fd3c507a0224cae4ef4edfa378022c8c9e9cc9d874f330221f559324f26eb`.
