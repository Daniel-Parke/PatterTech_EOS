---
summary: Choose the narrowest temporal type that holds the fact.
type: doctrine
tags: [eos]
id: DOC-BLM-007
statement: Choose the narrowest temporal type that holds the fact.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0282]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-BLM-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A
birthday is a plain date, an opening time is a wall-clock time, a
deadline is a zoned date-time, a log line is an instant (EV-0282).
Reason: a wide type silently invents a zero, a zone or a UTC assumption
for a value that is genuinely unknown.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:005`, lines 161-165, SHA-256 `9f78b8e435894d65ad6f9eb5597271df35a8e54a5c20a00394adb0cf3e53599d`.
