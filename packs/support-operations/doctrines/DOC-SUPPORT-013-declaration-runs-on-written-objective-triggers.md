---
summary: Declaration runs on written objective triggers.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-013
statement: Declaration runs on written objective triggers.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0423]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:011]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A second
  person is needed, the failure is visible to customers, or an hour of
  focused work has not closed it (EV-0423). Scope
  note: that hour is calibrated to a very large service estate and is
  not evidence for any threshold here; it is a starting number to argue
  with.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:011`, lines 252-257, SHA-256 `bd35ccc1238958d44306e3e8a48e19f8edb9d444838d1f6a64b42501bf9b644a`.
