---
summary: The quality tool.
type: doctrine
tags: [eos]
id: DOC-DATA-017
statement: The quality tool.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0056, EV-0306]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:preferences:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DATA-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Declared expectations (EV-0056) and computed metrics with anomaly detection (EV-0306) both work.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:preferences:003`, lines 249-250, SHA-256 `2cb5f82943364e96cbe031c01508b4d39498956984ab1c3eaaa78e2bd86bc32c`.
