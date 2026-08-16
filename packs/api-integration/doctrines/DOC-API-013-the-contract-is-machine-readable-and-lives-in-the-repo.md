---
summary: The contract is machine-readable and lives in the repo.
type: doctrine
tags: [eos]
id: DOC-API-013
statement: The contract is machine-readable and lives in the repo.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0023, EV-0024, EV-0144]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A
  boundary we publish carries a committed OpenAPI 3.x document
  (EV-0023), AsyncAPI document (EV-0024) or protobuf definition,
  versioned with the code. Reason: prose cannot be diffed, generated
  from or tested against, and under-specified contracts cap every
  downstream automation (EV-0144). This is a default rather than binding
  because what it names is a missing artefact, not a failure; the
  failure is a break reaching a consumer, and BR-2 is what stops that.
  Departing costs you BR-2, so the recorded reason has to say how the
  break gets caught instead.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:009`, lines 165-174, SHA-256 `b753d011f9666445b556efaee00385a92f9d613060a90c0fef6a5e6b4fcdc57a`.
