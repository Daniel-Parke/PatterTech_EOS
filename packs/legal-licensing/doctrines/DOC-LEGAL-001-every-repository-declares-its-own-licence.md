---
summary: Every repository declares its own licence.
type: doctrine
tags: [eos]
id: DOC-LEGAL-001
statement: Every repository declares its own licence.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0337, EV-0348]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-LEGAL-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`publishes_code`. A
licence file at the root and a declared SPDX expression in the project
manifest, using an identifier from the list or an explicit `LicenseRef`
(EV-0337). Reason: silence means exclusive copyright, and the hosting
platform's terms grant no right to use or redistribute (EV-0348), so a
repository published without one is unusable by the people it was
published for. Depart only where nothing is published. Authority:
default, because the repair is a later commit adding the file. Basis:
standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:001`, lines 139-147, SHA-256 `91d21acbf6eb7a34965540b3d901274f15c757a8b713f2f2c94af59af95e3cef`.
