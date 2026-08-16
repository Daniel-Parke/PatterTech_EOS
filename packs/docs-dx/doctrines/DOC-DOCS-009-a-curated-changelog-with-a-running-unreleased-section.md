---
summary: A curated changelog with a running Unreleased section.
type: doctrine
tags: [eos]
id: DOC-DOCS-009
statement: A curated changelog with a running Unreleased section.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0136, EV-0170, EV-0171, EV-0333]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-DOCS-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

One
entry per version, newest first, dated, grouped into added, changed,
deprecated, removed, fixed and security, with deprecations announced
before removal (EV-0333). Derive from commit history only where a
commit grammar is enforced at write time (EV-0170, EV-0171). Reason: a
consumer needs the consequence of upgrading, and a raw log is full of
merges and internal churn nobody can act on. Override for an internal
service whose only consumers are two other services of the same estate,
where a machine-readable compatibility diff (EV-0136) carries more than
prose. See `packs/docs-dx/wargames/WG-DOCS-003-changelog-ownership.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:003`, lines 219-228, SHA-256 `adcbda99377d9490a042d1fe4896677f49cf4fe625eeee46b4ffe1111194bb3d`.
