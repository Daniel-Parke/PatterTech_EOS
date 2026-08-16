---
summary: Shared logic with a native user interface.
type: doctrine
tags: [eos]
id: DOC-NAT-008
statement: Shared logic with a native user interface.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0386]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-NAT-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Sharing domain logic
and sharing pixels are two decisions; the first is graded Stable per
target while the interface layer carries its own grade
(EV-0386). Reason: it removes business-rule divergence without
forfeiting platform behaviour.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:001`, lines 204-208, SHA-256 `bb1d68af35347c68c1359bf76799429886ed98cfa5b661a5376723675c514c3d`.
