---
summary: Irreversible external effects are staged, and executed once by the integrator after merge.
type: doctrine
tags: [eos]
id: DOC-SWARM-021
statement: Irreversible external effects are staged, and executed once by the integrator after merge.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0478]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D11]
---

# DOC-SWARM-021

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A losing speculative branch still
externalises its effects unless they are fenced; a commit gate gave
about seven times the task success of immediate-effect baselines under
fault injection and leaked nothing where the comparators leaked over a
thousand messages (EV-0478).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:011`, lines 297-302, SHA-256 `d5746d4b3448a88db58a165411d77b810f52239c35c56450c39087aa72fc99e7`.
