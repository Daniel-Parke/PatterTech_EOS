---
summary: Identify by surrogate or hashed key in the analytics layer.
type: doctrine
tags: [eos]
id: DOC-DATA-011
statement: Identify by surrogate or hashed key in the analytics layer.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0321]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-DATA-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The
join key is a surrogate or a salted hash rather than the natural
identifier, so B3 has a cheap default answer. Reason: collecting less is
the cheapest privacy control and the sources barely mention it.
Differentially private aggregates (EV-0321) are a later step, never a
substitute for collecting less.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:defaults:008`, lines 196-201, SHA-256 `91eb6ebb879f4579151d7f66180065491b63687b4276a2973bb9a1fe3fbfb2ac`.
