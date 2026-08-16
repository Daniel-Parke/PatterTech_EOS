---
summary: Guardrails and classifiers run in parallel as a tripwire above the enforcement boundary, never as the boundary.
type: doctrine
tags: [eos]
id: DOC-SEC-015
statement: Guardrails and classifiers run in parallel as a tripwire above the enforcement boundary, never as the boundary.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0076, EV-0081, EV-0215]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SEC-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Adaptive attacks broke all eight in-band defences tested, over half the time

EV-0215, EV-0076, EV-0081

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:defaults:005`, lines 178-178, SHA-256 `2f7430313b7ffd91e1c38131f8bc2e9b4232f7b282ab8cfb864223356b8eebfe`.
