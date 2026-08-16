---
summary: The compatibility promise is declared before the first change.
type: doctrine
tags: [eos]
id: DOC-API-014
statement: The compatibility promise is declared before the first change.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0135, EV-0139]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A parseable line in DECISIONS.md or an ADR records the
  versioning approach and the tier or mode, for example a
  `compatibility` line naming BACKWARD. Tiers come from the toolchain in
  use: FILE, PACKAGE, WIRE_JSON or WIRE for protobuf (EV-0135);
  BACKWARD, FORWARD, FULL, NONE and their transitive variants for events
  (EV-0139). Reason:
  otherwise you discover your own promise by breaking someone. This is a
  default rather than binding because the gate in BR-2 still runs
  without it, at whatever strictness the tool defaults to, so the cost
  of departing is that you have accepted that default sight unseen.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:010`, lines 175-185, SHA-256 `c8a5a00290f364c326c00f35d5f58c87cc6de706a54d06d76c2e5f777ab8ba7e`.
