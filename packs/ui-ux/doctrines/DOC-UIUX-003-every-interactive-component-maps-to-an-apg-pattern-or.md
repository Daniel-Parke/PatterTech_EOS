---
summary: Every interactive component maps to an APG pattern or documents its deviation with a behaviour test.
type: doctrine
tags: [eos]
id: DOC-UIUX-003
statement: Every interactive component maps to an APG pattern or documents its deviation with a behaviour test.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0028, EV-0029]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-UIUX-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_user_interface`. The map
names the pattern, its keys and its states (EV-0028, EV-0029).
Prevents custom widgets that render correctly and cannot be operated.
Basis: standard. Binds for the same reason as B3: a control nobody can
operate by keyboard excludes that person from the task entirely. C8
carries focus visibility, which is a WCAG criterion in its own right
(EV-0027).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:003`, lines 125-132, SHA-256 `43bdf5efa470794572fbc2bce10780efce021540f039c688ed6ac8db95a279e2`.
