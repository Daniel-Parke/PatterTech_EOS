---
summary: No target and no published figure is the mean of a duration distribution.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-006
statement: No target and no published figure is the mean of a duration distribution.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [reports_support_metric]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0211]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-SUPPORT-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`reports_support_metric`. Incident and response
durations are reported as percentiles, as raw counts, or not at all
(EV-0211). Per-band time targets are not set, because the corpus that
looked found no correlation between duration and severity. Basis:
empirical-evidence. Prevents a target that describes no incident that
ever happened, and prevents a skewed distribution being summarised by
the one statistic it defeats. Failed the seriousness leg: a bad metric
is replaced by a better one at no cost, and the number itself harms
nobody.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:004`, lines 203-212, SHA-256 `82c9c36411c77fb5ecb23f19c6a0eec3aa3f931cc2c1c0f28c173bb0bf211b3f`.
