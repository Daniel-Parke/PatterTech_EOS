---
summary: Do not swarm work a single agent already does well.
type: doctrine
tags: [eos]
id: DOC-SWARM-012
statement: Do not swarm work a single agent already does well.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0452]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-SWARM-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Above
roughly 45 per cent single-agent success on the task's own acceptance
measure, adding lanes predicts a loss (EV-0452).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:002`, lines 239-241, SHA-256 `9169cb95d05dbe553a3ca465069f167bb50d049000f53e6812bb109ce322734c`.
