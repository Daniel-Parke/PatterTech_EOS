---
summary: Internal links and anchors resolve, checked in CI, and the check blocks.
type: doctrine
tags: [eos]
id: DOC-DOCS-001
statement: Internal links and anchors resolve, checked in CI, and the check blocks.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0331, EV-0332]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-DOCS-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The check runs offline over the repository, validates
fragments and not just paths, and distinguishes a broken link from a
broken checker so a tool failure is never read as a clean run
(EV-0331). Reason: an internal cross-reference to `#install-it` keeps
pointing at nothing the moment someone retitles the heading, and nobody
notices until a reader does. Depart where the repository has no
cross-references worth the CI minute, and say so. Authority: default.
Basis: standard, plus the exemplar at EV-0332 where the same check
gates merges across sibling repositories. See
`packs/docs-dx/refs/DOC_GATE.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:001`, lines 122-132, SHA-256 `76a7669d0290adc1068357458f71b5a1e0fd27c8792f98a1ea7a4e109ff22b2c`.
