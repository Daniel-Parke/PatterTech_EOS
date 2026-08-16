---
summary: Flake is a named state with an owner, never hidden behind retries.
type: doctrine
tags: [eos]
id: DOC-DEL-003
statement: Flake is a named state with an owner, never hidden behind retries.
kind: doctrine
authority: binding
basis: standard
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0015, EV-0195]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Blocking gates run zero retries. A test that cannot be
   made deterministic this week is quarantined out of the blocking path
   with a named owner; an unowned quarantine is a finding. Basis
   standard (EV-0015, EV-0195); the mechanics are in
   `packs/delivery-testing/references/FLAKE_AND_DETERMINISM.md`.
   Prevents: a green build that lies, and a quarantine queue nobody
   drains. The thirty-day expiry that used to sit inside this rule is
   now a default, because open question 4 below admits the number is our
   containment rather than a validated one, and a number we cannot
   defend should not need an ADR to move.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:requirements:004`, lines 120-130, SHA-256 `9c381f7bc9d0c6617cee62955a25698f7da4ff230e0f019966691a66d81bf079`.
