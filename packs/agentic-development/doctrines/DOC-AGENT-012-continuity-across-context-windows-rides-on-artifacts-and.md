---
summary: Continuity across context windows rides on artifacts and git history, not on compaction alone.
type: doctrine
tags: [eos]
id: DOC-AGENT-012
statement: Continuity across context windows rides on artifacts and git history, not on compaction alone.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0085, EV-0117]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-AGENT-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0085, EV-0117). Reason: a
compacted summary loses exactly the detail a resumed run needs.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:008`, lines 206-208, SHA-256 `7d67e21fce4bcef509d1eb74bc558a570ad5c40d707b8d48ece0337b01d46b4b`.
