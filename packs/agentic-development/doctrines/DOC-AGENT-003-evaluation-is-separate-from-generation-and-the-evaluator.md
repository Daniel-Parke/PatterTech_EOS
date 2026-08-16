---
summary: Evaluation is separate from generation, and the evaluator holds external truth.
type: doctrine
tags: [eos]
id: DOC-AGENT-003
statement: Evaluation is separate from generation, and the evaluator holds external truth.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0007, EV-0089, EV-0111, EV-0115]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-AGENT-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Tests, types, schema validators, linters, a fresh
context or a person. Without external truth, self-review degrades the
answer (EV-0111), and an agent asked to grade itself will praise itself
(EV-0089, EV-0115). Prevents verification theatre. Where no external
oracle exists, say so and do not claim an evaluator-optimizer loop.
Binds on measurement: tests generated after faulty code caught 14 per
cent of faults against 25 per cent for tests generated independently,
because the tests inherit the implementation's wrong assumptions
(EV-0007), and the self-correction result is controlled and
peer-reviewed (EV-0111). ADR-0006 decision 5 makes independence the
binding remainder across the estate, and this is its statement here.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:requirements:003`, lines 114-125, SHA-256 `0e9e89a206cca7ecc5b572042273ce64d2b9d9fe94503519aa64862008152ee8`.
