---
summary: Deprecation and removal are two dated events, and removal is never the earlier one.
type: doctrine
tags: [eos]
id: DOC-API-004
statement: Deprecation and removal are two dated events, and removal is never the earlier one.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0124, EV-0129]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [BR-6]
---

# DOC-API-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Announce deprecation in band with a date, carry
a separate sunset date, and do not remove before it (EV-0124). A rename
is a removal plus an addition and is therefore breaking: add the new
name, mark the old one deprecated, and let both resolve until sunset
(EV-0129). Adding a required field to a request is equally breaking, so
it ships behind a version discriminator, never in place. Prevents: the
silent removal that only the consumer discovers.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:requirements:004`, lines 124-131, SHA-256 `3fff60abfe5e0be516ff2a3917f260caafa64f53fcce44f138bf9595d0414f0f`.
