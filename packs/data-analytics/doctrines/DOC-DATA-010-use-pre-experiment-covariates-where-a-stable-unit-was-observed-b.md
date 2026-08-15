---
summary: Use pre-experiment covariates where a stable unit was observed before the test.
type: doctrine
tags: [eos]
id: DOC-DATA-010
statement: Use pre-experiment covariates where a stable unit was observed before the test.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0315]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-DATA-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Variance reduction from pre-period behaviour bought
roughly half the variance at Bing, which is the same power at half the
users (EV-0315). Reason: sensitivity is cheaper than traffic. It does
nothing for new users, first-session funnels or anonymous traffic, so
the default holds only where the precondition does.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:007`, lines 189-194, SHA-256 `81784fe77859ec34417ca98ed893f885b6a5887c8287ab6b92cb5bb9117ad6e0`.
