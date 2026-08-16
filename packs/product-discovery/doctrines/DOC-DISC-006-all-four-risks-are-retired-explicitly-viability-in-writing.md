---
summary: All four risks are retired explicitly, viability in writing.
type: doctrine
tags: [eos]
id: DOC-DISC-006
statement: All four risks are retired explicitly, viability in writing.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0416]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-DISC-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`proposes_capability`. Value, usability, feasibility and viability each
get a written answer, and none may be left blank
(`EV-0416`). Prevents the solo failure the source
itself predicts: with one operator holding all four, the two that are
interesting get tested and the other two get assumed, and viability is
the one that goes. Basis: decision. Failed the basis leg, and the audit
returned it to the grade the research gave it in the first place.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:004`, lines 168-175, SHA-256 `7325787fb4a37edbd31a6c3e3e01b0d3554869f3ddac2a910bb58fb47dd61e73`.
