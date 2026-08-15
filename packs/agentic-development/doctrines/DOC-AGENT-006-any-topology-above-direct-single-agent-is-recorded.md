---
summary: Any topology above direct single-agent is recorded.
type: doctrine
tags: [eos]
id: DOC-AGENT-006
statement: Any topology above direct single-agent is recorded.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0109]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-AGENT-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The record
names the pressure that forced the promotion and the failure mode it
removes (EV-0109). It carries six level-two sections: Topology,
Pressures, Bounds, Resumability, Verification, Approval. Front-matter
carries `summary`, `type` and `tags` including `eos`, it cites at least
four evidence ids of which at least two come from this pack's own set,
and it stays under 120 lines. Prevents topology chosen by fashion, and
prevents a design no reviewer can check. The section-by-section
requirements are in
`packs/agentic-development/refs/DECISION_RECORD_SHAPE.md` and a worked
record is
`packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md`.
Failed the seriousness leg: an unrecorded topology is written down
later at the cost of one reading.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:002`, lines 155-168, SHA-256 `beea17d861a5f581df3bbc6dbcd143c1eb678409f40c6aee49462ba08151d472`.
