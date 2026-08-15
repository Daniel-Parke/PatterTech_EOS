---
summary: Backwards-incompatible schema change ships as expand, migrate, contract, in separate deploys.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-001
statement: Backwards-incompatible schema change ships as expand, migrate, contract, in separate deploys.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0206, EV-0207]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Add the new shape, move every caller
   and row, delete the old shape only once nothing reads it. No deploy
   may break the application version still running beside it (EV-0206,
   EV-0207). *Prevents*: an application rollback that needs a database
   change to go with it, at the exact moment nobody can think straight.
   *Basis*: decision, on one practitioner write-up and one maintainer
   document. It binds as a production-safety floor rather than on that.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:001`, lines 140-147, SHA-256 `2c34f11ca80df94ade7c3b98656ced93f8e1e227a94202b27e18fdad3c0b5bce`.
