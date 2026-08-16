---
summary: Shared tables with a tenant key and a database-enforced predicate, until a customer's own keys, data location or backup policy buys them a dedicated store.
type: doctrine
tags: [eos]
id: DOC-IDENT-016
statement: Shared tables with a tenant key and a database-enforced predicate, until a customer's own keys, data location or backup policy buys them a dedicated store.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [authenticates_people]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-IDENT-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Density is cheap and dedicated stores are bought per requirement, not per customer

Azure multitenancy guidance, AWS SaaS Lens

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:defaults:006`, lines 183-183, SHA-256 `9432e4a94288d288a6a40fa1619c9cc34810ccdb9de01e702048ddcf9cb3dc64`.
