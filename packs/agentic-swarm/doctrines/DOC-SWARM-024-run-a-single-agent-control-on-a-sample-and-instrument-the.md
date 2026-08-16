---
summary: Run a single-agent control on a sample, and instrument the landing.
type: doctrine
tags: [eos]
id: DOC-SWARM-024
statement: Run a single-agent control on a sample, and instrument the landing.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0010, EV-0494]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:014]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D14]
---

# DOC-SWARM-024

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Compare accuracy and cost per merged change; if the swarm
does not beat the control, collapse it. Track median agent-done-to-
merged time and the share of lane-authored code rewritten within
fourteen days (EV-0494). Developers measured 19 per cent
slower while believing they were 20 per cent faster, so felt speed is
not a signal (EV-0010).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:014`, lines 316-322, SHA-256 `f1f02cab2ba5ba74418083b4b7d739612a1390657055307ec84878c27862a3d1`.
