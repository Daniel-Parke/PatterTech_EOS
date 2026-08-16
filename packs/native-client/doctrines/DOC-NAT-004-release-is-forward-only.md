---
summary: Release is forward-only.
type: doctrine
tags: [eos]
id: DOC-NAT-004
statement: Release is forward-only.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [distributes_via_app_store]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0026, EV-0374, EV-0375]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-NAT-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`distributes_via_app_store`. Every
shipping binary carries a remote kill switch for the behaviour it
introduces, and no runbook step says roll back. Apple ramps automatic
updates on a fixed schedule with no developer dial and no rollback
(EV-0374); Play gives the dial and a halt, but halting only
stops further delivery and the documented remedy for a bad build is to
ship another one (EV-0375). Flags are the rollback on a client
(EV-0026). Prevents an incident plan whose first step is impossible.
Authority: binding. Basis: standard. See
`packs/native-client/wargames/WG-NAT-003-release-path.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:004`, lines 152-161, SHA-256 `e42bc59cba4380807344663e0499f9719430e709984514b273361785a7516642`.
