---
summary: Cheap guardrails run beside the work and trip a wire, and cross-cutting policy sits at the runner rather than inside an agent.
type: doctrine
tags: [eos]
id: DOC-AGENT-013
statement: Cheap guardrails run beside the work and trip a wire, and cross-cutting policy sits at the runner rather than inside an agent.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0076, EV-0119, EV-0120]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-AGENT-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0076, EV-0120, EV-0119). Reason: a guardrail an agent can configure
away is not a guardrail.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:009`, lines 210-213, SHA-256 `c3a2da8fbed0fa741e0ec08d6e6fbccd5e5f9bbc46fb242737cabfe0416c2ff8`.
