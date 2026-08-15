---
summary: Below the traffic for a properly powered test, do not run one.
type: doctrine
tags: [eos]
id: DOC-DATA-007
statement: Below the traffic for a properly powered test, do not run one.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0059, EV-0313]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-DATA-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

An underpowered test launders a coin flip as evidence and is worse than
an argued decision with an instrumented rollout. Reason: with a low
prior on any idea working, a bare significant result from a small sample
is more likely false than a naive reading suggests (EV-0313). No source
says this plainly, because none was written for a venture. Decide by
argument, ship behind a flag, watch a guardrail (EV-0059).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:004`, lines 170-176, SHA-256 `5d67c2a04ad939b583355eab64904ffff93b2834446403797897085bbbe23c7c`.
