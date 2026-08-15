---
summary: Checkpoint state is a trust boundary.
type: doctrine
tags: [eos]
id: DOC-AGENT-004
statement: Checkpoint state is a trust boundary.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0121]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-AGENT-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Never resume from a
checkpoint of unknown provenance, and treat the store as attack surface
(EV-0121). Prevents code execution through a deserialised run state.
Binds as a protected-set floor: a checkpoint of unknown provenance is
untrusted content deciding what the agent does next, which
`packs/security-privacy/` B1 and B2 already hold.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:requirements:004`, lines 127-132, SHA-256 `f2e48682f89230e09350a7c86d40205cf6646cea69a12dae98dbe4e99bbd16e7`.
