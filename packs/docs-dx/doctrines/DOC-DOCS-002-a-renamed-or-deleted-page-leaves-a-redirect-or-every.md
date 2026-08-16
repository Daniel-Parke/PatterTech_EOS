---
summary: A renamed or deleted page leaves a redirect, or every reference to it is updated in the same change.
type: doctrine
tags: [eos]
id: DOC-DOCS-002
statement: A renamed or deleted page leaves a redirect, or every reference to it is updated in the same change.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0332]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-DOCS-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

One or the other, verified, in
the commit that does the moving (EV-0332). Reason: the half-move, where
the page is renamed, the inbound links are found later, and the reader
in between gets a dead end with no clue what replaced it. Authority:
default. Basis: decision, taken on that exemplar.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:002`, lines 134-139, SHA-256 `d38f2e141839f37a31dd28a22f82c00b756d56c5f39687382de060e7839efabb`.
