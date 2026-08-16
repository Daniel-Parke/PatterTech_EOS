---
summary: The tenant boundary is enforced below the code that serves the request.
type: doctrine
tags: [eos]
id: DOC-IDENT-002
statement: The tenant boundary is enforced below the code that serves the request.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [serves_multiple_tenants]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-IDENT-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where one system holds more than one customer's data, the
tenant predicate is applied by the storage layer, by a separate schema
or by a separate store, so that one forgotten condition in one query
cannot cross the boundary. The tenant is taken from the authenticated
credential and never from a parameter, a header or a path segment the
caller controls. Where a database row policy is the mechanism, the
bypass paths are closed in the same change: the application does not
connect as the table owner, no application role carries the bypass
attribute, and the tenant is set per transaction rather than per
connection. Predicate: `serves_multiple_tenants`. Prevents: a
cross-tenant read, which one source calls potentially unrecoverable for
the business it happens to (AWS SaaS Lens, PostgreSQL row security docs,
Azure multitenancy guidance).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:requirements:002`, lines 123-136, SHA-256 `8322b4e5444a5ba63f30711f6ef7c90d4bc3c62c13ae891670ac4991abeb8877`.
