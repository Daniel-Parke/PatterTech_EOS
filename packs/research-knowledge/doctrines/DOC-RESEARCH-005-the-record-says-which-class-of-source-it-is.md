---
summary: The record says which class of source it is.
type: doctrine
tags: [eos]
id: DOC-RESEARCH-005
statement: The record says which class of source it is.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [records_external_claim]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0545]
review: 2029-08
lifecycle: active
verification_refs: [packs/research-knowledge/CHECKS.md]
migration_sources: [packs/research-knowledge/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-RESEARCH-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every source is
recorded as primary, secondary or tertiary by its distance from the
thing, and a claim resting only on a secondary reading says so
(EV-0545). For a venture, primary is the artefact and its maintainer's
own statement about it: the specification, the source, the release
notes, the licence file, the API response. Interpretation of a primary
source is a finding of ours and is recorded as ours, not attributed to
the source. The ladder for common source types is in
`packs/research-knowledge/refs/source-classes.md`. Predicate:
`records_external_claim`. Prevents: a chain of secondary readings
circulating as a fact, where every link cites the link before it and
none of them read the specification.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/research-knowledge/PACK.md:requirements:005`, lines 166-177, SHA-256 `bf883692faf7bd2e69238c79f24b3b1c3320948c0e5aae45f9a21514425a35c6`.
