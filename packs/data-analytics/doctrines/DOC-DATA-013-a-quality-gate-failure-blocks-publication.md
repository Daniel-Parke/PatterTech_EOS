---
summary: A quality gate failure blocks publication.
type: doctrine
tags: [eos]
id: DOC-DATA-013
statement: A quality gate failure blocks publication.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0056, EV-0306]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D10]
---

# DOC-DATA-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`publishes_analytics_table`. A rule that raises a ticket while the table
publishes is monitoring, not a gate. Quality rules run inside the
pipeline as part of the build, not as a separate audit afterwards
(EV-0306, EV-0056). Reason: the documented-gate failure, a contract
written and never executed, which is documentation wearing a gate's
clothes. This is a default rather than binding because the evidence
behind it shows that in-pipeline checking works at scale, not that
blocking beats alerting; that comparison has not been run. Departing
means recording what stops bad data reaching a decision instead, and
saying it out loud, because a gate demoted to a monitor is the thing
this pack most often finds.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:010`, lines 215-226, SHA-256 `2e90ff5dd8c7aaaba7941e651af4bb9dd79569a58165dd7d0d0a243b240cd223`.
