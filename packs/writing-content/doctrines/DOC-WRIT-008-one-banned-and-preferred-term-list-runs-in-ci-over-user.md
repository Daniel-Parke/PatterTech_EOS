---
summary: One banned-and-preferred term list runs in CI over user-facing strings and documentation, and only one prose linter exists in the repository.
type: doctrine
tags: [eos]
id: DOC-WRIT-008
statement: One banned-and-preferred term list runs in CI over user-facing strings and documentation, and only one prose linter exists in the repository.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0335]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-WRIT-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`writes_user_facing_text`. Vale is the recorded tool
(EV-0335). Prevents two spellings of one action reaching a
translator as two concepts, and prevents the second linter that
disagrees with the first. Basis: decision, and an admittedly cheap
bet: no study was found showing that a maintained termbase improves
comprehension or reduces support load. Failed the basis leg, on that
admission.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:004`, lines 236-244, SHA-256 `58055b74a999a1f5a0be29b2db175e89dc9fa0033eca6fe237d8df58aec1df4b`.
