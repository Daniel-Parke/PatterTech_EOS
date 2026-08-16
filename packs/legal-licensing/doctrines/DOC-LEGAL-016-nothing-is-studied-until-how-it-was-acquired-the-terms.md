---
summary: Nothing is studied until how it was acquired, the terms attached to it and the governing law are written down.
type: doctrine
tags: [eos]
id: DOC-LEGAL-016
statement: Nothing is studied until how it was acquired, the terms attached to it and the governing law are written down.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [studies_external_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0337, EV-0348]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-LEGAL-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`studies_external_source`.
One row per source, before it is read: what the artefact is and at
which version, how we got it, the licence or terms of service that came
with it, and which country's law those terms are read under. Reason:
how the source was acquired is what decides whether the study was
lawful, and a public repository being forkable grants no right to use
what is in it (EV-0348). Record the identifier where the source carries
one (EV-0337). See
`packs/legal-licensing/wargames/WG-LEGAL-005-lawful-extraction.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:009`, lines 297-306, SHA-256 `664effed8a83307983c9c51f072f8519c8cfda551d93ea683605f833bcfec777`.
