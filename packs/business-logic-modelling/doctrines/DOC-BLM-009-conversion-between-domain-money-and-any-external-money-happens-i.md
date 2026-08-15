---
summary: Conversion between domain money and any external money happens in one adapter.
type: doctrine
tags: [eos]
id: DOC-BLM-009
statement: Conversion between domain money and any external money happens in one adapter.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0150, EV-0284]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-BLM-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The minor-unit exponent is a property of a currency in a
context, not of the currency alone: the same provider charges some
currencies with two decimals and pays them out whole (EV-0284). Reason:
one place to be wrong, and the domain keeps one representation
(EV-0150).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:007`, lines 177-182, SHA-256 `c3ad83f9aba19b82f71197359a2b5f60b830e1ea1c40242762234e6709a8bf56`.
