---
summary: Which policy engine, if any.
type: doctrine
tags: [eos]
id: DOC-IDENT-020
statement: Which policy engine, if any.
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [authenticates_people]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-IDENT-020

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A relationship engine is available as ordinary open-source software rather than as something to build (OpenFGA), which changes the cost but not the fork.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:preferences:001`, lines 192-194, SHA-256 `f0c3188ce99a9ba14c8cdd6f21301c61ab261f5aceaf2b50e3f1e91fbc449666`.
