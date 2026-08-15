---
summary: Generated contract artefacts are produced deterministically from a committed source and CI fails when they drift.
type: doctrine
tags: [eos]
id: DOC-ARCH-002
statement: Generated contract artefacts are produced deterministically from a committed source and CI fails when they drift.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_cross_language_contract]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0023, EV-0024, EV-0025, EV-0057]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-ARCH-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Schemas, types and clients are generated offline and deterministically, committed, and a CI check fails when the committed copy lags its source. Evidence: OpenAPI (EV-0023), AsyncAPI (EV-0024), JSON Schema (EV-0025), dbt model contracts (EV-0057). Prevents: the silent failure, where a renamed field makes a mutation fail and the caller reports success.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:requirements:002`, lines 114-120, SHA-256 `45f9f11def36825910fa7dcd2a93338a9f13132cb72002934b4dee4f8b906c8c`.
