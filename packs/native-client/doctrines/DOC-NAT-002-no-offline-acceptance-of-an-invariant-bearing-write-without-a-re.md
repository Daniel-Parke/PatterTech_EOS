---
summary: No offline acceptance of an invariant-bearing write without a reservation or compensation path.
type: doctrine
tags: [eos]
id: DOC-NAT-002
statement: No offline acceptance of an invariant-bearing write without a reservation or compensation path.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_local_write_store]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0379]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-NAT-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_invariant_bearing_writes` and
`has_local_write_store`. Either the client holds a server-issued
reservation before accepting the write, or the write is rejected
offline, or a named compensation event fires for the loser on
reconnection. Reason: two users hold one slot after a merge the
algorithm correctly calls converged (EV-0379), and a booking made twice
is a promise to a person that cannot be unmade by a later commit.
Authority: default only because the remedy is our ruling rather than a
published rule; the failure under it is the worst in this pack, and a
departure is a lock-book entry a reviewer will read. Basis: decision.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:002`, lines 130-140, SHA-256 `caf75703beef3a727b56303612de4b5deb763669afcd9f932833f4958c8b0ebe`.
