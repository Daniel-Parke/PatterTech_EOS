---
summary: A lifecycle with forbidden transitions is an explicit machine, and an illegal transition raises rather than doing nothing quietly.
type: doctrine
tags: [eos]
id: DOC-BLM-005
statement: A lifecycle with forbidden transitions is an explicit machine, and an illegal transition raises rather than doing nothing quietly.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0279, EV-0280]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-BLM-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A
declared machine refuses what a set of booleans merely fails to notice,
and hierarchy plus parallel regions stop the state explosion that makes
flat machines unusable (EV-0279, EV-0280). Reason: a silent no-op leaves
the caller believing the change happened. Depart when the lifecycle has
no forbidden transition at all.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:003`, lines 145-151, SHA-256 `b69c2bc1ae7b858171bedf4e6fffcbefb52e2f93f37349c1e4376fbb43b31cb5`.
