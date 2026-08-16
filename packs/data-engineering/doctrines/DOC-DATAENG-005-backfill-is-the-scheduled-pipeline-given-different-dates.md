---
summary: Backfill is the scheduled pipeline given different dates.
type: doctrine
tags: [eos]
id: DOC-DATAENG-005
statement: Backfill is the scheduled pipeline given different dates.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-DATAENG-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No
separate backfill script, no notebook, no one-off query. The microbatch
documentation makes this the shape rather than the exception: the same
model run with an explicit start and end, batch by batch, each one
replaced atomically. *Reason to depart*: a first historical load whose
volume genuinely cannot go through the ordinary path, which is a
capacity argument to record rather than a habit.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:002`, lines 197-203, SHA-256 `7f87f7d0d7fff17fc3dcf138271b086ce182c0285dfd1fb15df2ce53215ce195`.
