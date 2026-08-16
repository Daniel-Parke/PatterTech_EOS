---
summary: Start at direct single-agent with a strong oracle.
type: doctrine
tags: [eos]
id: DOC-AGENT-008
statement: Start at direct single-agent with a strong oracle.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0052, EV-0088]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-AGENT-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0088,
EV-0052). Promote only on a named pressure. Reason: the promotion
always costs tokens, latency or coherence, and often all three.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:004`, lines 182-184, SHA-256 `663faf08ee24152ae661c73500cbe122cf406083a58ab37989ad8aa1507ee1d8`.
