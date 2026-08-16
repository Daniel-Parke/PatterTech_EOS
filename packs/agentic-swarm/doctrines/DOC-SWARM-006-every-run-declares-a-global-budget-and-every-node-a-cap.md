---
summary: Every run declares a global budget and every node a cap, both enforced by the harness.
type: doctrine
tags: [eos]
id: DOC-SWARM-006
statement: Every run declares a global budget and every node a cap, both enforced by the harness.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0112]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-SWARM-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Tokens and money, with a no-progress
terminator, and delegation depth set explicitly rather than inherited
from a vendor default. Observability is not a control. Prevents an
unbounded bill, which is spend you cannot take back. Multi-agent runs
use roughly fifteen times chat tokens on the vendor's own reported
evaluation (EV-0112), so unbounded quality-seeking is unbounded spend.
That row sizes the exposure and does not test what a cap buys, which is
the leg on which `packs/agentic-development/PACK.md` demoted its own
bounded-loop rule. This one binds because an enforced ceiling is
arithmetic rather than a bet: a cap the harness holds cannot be
exceeded, and the spend it stops is not refundable.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:006`, lines 160-171, SHA-256 `140f931240ce6fc7266c90cd47ab530cca2717b3fbc12fe5be2e602862cb6e9d`.
