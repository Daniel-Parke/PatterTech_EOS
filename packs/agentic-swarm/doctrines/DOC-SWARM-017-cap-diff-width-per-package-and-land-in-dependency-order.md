---
summary: Cap diff width per package and land in dependency order.
type: doctrine
tags: [eos]
id: DOC-SWARM-017
statement: Cap diff width per package and land in dependency order.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0457]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-SWARM-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

One
concern per landing. Agent changes are about 2.6 times larger, wait
roughly five times longer for pickup and land within thirty days at
32.7 per cent against 84.5 per cent for unassisted ones
(EV-0457). The ceiling goes on the package, not on the
reviewer, because detection collapses on wide diffs.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:007`, lines 268-273, SHA-256 `3f9cc4ec420fc01abcca689dc0f0f97b4509e6753a5f5a607caa329f5ccaa93b`.
