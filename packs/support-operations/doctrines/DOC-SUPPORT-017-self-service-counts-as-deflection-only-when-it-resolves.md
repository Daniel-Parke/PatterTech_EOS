---
summary: Self-service counts as deflection only when it resolves.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-017
statement: Self-service counts as deflection only when it resolves.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0429]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:015]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Measure resolution and onward contacts, not page views, because a
  self-service layer that does not answer converts into an assisted
  contact with the customer's effort already spent
  (EV-0429).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:015`, lines 281-285, SHA-256 `437e007661174106b9b114279f9c857e287255f83ab678b041eb3de84f2290f2`.
