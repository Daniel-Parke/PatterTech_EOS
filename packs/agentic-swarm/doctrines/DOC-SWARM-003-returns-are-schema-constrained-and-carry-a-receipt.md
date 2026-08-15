---
summary: Returns are schema-constrained and carry a receipt.
type: doctrine
tags: [eos]
id: DOC-SWARM-003
statement: Returns are schema-constrained and carry a receipt.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0109, EV-0461]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-SWARM-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The receipt
names files changed, checks run with their verbatim results, what was
explicitly not done, unresolved unknowns, spend, and a terminal status
that distinguishes work outcome from infrastructure outcome. "Nothing to
do", "blocked, needs a decision", "failed the check" and "killed by an
error or a rate limit" are four different statuses and the integrator
handles them differently. Prevents an integrator reading a dead lane as
a clean negative result, which is how fabrication enters the trunk
wearing the integrator's authority. Task verification is one of the
three failure categories in the annotated multi-agent corpus (EV-0109),
and the runtime returns a bare absence for a killed node that a careless
aggregator filters out of existence (EV-0461).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:003`, lines 126-137, SHA-256 `4ab664de7ef51c56f218a8318aa61fb8ee5c488f83def9f1ae82ab731ddc0528`.
