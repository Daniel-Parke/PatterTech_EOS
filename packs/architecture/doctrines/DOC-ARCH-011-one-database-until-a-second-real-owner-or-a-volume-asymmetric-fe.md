---
summary: One database until a second real owner or a volume-asymmetric feed appears, and records never mingle with readings.
type: doctrine
tags: [eos]
id: DOC-ARCH-011
statement: One database until a second real owner or a volume-asymmetric feed appears, and records never mingle with readings.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0162]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-ARCH-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: ownership and
physical separation are different decisions, and private tables with
distinct credentials enforce ownership without paying for sagas and
cross-database joins (EV-0162).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:008`, lines 186-190, SHA-256 `64f2fd94b209a30b9aa25cea39211e8e753b84a76b0e7053d921e8a2cd7ce2a3`.
