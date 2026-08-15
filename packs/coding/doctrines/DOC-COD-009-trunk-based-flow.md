---
summary: Trunk-based flow.
type: doctrine
tags: [eos]
id: DOC-COD-009
statement: Trunk-based flow.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0168, EV-0183]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-COD-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Small changes merged to trunk at least daily,
branch lifetime measured in hours, three or fewer active branches, no
code freezes (EV-0168). Large changes ride behind feature flags or
branch by abstraction rather than a long branch (EV-0183). Reason: the
conditions are measurable and the association with delivery performance
is the best evidence available. Both sources are association or opinion
rather than causal evidence, and for a one-person venture the residue
that matters is merge cadence and the ban on freezes.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:003`, lines 216-223, SHA-256 `bded4021bb988671cf34c938e9bcae3dd8d4dbf87f2a9496719620a78d7d3abc`.
