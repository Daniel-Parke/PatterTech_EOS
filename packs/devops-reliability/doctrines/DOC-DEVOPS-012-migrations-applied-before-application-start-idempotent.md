---
summary: Migrations applied before application start, idempotent, advisory-locked, failing closed.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-012
statement: Migrations applied before application start, idempotent, advisory-locked, failing closed.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0020, EV-0026, EV-0043, EV-0058, EV-0059, EV-0071, EV-0096, EV-0197, EV-0198, EV-0199, EV-0200, EV-0201, EV-0202, EV-0203, EV-0204, EV-0205, EV-0206, EV-0207, EV-0208, EV-0209, EV-0210, EV-0211]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A failed migration fails the
  deploy. Nobody edits an applied migration. This carries forward from
  the v1 devops doctrine and is unchanged by the new evidence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:defaults:005`, lines 252-255, SHA-256 `4e35473632de970178a2044b16bf2ccb1702ceec9e15cf484d589873e6eb2c2a`.
