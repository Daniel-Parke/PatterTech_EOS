---
summary: Every signal names a threshold and a source that exists.
type: doctrine
tags: [eos]
id: DOC-DISC-005
statement: Every signal names a threshold and a source that exists.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0410]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-DISC-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`proposes_capability`. Each signal line carries the observation, the
number or state that would count as the signal firing, and the artefact
it will be read from. A source is a file, a table, a ticket export or a
named instrument that already exists. Prevents the readout that gets
invented after the fact (`EV-0410`). Basis: decision. Failed the basis
leg, same ladder as B1.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:003`, lines 160-166, SHA-256 `b327c17cdfa9b300ef80863a4e66c34a9a9437007f2343f6ed900f716697ee6d`.
