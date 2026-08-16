---
summary: An error budget policy in the shape the SRE Workbook describes, paraphrased.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-009
statement: An error budget policy in the shape the SRE Workbook describes, paraphrased.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0096]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Budget remaining means ship with low ceremony; budget
  spent means changes halt except P0 and security until back inside the
  SLO (EV-0096). That source is CC BY-NC-ND, so this pack paraphrases it
  and never quotes it. *Reason to depart*: pre-production, or a venture
  where the operator is also the only user.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:defaults:002`, lines 235-240, SHA-256 `eb4fdefbcf07b467db8561c1627e67df06b9c4ea9ef9714dab7c2375c0c1d652`.
