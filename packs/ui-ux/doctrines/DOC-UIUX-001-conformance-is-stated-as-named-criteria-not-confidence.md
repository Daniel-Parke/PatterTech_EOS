---
summary: Conformance is stated as named criteria, not confidence.
type: doctrine
tags: [eos]
id: DOC-UIUX-001
statement: Conformance is stated as named criteria, not confidence.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-UIUX-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_web_ui`. A surface claiming WCAG 2.2 at a level names the level
and the criteria that pass (EV-0027). The artefact is a conformance
record listing the version, the level, every criterion in that level
and that criterion's verdict. C17 settles that the record exists and is
complete; C5 supplies the machine-decidable half of the verdicts in it.
A claim with no such record fails whatever the scanner says, which is
what C17 is for. Prevents a conformance claim that rests on how the
reviewer felt. Basis: standard. Binds because the claim is a public
statement that cannot be withdrawn from the people who read it, and
where `statutory_a11y_duty` holds it is a legal one.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:001`, lines 104-114, SHA-256 `7b4b714db3ed1afd7ea32fe7fa4a3c57d8ea6666a194b14ab3fe538b867d49e8`.
