---
summary: Split only on a measured signal, never on a label.
type: doctrine
tags: [eos]
id: DOC-ARCH-005
statement: Split only on a measured signal, never on a label.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0151]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-ARCH-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The signals
are DORA's: changes needing approval outside the owner, inability to
test in isolation, and unplanned work caused by upstream change
(EV-0151). DORA is explicit that the label does not determine the
outcome.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:002`, lines 151-155, SHA-256 `e5c8e59da0f58159fe860b77d86234fff03db5e35ebb71fcec813e8f8f079818`.
