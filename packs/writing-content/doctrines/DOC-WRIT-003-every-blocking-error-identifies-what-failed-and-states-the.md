---
summary: Every blocking error identifies what failed and states the required input or the next action.
type: doctrine
tags: [eos]
id: DOC-WRIT-003
statement: Every blocking error identifies what failed and states the required input or the next action.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_forms]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0447]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-WRIT-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_forms`. WCAG 2.2 success
criteria 3.3.1 and 3.3.3 make this a conformance obligation where they
apply (EV-0027). Replacing a diagnosis with the shape of a correct
answer is the highest-yield rewrite in the set
(EV-0447). Prevents `Invalid input`, which tells the
reader only that they have failed. Basis: standard. Binds because a
person who cannot tell what a good answer looks like cannot finish the
form at all, which is serious wherever the duty in 3.3.1 reaches and
wherever it does not.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:requirements:003`, lines 174-183, SHA-256 `cbcb5eff0d557d0840c79035ec3e8c2c02df7dfd559942e19b36b042c301d963`.
