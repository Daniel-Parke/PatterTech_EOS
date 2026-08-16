---
summary: Retention is reported as a cohort curve, and lifetime value is never revenue over blended churn.
type: doctrine
tags: [eos]
id: DOC-BMP-008
statement: Retention is reported as a cohort curve, and lifetime value is never revenue over blended churn.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0296]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-BMP-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: the observed period-over-
period retention rate of a cohort rises with age purely because
high-churn customers leave first, so a single average churn projected
forward is wrong in a knowable direction (EV-0296). Scope note: the
model needs several periods of contractual cohort data, which a
first-year venture does not have; until then report the observed curve
and refuse the single number. See
`packs/business-model-pricing/references/RETENTION_AND_LTV.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:defaults:004`, lines 181-189, SHA-256 `96cda1ec075b81dba3c3fe2b7b4d4c75848252ca8c437fd2ad59ee3f92815495`.
