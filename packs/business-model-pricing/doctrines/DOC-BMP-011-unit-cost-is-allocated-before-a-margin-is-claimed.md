---
summary: Unit cost is allocated before a margin is claimed.
type: doctrine
tags: [eos]
id: DOC-BMP-011
statement: Unit cost is allocated before a margin is claimed.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0197]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-BMP-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every charged
unit carries an allocated cost to serve, using the FinOps allocation the
devops-reliability pack owns (EV-0197). Reason: a margin percentage
without an allocation is a guess wearing a decimal point.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:defaults:007`, lines 209-212, SHA-256 `bac96ed9b9fec4f10dd46381adac4c3c3e2bdefa56d31c0cce5847cc8caa55d2`.
