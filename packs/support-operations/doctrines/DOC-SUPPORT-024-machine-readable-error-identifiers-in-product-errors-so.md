---
summary: Machine-readable error identifiers in product errors so a ticket can be matched to a cause without a screenshot (EV-0122).
type: doctrine
tags: [eos]
id: DOC-SUPPORT-024
statement: Machine-readable error identifiers in product errors so a ticket can be matched to a cause without a screenshot (EV-0122).
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0122]
review: on-change-of:ISO-10002-revision
lifecycle: active
verification_refs: [packs/support-operations/CHECKS.md]
migration_sources: [packs/support-operations/PACK.md:preferences:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-SUPPORT-024

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No separate rationale was recorded.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/support-operations/PACK.md:preferences:006`, lines 301-302, SHA-256 `9907accb6c4296ac68c2882567a047fb3685575fb34db9aaf412b25e0826b671`.
