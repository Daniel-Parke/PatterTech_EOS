---
summary: Contract-first with a definition language such as TypeSpec (EV-0145) when the boundary is public or has several consumers; code-first generation when it is internal, because a spec emitted from the handlers cannot drift from them.
type: doctrine
tags: [eos]
id: DOC-API-015
statement: Contract-first with a definition language such as TypeSpec (EV-0145) when the boundary is public or has several consumers; code-first generation when it is internal, because a spec emitted from the handlers cannot drift from them.
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0023, EV-0145]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

OpenAPI itself declines to prescribe either (EV-0023) and there is no controlled evidence on the question.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:preferences:001`, lines 191-195, SHA-256 `94a3328dc09eef5bd16e00b63a73bff4bfb46a154ca9e55f3ea3740b4bf1bda1`.
