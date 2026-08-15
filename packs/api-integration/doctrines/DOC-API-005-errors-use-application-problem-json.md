---
summary: Errors use application/problem+json.
type: doctrine
tags: [eos]
id: DOC-API-005
statement: Errors use application/problem+json.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0122, EV-0132]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0122). One
  negotiated container with a stable type URI a consumer can branch on.
  Override where a platform mandates a different envelope (EV-0132).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:001`, lines 138-140, SHA-256 `abc16753439f7e388809645399a26a28790ac3bc57646634d485df928dd410bc`.
