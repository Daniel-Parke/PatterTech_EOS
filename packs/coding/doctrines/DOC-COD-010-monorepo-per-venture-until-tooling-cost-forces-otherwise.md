---
summary: Monorepo per venture until tooling cost forces otherwise.
type: doctrine
tags: [eos]
id: DOC-COD-010
statement: Monorepo per venture until tooling cost forces otherwise.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0172, EV-0173]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-COD-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A
small repository gets the monorepo benefits free, because it is small
(EV-0172, EV-0173). Reason: the benefits at scale are bought with
bespoke tooling nobody at venture scale can fund, and the pain sits in
the middle sizes. Override when a component has its own release train
or its own consumers. See
`packs/coding/wargames/WG-COD-005-repo-shape.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:004`, lines 225-231, SHA-256 `0a68ff5234aa4984d00d939a3e7ee94ae5077147124b5cb05db747facb010e1a`.
