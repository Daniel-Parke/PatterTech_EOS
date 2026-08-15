---
summary: Which secret scanner.
type: doctrine
tags: [eos]
id: DOC-SEC-020
statement: Which secret scanner.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0221]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SEC-020

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Gitleaks is declared feature complete by its maintainer with security patches only and a named successor, Betterleaks, so the choice has a shelf life (EV-0221).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:preferences:001`, lines 188-190, SHA-256 `17be1420c871b743d180c56025213f38b291a6b489df46628556344e637a15ec`.
