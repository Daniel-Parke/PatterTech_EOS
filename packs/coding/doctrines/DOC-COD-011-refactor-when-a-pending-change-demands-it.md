---
summary: Refactor when a pending change demands it.
type: doctrine
tags: [eos]
id: DOC-COD-011
statement: Refactor when a pending change demands it.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0177]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-COD-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Refactoring is
change-driven, not smell-driven: developers refactor to make a specific
pending change possible, and a smell-detector backlog is a poor model
of the work (EV-0177). Reason: backlog-driven tidying spends the budget
where no change is coming. Override for a documented decay signal you
have measured in your own repository.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:005`, lines 233-238, SHA-256 `f0907c36d3fc1945f47f3ae5665115cbbaa95e1074cf9521040acc6e1adaceaa`.
