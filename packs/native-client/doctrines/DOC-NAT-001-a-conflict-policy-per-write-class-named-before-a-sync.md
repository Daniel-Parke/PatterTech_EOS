---
summary: A conflict policy per write class, named before a sync library is chosen.
type: doctrine
tags: [eos]
id: DOC-NAT-001
statement: A conflict policy per write class, named before a sync library is chosen.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_local_write_store]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0379, EV-0383]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-NAT-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_local_write_store`. Every class is classified as
commutative, last-writer-acceptable or invariant-bearing, and each gets
exactly one policy from `converge`, `last-writer-wins`,
`reserve-then-commit` or `reject-offline`, recorded in a decisions file
citing at least three evidence ids. Reason: otherwise the library picks
the policy by default. Convergence proofs say replicas agree and no
update is lost, and say nothing about whether the agreed value
satisfies an invariant (EV-0379), while the shipped
server-authoritative product states outright that there is no single
correct choice for handling a write failure (EV-0383). Depart where
there is no local write store at all. Authority: default. Basis:
decision. See
`packs/native-client/wargames/WG-NAT-002-offline-write-model.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:001`, lines 115-128, SHA-256 `a83762c49f50a750fbb4cb046449cc05acaaec4334cdbb1ebc785ea0567fe04e`.
