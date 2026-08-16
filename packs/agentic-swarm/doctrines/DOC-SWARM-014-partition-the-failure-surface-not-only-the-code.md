---
summary: Partition the failure surface, not only the code.
type: doctrine
tags: [eos]
id: DOC-SWARM-014
statement: Partition the failure surface, not only the code.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0053]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-SWARM-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where one
opaque verification step can fail for every lane at once, split it
before fanning out. Sixteen agents pointed at one monolithic build hit
identical bugs simultaneously and parallelism was worth nothing until
the failure was decomposed (EV-0053). A swarm pointed at one
undecomposable failure is a swarm of one. This is a default rather than
binding because the evidence is one case study, and the cost of getting
it wrong is a wasted run rather than a bad merge.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:004`, lines 249-256, SHA-256 `3bfba8ba387c4e3e6422cecbd8d521a6a48fb6f68a9bfe7a84bb44e395648b65`.
