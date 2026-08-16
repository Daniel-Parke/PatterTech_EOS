---
summary: The partition is written before any lane starts, and it is cut on the dependency graph.
type: doctrine
tags: [eos]
id: DOC-SWARM-001
statement: The partition is written before any lane starts, and it is cut on the dependency graph.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0450, EV-0455]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-SWARM-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

It names, per lane: the files owned, the
interfaces consumed, the interfaces published, and the lanes depended
on. Hub artefacts, meaning registries, schemas, routing tables, shared
type definitions and configuration, are integrator-owned and never
delegated. Prevents duplicated and gapped work, and merges into work a
lane did not know existed. Cohesion-based cutting with hub isolation
beat sequential work on pass rate at two thirds the cost, while cutting
one file per agent cost 44 to 60 per cent more than sequential for one
to three points (EV-0450). Agents left to infer relations between queued
changes recalled 35 to 58 per cent of them and committed unsafe merges
in 69.8 per cent of runs; the relations they did identify they then
respected 98 to 100 per cent of the time, and handing them the true
relations raised the delivery score by 22.3 to 50.2 points (EV-0455).
Compute the graph and hand it over.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:001`, lines 91-105, SHA-256 `39e47ddd7bf99170f6f51bbf6ef1144c2bc4e3258444bebfe4cb9ec17cf942b2`.
