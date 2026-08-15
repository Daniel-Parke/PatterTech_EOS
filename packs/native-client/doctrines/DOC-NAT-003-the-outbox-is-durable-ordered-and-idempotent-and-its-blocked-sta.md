---
summary: The outbox is durable, ordered and idempotent, and its blocked state is named.
type: doctrine
tags: [eos]
id: DOC-NAT-003
statement: The outbox is durable, ordered and idempotent, and its blocked state is named.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_local_write_store]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0383]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-NAT-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_local_write_store`. A write acknowledged to the
user survives process death, replays without duplicating, and the
blocked state is surfaced within a stated timeout while reads keep
working. Reason: the two failures of a FIFO upload queue, the write
lost to a crash between acknowledgement and flush, and head-of-line
blocking, where one unacknowledged mutation stalls the whole client and
nothing on screen says so (EV-0383). Authority: default. Basis:
decision.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:003`, lines 142-150, SHA-256 `29e4e254e65a1b93ab1cdebdb489936da214eac3118db23ed957cbf01dfc2382`.
