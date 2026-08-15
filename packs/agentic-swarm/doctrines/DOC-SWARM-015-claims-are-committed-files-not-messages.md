---
summary: Claims are committed files, not messages.
type: doctrine
tags: [eos]
id: DOC-SWARM-015
statement: Claims are committed files, not messages.
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
migration_sources: [packs/agentic-swarm/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-SWARM-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A lane claims its
scope by committing to `org/claims.json`; version control is the mutex
and the history is the audit trail (EV-0053).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:005`, lines 258-260, SHA-256 `2eb5707efdf8e2cd14485c3007e107dde734bafc311cf2cc447820430f7b4760`.
