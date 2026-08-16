---
summary: The partition value is derived by the engine from a real column, or in exactly one place in code, and never written by hand at the call site.
type: doctrine
tags: [eos]
id: DOC-DATAENG-007
statement: The partition value is derived by the engine from a real column, or in exactly one place in code, and never written by hand at the call site.
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
migration_sources: [packs/data-engineering/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-DATAENG-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where the format supports a declared transform of the event-time
column, use it and let the engine apply it. Where it does not, one
function owns the derivation. *Reason to depart*: a table small enough
that it is not partitioned at all, which is most tables in a young
venture.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:004`, lines 213-219, SHA-256 `3bd9c1d367ec600ce15b1c4378f343bb6bd763b999e35b2c5d6c3d1f1d5c2229`.
