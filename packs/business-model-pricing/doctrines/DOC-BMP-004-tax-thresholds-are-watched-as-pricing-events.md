---
summary: Tax thresholds are watched as pricing events.
type: doctrine
tags: [eos]
id: DOC-BMP-004
statement: Tax thresholds are watched as pricing events.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0303, EV-0304]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-BMP-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Predicates:
sets_a_price, reports_commercial_metrics. VAT registration is compulsory
once taxable turnover over any rolling twelve months exceeds ninety
thousand pounds, or is expected to within thirty days (EV-0303). Making
Tax Digital for Income Tax starts 6 April 2026 above fifty thousand
pounds of qualifying income, 2027 above thirty thousand and 2028 above
twenty thousand (EV-0304). Prevents crossing the VAT threshold and
discovering the effective consumer price has fallen by the VAT rate
overnight. Both are dated policy numbers with refresh triggers, held in
`packs/business-model-pricing/references/UK_OBLIGATIONS.md`, never inlined
elsewhere.

Guarded actions stay outside this pack. Taking money, refunding money
and changing a live price are ruled by `kernel/GUARD_SPEC.md` and its
non-waivable floors. No pricing argument changes a guard verdict.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:requirements:004`, lines 130-144, SHA-256 `c5f68be266395fdb5d9518c2b546c19c89613ca36affb220aad20b0de76de89d`.
