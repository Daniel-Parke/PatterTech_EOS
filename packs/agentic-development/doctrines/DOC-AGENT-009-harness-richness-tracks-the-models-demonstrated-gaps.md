---
summary: Harness richness tracks the model's demonstrated gaps.
type: doctrine
tags: [eos]
id: DOC-AGENT-009
statement: Harness richness tracks the model's demonstrated gaps.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0052, EV-0089, EV-0110]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-AGENT-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Add a
component only by naming the model limitation it compensates for, and
strip components as models improve (EV-0089, EV-0110, EV-0052). Reason:
every component encodes an assumption about what the model cannot do,
and those assumptions expire. This default is the one most likely to
move; the ratio of harness to model can shift without any binding
requirement changing.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:005`, lines 186-192, SHA-256 `ce9e0a8497d32bade7c99f08b75c56df67d8b1e8a203adeeae9a9fa226974bd2`.
