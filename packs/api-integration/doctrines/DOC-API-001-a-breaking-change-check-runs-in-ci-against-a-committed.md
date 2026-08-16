---
summary: A breaking-change check runs in CI against a committed baseline, and fails the build.
type: doctrine
tags: [eos]
id: DOC-API-001
statement: A breaking-change check runs in CI against a committed baseline, and fails the build.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0135, EV-0136, EV-0139]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [BR-2]
---

# DOC-API-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

For HTTP that is `oasdiff breaking` against the
frozen previous revision (EV-0136); for protobuf it is the buf breaking
check (EV-0135); for a registry-backed event topic it is the registry's
own compatibility check (EV-0139). Prevents: shipping a break silently
and learning about it from a consumer. A published boundary carrying no
machine-readable contract cannot satisfy this, which is what D9 costs
when you depart from it, and why departing from D9 is done in writing
rather than in silence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:requirements:001`, lines 93-101, SHA-256 `980576a7338773d43ab582b1cb7e97016e0e0d45f05568a8dfc4ca44786eb379`.
