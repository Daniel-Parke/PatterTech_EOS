---
summary: One lane, one worktree, one branch, one owned file set, and the integrator owns merge order.
type: doctrine
tags: [eos]
id: DOC-SWARM-009
statement: One lane, one worktree, one branch, one owned file set, and the integrator owns merge order.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0108, EV-0452, EV-0460]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B9]
---

# DOC-SWARM-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Isolation is enforced by the harness or
the version control system, never by instruction. Merge sequence is a
decision the integrator records, not an emergent property of who
finished first. Prevents silent overwrite between lanes and unsafe
merges from hidden inter-change relations. Two writers on one file
overwrite each other, which the harness documents plainly and enforces
where it can (EV-0108, EV-0460). Error amplification
against a single agent was 17.2 times for independent lanes and 4.4
times with a validating orchestrator (EV-0452).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:009`, lines 208-217, SHA-256 `b45a90750f5272a41f52660620a941ff3411b001c40a2b171501eb3106300e12`.
