---
summary: Experiment flags governed by asymmetric gating, where goal metrics drive the ship decision and guardrails block only on significant harm (EV-0059).
type: doctrine
tags: [eos]
id: DOC-DEVOPS-018
statement: Experiment flags governed by asymmetric gating, where goal metrics drive the ship decision and guardrails block only on significant harm (EV-0059).
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0059]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:preferences:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-018

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No separate rationale was recorded.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:preferences:005`, lines 273-275, SHA-256 `a39080cf46c7e70ba04029b5678a8500fc344bee413cf07de56e916026814709`.
