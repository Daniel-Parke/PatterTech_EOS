---
summary: If the graph will not cut, do not swarm.
type: doctrine
tags: [eos]
id: DOC-SWARM-013
statement: If the graph will not cut, do not swarm.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0452]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-SWARM-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A chain where step N
needs step N minus one, or a cohesion pass that returns one group, runs
sequentially in one lane. Decomposability rather than difficulty
decides whether added agents help: one domain lost 70.0 per cent where
another gained 80.9 at an almost identical score (EV-0452).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:003`, lines 243-247, SHA-256 `91323388dd306bd0e15cb2b071a8c633ee21d8b86141b8aceba68039223fbf1a`.
