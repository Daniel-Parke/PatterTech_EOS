---
summary: Write acceptance criteria in EARS clause order once the problem is settled.
type: doctrine
tags: [eos]
id: DOC-DISC-017
statement: Write acceptance criteria in EARS clause order once the problem is settled.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0409]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:defaults:015]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-DISC-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

While a precondition, when a trigger, the named system shall
produce a response, one trigger at most and one system exactly
(`EV-0409`). Reason: a requirement that will not fit
the template is usually a wish, a design decision, or two requirements
stuck together. Scope note: EARS was derived on airworthiness
regulations where the trigger set is closed. It constrains form only.
See
`packs/product-discovery/wargames/WG-DISC-004-acceptance-criteria-form.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:defaults:015`, lines 254-262, SHA-256 `6a7d2cc6dda0a96fca6f15e688c2d4df7d6a1ee63773956045612df20a0b2205`.
