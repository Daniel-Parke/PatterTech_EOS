---
summary: A failure that suggests a fix declares how confident it is.
type: doctrine
tags: [eos]
id: DOC-DOCS-010
statement: A failure that suggests a fix declares how confident it is.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0328]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-DOCS-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Four tiers work: safe to apply automatically, contains placeholders,
possibly wrong, unstated (EV-0328). Reason: a caller, human or agent,
needs to know whether to apply the suggestion without reading further.
Override where nothing can act on the suggestion automatically, in
which case the tier is decoration.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:004`, lines 230-235, SHA-256 `f7674640c27a54f4c85e7c2f0c54c3102be2a452393997cb9135f0ac4a0e5b72`.
