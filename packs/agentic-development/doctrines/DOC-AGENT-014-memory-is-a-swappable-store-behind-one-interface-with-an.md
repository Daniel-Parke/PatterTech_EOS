---
summary: Memory is a swappable store behind one interface with an explicit trimming policy.
type: doctrine
tags: [eos]
id: DOC-AGENT-014
statement: Memory is a swappable store behind one interface with an explicit trimming policy.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0117]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-AGENT-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0117). Reason: recall is not relevance.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:010`, lines 215-216, SHA-256 `bb620738dc77652911f41702b9da483dc1d2401499c28df0a099abf4b5f7a880`.
