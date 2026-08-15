---
summary: Irreversible or externally visible acts pass a human checkpoint.
type: doctrine
tags: [eos]
id: DOC-AGENT-002
statement: Irreversible or externally visible acts pass a human checkpoint.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0079, EV-0108]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-AGENT-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The gate sits at the risky act, not at a tidy phase
boundary (EV-0079, EV-0108). Prevents an agent publishing, deploying,
deleting or spending on its own. The checkpoint is a recorded approval
event, never a claim in prose. Binds as a protected-set floor: approval
for consequential external actions is named in `GOVERNANCE.md`, carried
by `packs/security-privacy/` B6, and enforced at the act by
`kernel/GUARD_SPEC.md`. No audit touches it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:requirements:002`, lines 105-112, SHA-256 `f5e91b56d4981cfc367095ceeb9469731661e220f5a7f7cfe5083746105a5947`.
