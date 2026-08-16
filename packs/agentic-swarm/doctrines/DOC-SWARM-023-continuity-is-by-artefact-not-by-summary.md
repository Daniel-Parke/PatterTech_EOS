---
summary: Continuity is by artefact, not by summary.
type: doctrine
tags: [eos]
id: DOC-SWARM-023
statement: Continuity is by artefact, not by summary.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0469]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:013]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D13]
---

# DOC-SWARM-023

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Cross-lane state
lives in files and orchestrator variables. Compaction is a fallback
inside a lane, never the mechanism between lanes: simple truncation
matched or beat summarisation at every budget tested, both sat below
full context, and compression turned reliably solved tasks into
intermittently solved ones (EV-0469).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:013`, lines 309-314, SHA-256 `c774de7c44663296ed8d45c09bef1996f43f1d1f07f28e93d2896e1806c37f17`.
