---
summary: Client and server contracts change by expand, migrate, contract.
type: doctrine
tags: [eos]
id: DOC-NAT-007
statement: Client and server contracts change by expand, migrate, contract.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0171, EV-0206]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-NAT-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`ships_a_binary`. The new shape ships alongside the old,
waits out the installed base, then the old is removed (EV-0206).
Reason: a server release otherwise breaks a binary its user cannot
update today and may never update, and version numbers mean nothing
until that surface is declared precisely (EV-0171). Depart only where
every client is known to be current and the venture can prove it.
Authority: default, because the pattern is a ruling of ours and the
source behind it is one practitioner's write-up. Basis: decision.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:007`, lines 190-198, SHA-256 `1c11fc03ae4dd1025a28daedd59bec01ec7c7d9f74001089453b705441be27d5`.
