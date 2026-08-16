---
summary: Policy checks expressed as code where the inputs are already machine-readable.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-013
statement: Policy checks expressed as code where the inputs are already machine-readable.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0071]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A decision engine queried with structured input
  beats a prose checklist, but only where structured input exists
  (EV-0071).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:defaults:006`, lines 256-259, SHA-256 `b19bc70d34e7e67e929d430dfdeabe404a5bf21b2ab2983609154a13fe7c8067`.
