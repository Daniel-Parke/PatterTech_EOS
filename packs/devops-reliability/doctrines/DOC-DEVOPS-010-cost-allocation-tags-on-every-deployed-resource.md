---
summary: Cost allocation tags on every deployed resource.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-010
statement: Cost allocation tags on every deployed resource.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0197]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Allocation is the
  precondition that makes optimisation and chargeback mean anything;
  without an owner per unit of spend the rest is theatre (EV-0197,
  CC BY 4.0, attribution to the FinOps Foundation). *Reason to depart*:
  a single-resource estate where allocation is trivially the whole bill.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:defaults:003`, lines 241-245, SHA-256 `07d65d6e07172947e423ea2cb5037d780030d8680ef9a949377c93aa42f69db9`.
