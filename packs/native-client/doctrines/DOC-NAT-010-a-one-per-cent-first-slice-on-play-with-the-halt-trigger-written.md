---
summary: A one per cent first slice on Play with the halt trigger written down before the release starts, and phased release left on for Apple.
type: doctrine
tags: [eos]
id: DOC-NAT-010
statement: A one per cent first slice on Play with the halt trigger written down before the release starts, and phased release left on for Apple.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0374, EV-0375]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-NAT-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: Play's only real containment lever is how small the first slice
is (EV-0375) and Apple's ramp is fixed, unsteerable and
bypassable by anyone updating manually (EV-0374), so the trigger
comes from your own telemetry on both.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:003`, lines 215-220, SHA-256 `c879d056fe21ba0228be722aaf884aca4cdcc432432956de0eaaf8af65db55d4`.
