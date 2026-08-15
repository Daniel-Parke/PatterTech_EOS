---
summary: Evaluation suites start at twenty to fifty tasks harvested from real failures, scored with pass@k and pass^k.
type: doctrine
tags: [eos]
id: DOC-AGENT-015
statement: Evaluation suites start at twenty to fifty tasks harvested from real failures, scored with pass@k and pass^k.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0087]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-AGENT-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0087). Reason:
agents are non-deterministic, so a single pass proves little.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:011`, lines 218-220, SHA-256 `dad5b4b67950f0c203b9b58b0e36b4ad981d57b944cec4dca1b109c1fb453d59`.
