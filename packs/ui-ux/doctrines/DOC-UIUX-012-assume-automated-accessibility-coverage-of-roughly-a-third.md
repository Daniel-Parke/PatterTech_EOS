---
summary: Assume automated accessibility coverage of roughly a third.
type: doctrine
tags: [eos]
id: DOC-UIUX-012
statement: Assume automated accessibility coverage of roughly a third.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0104, EV-0236]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-UIUX-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

not
  the tool vendor's 57 per cent, when deciding what a passing build
  proves (EV-0236, EV-0104).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:defaults:006`, lines 220-222, SHA-256 `f0ff25f27f01b02ae514de44168c97e1afcc3a896ea04b54586d5807140d96df`.
