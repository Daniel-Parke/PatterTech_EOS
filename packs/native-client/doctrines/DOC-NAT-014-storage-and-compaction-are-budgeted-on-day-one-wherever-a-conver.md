---
summary: Storage and compaction are budgeted on day one wherever a convergent store is used.
type: doctrine
tags: [eos]
id: DOC-NAT-014
statement: Storage and compaction are budgeted on day one wherever a convergent store is used.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0381]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-NAT-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Text-suitable CRDTs only grow and the
answer is conditional tombstone collection (EV-0381). Reason:
compaction found at month six is a migration, not a tuning pass.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:007`, lines 240-243, SHA-256 `8b71b146f0afa599e360e7b1af8b297ce229e0ac457c8d528becf92f5da21ea6`.
