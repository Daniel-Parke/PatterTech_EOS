---
summary: Every persisted table names its consumer and its retention plan before it lands.
type: doctrine
tags: [eos]
id: DOC-ARCH-012
statement: Every persisted table names its consumer and its retention plan before it lands.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-ARCH-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: local observation across three ventures that
unowned tables become unbounded ones. Grade: anecdotal, and it is a
default for exactly that reason.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:009`, lines 192-195, SHA-256 `a0c6563e2e3a783be8aaf39f40ecac0da33376d928bbdbb44821e3d2d1c15dd8`.
