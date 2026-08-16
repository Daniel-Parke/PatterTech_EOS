---
summary: Fixed horizon, unless a sequential method is chosen deliberately and written into the stopping rule.
type: doctrine
tags: [eos]
id: DOC-DATA-006
statement: Fixed horizon, unless a sequential method is chosen deliberately and written into the stopping rule.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0312, EV-0313, EV-0317]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-DATA-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: a correctly powered
fixed-horizon test left alone is the most powerful option per unit of
traffic (EV-0313). Where people will look anyway, fix the statistic
rather than the operator: always-valid and group sequential methods make
monitoring supported (EV-0312) and ship in a maintained Apache-2.0
library, so this is not a reason to buy a platform (EV-0317).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:003`, lines 162-168, SHA-256 `4d2be8cd1b6e45673510d0db77340a29dd0a95854e7944d71ed915558ded0fb4`.
