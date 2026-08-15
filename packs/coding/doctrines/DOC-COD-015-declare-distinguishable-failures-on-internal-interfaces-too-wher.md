---
summary: Declare distinguishable failures on internal interfaces too, where more than one caller exists.
type: doctrine
tags: [eos]
id: DOC-COD-015
statement: Declare distinguishable failures on internal interfaces too, where more than one caller exists.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0003, EV-0004, EV-0006, EV-0007, EV-0008, EV-0010, EV-0069, EV-0070, EV-0089, EV-0094, EV-0105, EV-0164, EV-0165, EV-0166, EV-0167, EV-0168, EV-0169, EV-0170, EV-0171, EV-0172, EV-0173, EV-0174, EV-0175, EV-0176, EV-0177, EV-0178, EV-0179, EV-0180, EV-0181, EV-0182, EV-0183, EV-0191, EV-0192, EV-0480]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-COD-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: the coordination benefit
is real once there are two callers and absent when there is one, so this
is judgement rather than law. B4 is the binding version and applies to
published interfaces only. Override for a module with a single caller,
where the declaration is rigidity for its own sake.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:009`, lines 264-269, SHA-256 `3144702b0d4529d63808e732354cab10e84e48898e06e7dd2bae8b76c19c965a`.
