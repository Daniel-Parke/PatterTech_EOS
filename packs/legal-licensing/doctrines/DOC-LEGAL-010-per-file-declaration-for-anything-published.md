---
summary: Per-file declaration for anything published.
type: doctrine
tags: [eos]
id: DOC-LEGAL-010
statement: Per-file declaration for anything published.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0344]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-LEGAL-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Tags in file
headers, a sibling file where a comment cannot go, full texts in a
`LICENSES/` directory, bulk cases by glob, and a lint step in CI
(EV-0344). Reason: it is the only pattern here a cold
agent satisfies without judgement. Cost: real per-file overhead on a
small repository, which is why repository-level declaration is the
default for anything unpublished. A green lint proves declarations are
present and consistent, never that they are correct.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:003`, lines 261-268, SHA-256 `79e8e437090bd91930950b0c4283d8ca6fc319c607cdc4fbb83720262cb9e328`.
