---
summary: The session that reads the source and the lanes that build are different, and the build lanes get the lesson, never the source.
type: doctrine
tags: [eos]
id: DOC-LEGAL-017
statement: The session that reads the source and the lanes that build are different, and the build lanes get the lesson, never the source.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [studies_external_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0344, EV-0352]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D10]
---

# DOC-LEGAL-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`studies_external_source`. Reason: similarity plus access is what an
infringement argument is made of, so the cheapest defence is that the
people who wrote the replacement never saw the original. A machine
reimplementation is not presumed clean either, because the model may
have been trained on the source and authorship of machine output is
unsettled (EV-0352). Where real code is carried rather than a lesson,
it is declared per file at the moment it lands (EV-0344) and it stops
being a study and becomes a vendored dependency under D5 and B2.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:010`, lines 308-317, SHA-256 `5e826eb0b12ad1d9c1f85c04f05e69f119f38673117a82c2da7ac80850af2c59`.
