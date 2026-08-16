---
summary: One priority band reserved for plausible but unevidenced.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-012
statement: One priority band reserved for plausible but unevidenced.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0424]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Keeps opinion out of the roadmap without throwing it away
  (EV-0424).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:010`, lines 249-251, SHA-256 `e891f3c631a3a7e3007a7006821fd06a55e937f8565e1201f72ea71c29d31f74`.
