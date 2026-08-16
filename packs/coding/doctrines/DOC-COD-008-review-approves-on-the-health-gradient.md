---
summary: Review approves on the health gradient.
type: doctrine
tags: [eos]
id: DOC-COD-008
statement: Review approves on the health gradient.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0164, EV-0165]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-COD-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Approve once the change
definitely improves overall code health even when it is imperfect, and
refuse only what definitely worsens it. One reviewer, one iteration,
small changes (EV-0164, EV-0165). Reason: the practice that makes
review affordable is keeping changes small, and the alternative bar of
perfection stalls the queue. Scope note: EV-0165 describes one company
with bespoke tooling and predates machine authorship.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:002`, lines 208-214, SHA-256 `086821482af8362eab4b7e6d58c8f5f97d16c1ebb16a0a3f2dc4f6801194b139`.
