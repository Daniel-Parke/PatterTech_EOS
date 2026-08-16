---
summary: An error renders adjacent to its cause, does not fire before the person has finished, and never destroys what they typed.
type: doctrine
tags: [eos]
id: DOC-WRIT-006
statement: An error renders adjacent to its cause, does not fire before the person has finished, and never destroys what they typed.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_forms]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0062, EV-0063, EV-0233, EV-0441]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-WRIT-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_forms`.
Placement and timing fail more often than wording
(EV-0441, EV-0233), and structural components exist
that fix placement so no writer has to remember it (EV-0062, EV-0063).
Prevents the well-written message rendered in a banner at the top of
the page, and prevents the retype. Basis: decision, on practitioner
consensus rather than a measured effect. Failed the basis leg. The part
of it that a statutory duty reaches is already carried by
`packs/ui-ux/` B3 and B4 through form labels and the keyboard contract.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:002`, lines 215-224, SHA-256 `0bd49f27aa1934d723e981fc90543ba4125577f0b82334b90380b2a77f01b9b9`.
