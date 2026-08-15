---
summary: A fact model declares its grain in words before it declares columns.
type: doctrine
tags: [eos]
id: DOC-DATA-014
statement: A fact model declares its grain in words before it declares columns.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0308]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D11]
---

# DOC-DATA-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`publishes_analytics_table`. One sentence naming what one row
is. Reason: the unauditable table. Without a stated grain nobody can say
whether a count is double-counting, and every downstream number inherits
the ambiguity. Grain-first is the first of the three ordered dimensional
decisions and survives every argument about physical shape (EV-0308).
This is the grade the research gave it, and the ADR-0008 audit returned
it there: EV-0308 is a practice body with no measurement behind it, and
the failure is a number nobody can audit rather than one nobody can
undo.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:011`, lines 228-237, SHA-256 `159cc5b071f6641066b3515577995b52dd49f5f83a1e843eb78c9c7ce68cd98b`.
