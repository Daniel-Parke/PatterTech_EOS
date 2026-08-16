---
summary: Runs are traceable.
type: doctrine
tags: [eos]
id: DOC-AGENT-007
statement: Runs are traceable.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0021, EV-0118]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-AGENT-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A stable span vocabulary (run, turn, agent,
generation, tool, guardrail, handoff), a workflow name, and a group id
linking related runs, with a switch that keeps spans while excluding
payloads where data policy forbids them (EV-0118, EV-0021). Prevents
failures that cannot be located, which is the whole cost of parallel
work. Failed the basis leg: the sources are vendor documentation for
their own tracing products. The payload-exclusion half is not loosened
by this, because personal data in a trace is a `packs/security-privacy/`
B5 matter and that binds on its own.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:003`, lines 170-178, SHA-256 `486d69e8fe5319eefe8d9c68213fb35ef6b8788d432f86284c148c8acfc9da54`.
