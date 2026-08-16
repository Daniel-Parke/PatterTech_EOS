---
summary: The routing loop has a budget, and the run records what it spent.
type: doctrine
tags: [eos]
id: DOC-LEGAL-015
statement: The routing loop has a budget, and the run records what it spent.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0069, EV-0225, EV-0337, EV-0338, EV-0339, EV-0340, EV-0341, EV-0342, EV-0343, EV-0344, EV-0345, EV-0346, EV-0347, EV-0348, EV-0349, EV-0350, EV-0351, EV-0352]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-LEGAL-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

One inventory pass, one decision pass, one re-check after the
fix. A run that has not converged inside that budget escalates rather
than iterating. Reason: this is a decision rather than evidence, and it
prevents exhaustive flailing that reads as diligence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:008`, lines 291-295, SHA-256 `fba4167df7ea58a64b8709a325a49cad04a97a82c5e5cd41eff0eee169b2698d`.
