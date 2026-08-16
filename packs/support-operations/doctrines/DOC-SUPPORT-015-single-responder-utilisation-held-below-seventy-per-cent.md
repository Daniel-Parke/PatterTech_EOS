---
summary: Single-responder utilisation held below seventy per cent.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-015
statement: Single-responder utilisation held below seventy per cent.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0430]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:013]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Waiting time in a single-server queue rises as utilisation over one
  minus utilisation, so the wait is roughly two and a third service
  times at seventy per cent, five and two thirds at eighty-five, and
  nineteen at ninety-five (EV-0430). The levers that
  work are reducing arrival variability and holding deliberate slack.
  Scope note: that is a heavy-traffic approximation for one server,
  first come first served, with no priority classes and nobody giving
  up, so a severity-prioritised desk differs in detail while keeping
  the same shape of collapse.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:013`, lines 266-275, SHA-256 `fab96fc790aff8b8fd3cb7d231262c6360c4bff8c58d1f0e009f68b80aa7a7a5`.
