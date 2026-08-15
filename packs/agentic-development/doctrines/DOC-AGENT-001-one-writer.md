---
summary: One writer.
type: doctrine
tags: [eos]
id: DOC-AGENT-001
statement: One writer.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0106, EV-0107, EV-0109]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-AGENT-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Several agents may read shared state. Writes to any
shared artefact are serialised through exactly one owner, or split into
disjoint files each with a single owner. Prevents the conflicting
decisions and silent overwrite failures that dominate multi-agent
traces (EV-0109, EV-0106, EV-0107). This is the constraint that lets
parallel reading and single-writer merging coexist. Binds on both legs:
a silent overwrite destroys work that nobody knows to look for, and
ADR-0008 kept the estate's own claim refusal binding for the same
reason, on its own conflict data.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:requirements:001`, lines 95-103, SHA-256 `ae8597c8cb166739d9400697de8793bf43fc2e3d1e592b95032da1aad203744b`.
