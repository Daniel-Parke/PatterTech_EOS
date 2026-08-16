---
summary: Tool capability order: explicit tools, then bash, then generated code, then MCP.
type: doctrine
tags: [eos]
id: DOC-AGENT-011
statement: Tool capability order: explicit tools, then bash, then generated code, then MCP.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0113, EV-0115]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D4]
---

# DOC-AGENT-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0115). Tools are consolidated around whole
workflows and namespaced, returning meaning rather than identifiers
(EV-0113). Reason: each step down the order costs context and
indirection.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:007`, lines 200-204, SHA-256 `3505c3b6825fcc6851637fb3cfcf814f1711ac83eaae4a5f4f782c6268f9b727`.
