---
summary: Two queues, incident and request, with separate targets and no item in both.
type: doctrine
tags: [eos]
id: DOC-SUPPORT-008
statement: Two queues, incident and request, with separate targets and no item in both.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0426]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Restoring an interrupted service and fulfilling a
  routine ask have different clocks, so one target describes neither
  (EV-0426). The queue axis in B1 carries the split.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:defaults:006`, lines 231-234, SHA-256 `c9afefda8fb88d1f998ce2853b972579da0a179b9b5a5bcc8c0c22cec7d2aef1`.
