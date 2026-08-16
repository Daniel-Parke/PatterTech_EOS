---
summary: The error path is handled, never discarded.
type: doctrine
tags: [eos]
id: DOC-COD-004
statement: The error path is handled, never discarded.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0174]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-COD-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A bare catch-all, a
catch that swallows and continues, or a handler that logs and drops a
signalled failure is rejected. Every caught error is either handled,
translated into a declared failure, or re-raised. Prevents the failure
class that dominates production catastrophe: 92 per cent of the
catastrophic failures studied came from mishandling errors the software
had already signalled, and about a third were visible to plain
inspection (EV-0174). Scope note: that corpus was Java-heavy
distributed data systems in 2014, so the direction of attention
transfers and the exact proportion does not. See
`packs/coding/references/ERROR_PATH.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:003`, lines 123-133, SHA-256 `4fbbf7617adb4ea16a96b59ab454495c80eef6d46e601588a024b16365369e3e`.
