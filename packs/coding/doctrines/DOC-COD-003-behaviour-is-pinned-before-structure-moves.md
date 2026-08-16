---
summary: Behaviour is pinned before structure moves.
type: doctrine
tags: [eos]
id: DOC-COD-003
statement: Behaviour is pinned before structure moves.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0177, EV-0180]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-COD-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No refactor of code
whose specification is missing or untrusted begins until a
characterisation or approval test captures current behaviour. Prevents
the silent behaviour change sold as a tidy-up, which is the failure
mode inherited and agent-written code both carry, because nobody can
say what the code was supposed to do (EV-0180, EV-0177). See
`packs/coding/wargames/WG-COD-004-pin-then-change.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:002`, lines 115-121, SHA-256 `3cf45b7677aa8b6f35af7921c06d8204a80633b6fdc8e39d4ed28cf50c88d488`.
