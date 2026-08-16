---
summary: Cursor pagination with opaque tokens, no offset.
type: doctrine
tags: [eos]
id: DOC-API-006
statement: Cursor pagination with opaque tokens, no offset.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0130]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0130).
  Tokens bind to the filter and ordering of the issuing call and carry
  no authorisation. Override for a table UI that needs page numbers, see
  `packs/api-integration/wargames/WG-API-005-collection-traversal.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:002`, lines 141-144, SHA-256 `a161794ce5573625bcb882c8a1bb1b2cee06e928836cf0048c1f840cf82c8b5a`.
