---
summary: A loyalty or satisfaction score is a trend about one population, never a cross-firm benchmark.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-007
statement: A loyalty or satisfaction score is a trend about one population, never a cross-firm benchmark.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [reports_support_metric]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0428]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-SUPPORT-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`reports_support_metric`. The score is
reported with its population, its n and its date range, and it is never
used to claim a position relative to another company or an industry
figure (EV-0428). Basis: empirical-evidence.
Prevents an instrument being sold internally as evidence it has been
tested for and failed to provide. Scope note: the replication that
settles this covered 21 firms and more than 15,500 interviews from one
national panel, in industries and an era that predate subscription
software. It refutes a superiority claim; it does not show the score is
useless, and it says nothing about behaviour at the sample sizes a
venture with sixty customers actually has. Failed the seriousness leg
by the same reasoning as B5. Publishing the comparison outside the
venture is a marketing claim and belongs to `packs/marketing-growth/`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:005`, lines 214-227, SHA-256 `6d15c05445cddbf8a99bfad3c74d0d3814d90eefc29b3d283c3605508ab9be65`.
