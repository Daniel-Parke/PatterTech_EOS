---
summary: Webhook signatures over the triple id.timestamp.payload with a versioned prefix.
type: doctrine
tags: [eos]
id: DOC-API-012
statement: Webhook signatures over the triple id.timestamp.payload with a versioned prefix.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [exposes_service_boundary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0125]
review: 2027-12
lifecycle: active
verification_refs: [packs/api-integration/CHECKS.md]
migration_sources: [packs/api-integration/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
---

# DOC-API-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

for anything we emit (EV-0125). Timestamp
  tolerance five minutes: that number is an estate choice, since no
  source fixes one.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/api-integration/PACK.md:defaults:008`, lines 161-164, SHA-256 `ab4664c8f2dbf151cae405eb678a23d28b7f1947a9337cb56e4af8abaf2bfe67`.
