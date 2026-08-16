---
summary: Tokens are defined once and generated; derived files are never hand-edited.
type: doctrine
tags: [eos]
id: DOC-UIUX-006
statement: Tokens are defined once and generated; derived files are never hand-edited.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0030, EV-0064, EV-0065]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-UIUX-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_design_tokens`. One source in the DTCG shape, with
per-platform outputs produced by a build (EV-0030, EV-0065, EV-0064).
C1, C2, C3 and C15 settle it, C3 being the one that catches the
hand-edit: regeneration must leave a clean tree.
Prevents platforms drifting apart and prevents a value edited in one
output being silently overwritten. Basis: standard. Binds because
ADR-0008 keeps the derived-file rule by name: a file with a generator is
never hand-edited, and that failure has happened in this repository
twice.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:005`, lines 149-158, SHA-256 `39a4740b806c02f7d66cc667216cb889477046590f216e44e28687c1e22aacc9`.
