---
summary: Reason about the worst case of a small sample, not its average.
type: doctrine
tags: [eos]
id: DOC-DISC-015
statement: Reason about the worst case of a small sample, not its average.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0407]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:013]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-DISC-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Across random sets of five participants the share of known problems
found ranged from 99 per cent down to 55; ten raised the floor to about
80 and twenty to about 95 (`EV-0407`). Reason: you
draw one sample and cannot tell which one you drew. Scope note: one 2003
web application, usability defect finding rather than demand.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:013`, lines 240-245, SHA-256 `6d05e4642cb6bcfa9d9a2d10cc40e99eaba1c3c19dc145bc5a740d589b33e8bb`.
