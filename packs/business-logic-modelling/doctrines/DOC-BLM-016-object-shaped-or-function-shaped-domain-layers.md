---
summary: Object-shaped or function-shaped domain layers.
type: doctrine
tags: [eos]
id: DOC-BLM-016
statement: Object-shaped or function-shaped domain layers.
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0272]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:preferences:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-BLM-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Behaviour-free
  objects with every rule in a service are called an anti-pattern
  (EV-0272), and the same source is content with a procedural service
  layer over a rich model.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:preferences:003`, lines 240-243, SHA-256 `8e4a0ece1179180aab0c78353ff14c32fb8d5646e356f63299415f4638fd497c`.
