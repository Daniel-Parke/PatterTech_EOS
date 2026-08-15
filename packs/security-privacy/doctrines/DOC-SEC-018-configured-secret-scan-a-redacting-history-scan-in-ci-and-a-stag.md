---
summary: Configured secret scan: a redacting history scan in CI and a staged scan pre-commit.
type: doctrine
tags: [eos]
id: DOC-SEC-018
statement: Configured secret scan: a redacting history scan in CI and a staged scan pre-commit.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0221, EV-0222]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SEC-018

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Two placements catch what one misses

EV-0221, EV-0222

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:defaults:008`, lines 181-181, SHA-256 `d891eff23cde6d825da93722e23ac9bd63e8988ea9aae656b2665245d08aedd9`.
