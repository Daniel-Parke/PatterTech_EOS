---
summary: Money is an integer count of minor units carrying its currency code.
type: doctrine
tags: [eos]
id: DOC-BLM-001
statement: Money is an integer count of minor units carrying its currency code.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [models_money]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0283, EV-0284]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-BLM-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`models_money`. No float, no bare number, no assumption that the
exponent is two. The published lists carry an alphabetic code, a numeric
code and a minor unit exponent per currency, and that exponent varies
(EV-0283); the largest payment provider represents every amount the same
way (EV-0284). Arithmetic between two currencies is refused rather than
coerced, and a stored amount keeps the code it was denominated in,
because currencies retire (EV-0283). Prevents the defect nobody sees
until reconciliation: binary fractions that do not sum, and a total out
by a factor of a hundred in the one currency nobody tested. Basis:
standard. See
`packs/business-logic-modelling/refs/MONEY_AND_CURRENCY.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:requirements:001`, lines 98-109, SHA-256 `b0e587be1ea14f59b5814eaa7171ecd6c79a65bf095f009eae152d6106c89fce`.
