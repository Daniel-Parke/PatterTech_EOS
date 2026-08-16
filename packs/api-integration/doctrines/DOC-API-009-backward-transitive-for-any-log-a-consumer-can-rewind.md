---
summary: BACKWARD_TRANSITIVE for any log a consumer can rewind.
type: doctrine
tags: [eos]
id: DOC-API-009
statement: BACKWARD_TRANSITIVE for any log a consumer can rewind.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0139]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0139). Non-transitive modes check only the last version and give
  false comfort on replay.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:005`, lines 151-153, SHA-256 `3a60eea57e44f8ce56276d4c8af9ea8be3273a82c70a4fbf95d7da15e3fffe16`.
