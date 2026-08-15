---
summary: C4 container and component views authored in Structurizr DSL.
type: doctrine
tags: [eos]
id: DOC-ARCH-007
statement: C4 container and component views authored in Structurizr DSL.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0101, EV-0102, EV-0149, EV-0158]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-ARCH-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: one text model generates many views that cannot drift from each
other (EV-0101, EV-0102). Borrow arc42 headings (EV-0149) only for the
non-diagram content actually needed, and reach for ISO 42010 vocabulary
(EV-0158) only when a stakeholder demands that rigour.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:004`, lines 163-167, SHA-256 `165e5d606c662faf8950bca14c4760673977ac7604cf1b60a156b5c6272aadd0`.
