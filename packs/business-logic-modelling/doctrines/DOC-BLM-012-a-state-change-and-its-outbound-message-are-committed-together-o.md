---
summary: A state change and its outbound message are committed together or not at all.
type: doctrine
tags: [eos]
id: DOC-BLM-012
statement: A state change and its outbound message are committed together or not at all.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0157]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D10]
---

# DOC-BLM-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`crosses_consistency_boundary`. The message goes to an
outbox written in the same transaction as the state change, and every
consumer is idempotent (EV-0157). Reason: otherwise the state is saved
with the event lost, or the event is sent with the state rolled back,
and nothing in the system can tell you which happened. This is a default
rather than binding because EV-0157 is a pattern catalogue with no
measurement behind it; the failure is real, the evidence is a
description. Depart only with a written account of how the two writes
are reconciled instead, and note that the pattern buys at-least-once
delivery and nothing more, which is why the idempotence half is not the
part to drop.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:010`, lines 203-214, SHA-256 `d97e2cbc43fe9e88f34c5672976430e12d62a91fe4c755d68de416fff5116de8`.
