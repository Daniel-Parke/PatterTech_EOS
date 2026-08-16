---
summary: Diff-aware static analysis split into blocking and monitor, autofix only for mechanical findings.
type: doctrine
tags: [eos]
id: DOC-SEC-013
statement: Diff-aware static analysis split into blocking and monitor, autofix only for mechanical findings.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0070]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SEC-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Blocking everything trains people to bypass the gate

EV-0070

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:defaults:003`, lines 176-176, SHA-256 `f3b3f3f6c740fe01488c2130356824a9379e59156f25efafa6eb5507a3ad71d5`.
