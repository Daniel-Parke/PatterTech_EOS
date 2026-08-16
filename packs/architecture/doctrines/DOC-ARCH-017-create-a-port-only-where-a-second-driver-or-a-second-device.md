---
summary: Create a port only where a second driver or a second device is genuinely plausible.
type: doctrine
tags: [eos]
id: DOC-ARCH-017
statement: Create a port only where a second driver or a second device is genuinely plausible.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0150]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:preferences:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-ARCH-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Cockburn's 2005 statement (EV-0150) never bounded this, and an adapter per dependency is ceremony.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:preferences:002`, lines 234-236, SHA-256 `97201a57d08832e24077e43abfb0a996c4d8d8d2a3401d5b09735a870f633979`.
