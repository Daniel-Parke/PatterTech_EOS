---
summary: A pseudo-locale build passes before any string reaches a translator.
type: doctrine
tags: [eos]
id: DOC-WRIT-005
statement: A pseudo-locale build passes before any string reaches a translator.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [ships_second_locale]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0446]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-WRIT-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`ships_second_locale`. No truncation, no missing glyphs,
no unexternalised strings (EV-0446). Prevents paying
for the same mechanical defect in every locale at once, which is what
happens when the first real translation is also the first test.
Basis: decision, taken on vendor guidance rather than on a trial. The
source is a maintainer document last touched in 2024 with an
unverified licence, and no study of its effect was found. Failed the
basis leg, on that admission.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:001`, lines 205-213, SHA-256 `84791e6b6e0c640d8c5e2f8a86ca36be4aa625a5bf86d82a6c2447dfa1bc0378`.
