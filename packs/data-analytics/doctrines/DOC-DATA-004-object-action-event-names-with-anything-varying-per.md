---
summary: Object-action event names, with anything varying per occurrence in a property.
type: doctrine
tags: [eos]
id: DOC-DATA-004
statement: Object-action event names, with anything varying per occurrence in a property.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0319]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-DATA-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Names are generated from the product's objects and the
actions available on them rather than enumerated one at a time, and no
identifier, number or variant goes in the name (EV-0319). Reason: a
generated taxonomy stays finite, an enumerated one grows to thousands of
near-duplicates. The evidence is vendor assertion, and the casing is
taste.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:001`, lines 147-153, SHA-256 `5a8306bbce4f26ad34ed217f318f9a399c47eb11ed03fcce4b78100a5b5f334c`.
