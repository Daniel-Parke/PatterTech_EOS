---
summary: The repricing trigger is written before it fires.
type: doctrine
tags: [eos]
id: DOC-BMP-012
statement: The repricing trigger is written before it fires.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0096]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-BMP-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Agree in
advance what movement in cost or delivered value opens a price change,
and what the response is, in the shape of a pre-agreed error budget
policy (EV-0096). Reason: a trigger written after the pressure arrives
is negotiated under the pressure.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:defaults:008`, lines 214-218, SHA-256 `79d4beeff12dbd4f91cedce214fc2f2f91dad5db20bfcd04e2a44f810f42537c`.
