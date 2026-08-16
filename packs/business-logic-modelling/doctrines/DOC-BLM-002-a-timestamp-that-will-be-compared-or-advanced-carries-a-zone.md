---
summary: A timestamp that will be compared or advanced carries a zone identifier, not just an offset.
type: doctrine
tags: [eos]
id: DOC-BLM-002
statement: A timestamp that will be compared or advanced carries a zone identifier, not just an offset.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [models_time]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0281]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-BLM-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`models_time`. An offset is a single
number; a zone identifier such as Europe/London is a function from
instants to offsets, and only the second answers what one day later
means across a daylight-saving change (EV-0281). A naive timestamp with
no zone is refused outright. Prevents the bug that appears twice a year
and always in production: a hold that expires an hour early, a renewal
that bills twice, a report whose day boundary moves. Basis: standard.
See `packs/business-logic-modelling/references/TIME_TYPES.md`.

Nothing here lowers a tier floor in `kernel/POLICY_SPEC.md` or converts
a guarded action under `kernel/GUARD_SPEC.md`. Money movement is a
guarded action whatever this pack says about modelling it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:requirements:002`, lines 111-123, SHA-256 `c76a20a1802e0740bc2b0a9359524522aad9fe2c78ac10c220067ca90a145b7a`.
