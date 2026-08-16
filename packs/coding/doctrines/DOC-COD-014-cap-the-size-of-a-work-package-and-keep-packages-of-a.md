---
summary: Cap the size of a work package, and keep packages of a similar size.
type: doctrine
tags: [eos]
id: DOC-COD-014
statement: Cap the size of a work package, and keep packages of a similar size.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0178]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-COD-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The venture picks the cap and records it. Reason: small, even
increments are the ingredient the sequencing literature actually
measured (EV-0178), and dropping the test-first cycle drops the thing
that enforced them. Nothing in a queue or a dependency graph supplies
this automatically.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:008`, lines 257-262, SHA-256 `0bcae5a9f2b42dd82096bdef23e617a814dd87a1418bccc01bb48e4e97c19533`.
