---
summary: Rules stay in code until they change on a different clock from the code.
type: doctrine
tags: [eos]
id: DOC-BLM-008
statement: Rules stay in code until they change on a different clock from the code.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0274, EV-0277, EV-0278]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-BLM-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

When they do, move them to a flat decision table with declared
inputs, outputs and overlap handling, never to a chaining inference
engine (EV-0277, EV-0278). Reason: with chaining, one rule's action
satisfies another's condition and nobody predicts the outcome from
reading any single rule (EV-0274), while a flat table is a closed form
whose completeness is machine-checkable. A handful of rules earns
neither. See
`packs/business-logic-modelling/guides/GD-BLM-002-rule-placement.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:006`, lines 167-175, SHA-256 `0b5eb662d5272f6c194cd90a4f30bbd3cb89486e6b566f4b33bbb213757deaf6`.
