---
summary: The severity ladder is written before the incident, and one band changes what the organisation does.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-004
statement: The severity ladder is written before the incident, and one band changes what the organisation does.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_customer_visible_incident]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0421]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-SUPPORT-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_customer_visible_incident`.
The ladder is ordered, each band has a written impact criterion, it
states that the higher band is taken when the call is unclear, and at
least one threshold switches the response mode rather than only the
wording (EV-0421). The band is not litigated during
the incident; the argument goes in the postmortem. Basis: decision,
taken on exemplar practice with no outcome data behind it. Prevents
severity being assigned afterwards to justify the response that already
happened. Failed the basis leg, which the pack already said out loud.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:002`, lines 180-189, SHA-256 `149ef1aa6175019c49f5ed446b44ce5243db4a4f91836ae57bc985c7dd1482cc`.
