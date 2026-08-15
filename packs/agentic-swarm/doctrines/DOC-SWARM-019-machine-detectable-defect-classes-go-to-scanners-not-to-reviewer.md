---
summary: Machine-detectable defect classes go to scanners, not to reviewers.
type: doctrine
tags: [eos]
id: DOC-SWARM-019
statement: Machine-detectable defect classes go to scanners, not to reviewers.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0488]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-SWARM-019

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Secrets, dependency existence, type and build errors,
licence violations. Of 74 validated genuine credentials in agent
changes, 81.1 per cent reached integration with no comment from seven
review tools or any human (EV-0488).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:009`, lines 286-290, SHA-256 `2fadf9b9be22de0a83242c808618277b672996568faf6c0eb598cfd40d80e1b0`.
