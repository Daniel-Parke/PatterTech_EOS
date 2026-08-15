---
summary: Defer domain grouping and per-domain gateways until service count makes them a real problem.
type: doctrine
tags: [eos]
id: DOC-ARCH-020
statement: Defer domain grouping and per-domain gateways until service count makes them a real problem.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0160]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:preferences:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-ARCH-020

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Uber reached for them at roughly 2,200 services (EV-0160).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:preferences:005`, lines 241-243, SHA-256 `ac821cbbc40c6382eb63e1d3ed127176e2355eca81ee97c1043fbfa0d2dcb979`.
