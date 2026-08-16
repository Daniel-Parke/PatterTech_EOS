---
summary: Auto-close and stale timers on public trackers only.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-011
statement: Auto-close and stale timers on public trackers only.
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
migration_sources: [packs/support-operations/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Unreproducible reports close on a timer where the reporter is a
  volunteer and closing costs nothing contractual
  (EV-0424). Recorded counter-evidence: maintainers
  of the project that runs that bot have filed complaints that it
  closes real bugs.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:009`, lines 243-248, SHA-256 `07b3564f3907a2b4b8a206d6bf9a50910480f96982b4568fef6fd4d26c55e558`.
