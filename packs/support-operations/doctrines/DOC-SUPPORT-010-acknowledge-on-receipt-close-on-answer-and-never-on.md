---
summary: Acknowledge on receipt, close on answer, and never on silence, for anyone who pays.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-010
statement: Acknowledge on receipt, close on answer, and never on silence, for anyone who pays.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0425]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The route to complain is visible and free to
  use, and the loop closes when the complainant has been told the
  outcome (EV-0425).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:008`, lines 239-242, SHA-256 `983e15ba3e38487d8c530b4715ac7b3af0b7818592e5e8620cbbb5f54f5033de`.
