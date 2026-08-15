---
summary: Every commercial number travels with its definition.
type: doctrine
tags: [eos]
id: DOC-BMP-009
statement: Every commercial number travels with its definition.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0199, EV-0210]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-BMP-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The formula
sits next to the number, and a definition change is stated in the report
where it happens. Reason: this mirrors the metric hygiene the DORA and
SPACE work insists on (EV-0199, EV-0210), and no primary source was
found at the cutoff that fixes ARR, net revenue retention or churn.
Honest weakness: an attempt to anchor this in the SEC release on key
performance indicators failed because the source could not be fetched,
so D5 rests on internal reasoning and is weaker than it should be. See
`packs/business-model-pricing/refs/METRIC_DEFINITIONS.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:defaults:005`, lines 191-199, SHA-256 `dd2ab451a2fdc62ae9ed681a67951d21b52403c69461b02910469be5450ea7eb`.
