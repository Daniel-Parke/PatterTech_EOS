---
summary: Layout slack sized for two to three times expansion on strings under ten characters.
type: doctrine
tags: [eos]
id: DOC-WRIT-014
statement: Layout slack sized for two to three times expansion on strings under ten characters.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0445]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
---

# DOC-WRIT-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0445). Buttons, tabs and
  labels are the shortest strings and therefore the highest risk. The
  figures cover English into European languages only.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:010`, lines 286-289, SHA-256 `6e05693675cd3bb5ad6ab0b666308754d8eca65e3c61f7c5b4aedf0200897c30`.
