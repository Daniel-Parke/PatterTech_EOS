---
summary: A customer-visible incident records a communication owner separately from the person changing the system.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-005
statement: A customer-visible incident records a communication owner separately from the person changing the system.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_customer_visible_incident]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0422, EV-0423]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-SUPPORT-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_customer_visible_incident`. Both fields are filled even when the
two values are the same name, because the record has to show the
decision was taken (EV-0423,
EV-0422). Basis: decision. Prevents the fixer's
attention being spent on updates, and prevents an incident closing with
nobody accountable for having told anyone. Failed the basis leg.
Nothing else in this pack catches an incident that closed with nobody
accountable for telling anyone, so this is the default a venture should
think hardest before departing from.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:003`, lines 191-201, SHA-256 `7968ed41122a836c9da7f7b3b6a59c137e2a213d40a789cb4177ca4d6ef51f54`.
