---
summary: One time dimension until somebody has actually had to answer a two-dimensional question.
type: doctrine
tags: [eos]
id: DOC-BLM-006
statement: One time dimension until somebody has actually had to answer a two-dimensional question.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0275]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-BLM-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Add valid time and transaction time
together, or neither (EV-0275). Reason: the second dimension answers
what we thought was true when we ran the payroll, and it complicates
every reader of the model, which is the over-modelling D1 refuses.
Depart once a correction, a dispute or a reprocessing has been asked for
and the answer was not available.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:004`, lines 153-159, SHA-256 `d96a3324bd7d6e4a56a4fd317fde1ded59113ebacad58d14fd59cb97088dd103`.
