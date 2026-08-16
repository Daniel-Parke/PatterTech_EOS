---
summary: Progressive rollout with an automated abort condition for user-facing change.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-008
statement: Progressive rollout with an automated abort condition for user-facing change.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0204]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Promotion is a machine decision against a
  declared query with a failure limit, and breaching it shifts traffic
  back to the last stable version without a human in the loop (EV-0204).
  *Reason to depart*: no traffic router or metrics backend exists yet,
  in which case say so and use a flag with a manual kill.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:defaults:001`, lines 229-234, SHA-256 `2910a2d0b637f92584a5ec7507333e16c060eaa084b7d5a0cf09159a601ad8fb`.
