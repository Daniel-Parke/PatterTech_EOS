---
summary: Three to five lanes.
type: doctrine
tags: [eos]
id: DOC-SWARM-011
statement: Three to five lanes.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0053, EV-0452, EV-0454]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-SWARM-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Wider only against a strong decidable
oracle, with the reason recorded. Reason: coordination cost grows
superlinearly with lane count and per-agent reasoning goes thin beyond
three or four agents under a fixed budget (EV-0452), while
pairwise conflict exposure grows with the square of the count
(EV-0454). Sixteen lanes worked once, on a compiler with
an oracle almost no business software has (EV-0053).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:001`, lines 231-237, SHA-256 `ebdcbcc2d655d03d4d4d7d321318727991612b2d316543be5f7f874df6f6b173`.
