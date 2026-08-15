---
summary: A discovery record exists and names the decision it unblocks.
type: doctrine
tags: [eos]
id: DOC-DISC-003
statement: A discovery record exists and names the decision it unblocks.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0410]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-DISC-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`proposes_capability`. The record carries the fixed sections set out in
`packs/product-discovery/refs/DISCOVERY_RECORD.md`. Prevents the
proposal that cannot be wrong: the goals-signals-metrics ladder holds
that a proposal with no stated signal is untestable and that a metric
picked before its goal is a vanity metric by construction
(`EV-0410`). Basis: decision, on that ladder. Failed the basis leg: one
consultancy ladder, never evaluated.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:001`, lines 143-150, SHA-256 `4c44b6deaba6a58e89474cb515e677d8e56f663dbc913d9f46fd643734147479`.
