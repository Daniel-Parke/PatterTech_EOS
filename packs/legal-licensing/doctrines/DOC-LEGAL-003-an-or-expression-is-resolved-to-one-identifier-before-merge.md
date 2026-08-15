---
summary: An OR expression is resolved to one identifier before merge.
type: doctrine
tags: [eos]
id: DOC-LEGAL-003
statement: An OR expression is resolved to one identifier before merge.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0338]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-LEGAL-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`adds_dependency`. `MIT OR GPL-2.0-only` is a choice the project has to
make and record; the raw expression never survives into the inventory
verdict column (EV-0338). Reason: an unmade choice carried into a
shipped artefact leaves the obligations that apply undetermined, and
nobody can tell later which branch was relied on. Depart only where the
expression is still being negotiated, and say so in the entry.
Authority: default, because the choice can still be made after the
merge. Basis: standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:003`, lines 158-166, SHA-256 `5d1be6fd25123718eaf0d7ff96768312af2df8f171b8732d00532a34a324cdd6`.
