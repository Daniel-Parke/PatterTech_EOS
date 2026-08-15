---
summary: Every loop is bounded.
type: doctrine
tags: [eos]
id: DOC-AGENT-005
statement: Every loop is bounded.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0051, EV-0052]
review: on-change-of:agent-sdk-major-release
lifecycle: active
verification_refs: [packs/agentic-development/CHECKS.md]
migration_sources: [packs/agentic-development/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-AGENT-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A loop carries numeric limits on turns,
tokens or wall-clock, at least two of the three, with units, plus a
stated stop condition and what happens when it trips (EV-0051,
EV-0052). Prevents unbounded spend and the stall that looks like
progress. Failed the basis leg: both sources are repositories that
happen to implement bounds, and nothing measures what bounding buys.
The failure is still real and still expensive, and money spent is not
refunded, so a run that departs from this default says what ceiling it
is accepting instead.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-development/PACK.md:defaults:001`, lines 145-153, SHA-256 `9e3aa2e7005c81a4eaaab25dbc33ed18f4c9a2f5cb0b76f1bb3b6e7f34bd9ec0`.
