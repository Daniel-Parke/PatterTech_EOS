---
summary: Budget one rejection cycle into every release calendar.
type: doctrine
tags: [eos]
id: DOC-NAT-011
statement: Budget one rejection cycle into every release calendar.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0373]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-NAT-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Roughly
one submission in four was rejected in the 2025 reporting year, the
largest bucket by a wide margin being Performance (EV-0373).
That is a vendor census of its own decisions and sizes a calendar risk
only; the scope note sits in
`packs/native-client/references/RELEASE_MECHANICS.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:004`, lines 222-227, SHA-256 `41b9ab8bc33bde8681fb3cf1337be6004d2a111c26d3b647767dde536aae6bec`.
