---
summary: A postmortem due date is recorded at the moment of resolution.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-016
statement: A postmortem due date is recorded at the moment of resolution.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0200]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:014]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

for any customer-visible incident, no more than five days after
  resolution, with a named owner. The clock and the ownership come from
  the exemplar (EV-0200); the number five is the estate's, and it is a
  default rather than a finding.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:014`, lines 276-280, SHA-256 `58ef2aada4202bed1cbbbbe49b2493664cde46dc136138f7a19b69898fc5ae21`.
