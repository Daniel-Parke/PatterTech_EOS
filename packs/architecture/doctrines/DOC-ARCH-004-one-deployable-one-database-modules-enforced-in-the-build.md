---
summary: One deployable, one database, modules enforced in the build.
type: doctrine
tags: [eos]
id: DOC-ARCH-004
statement: One deployable, one database, modules enforced in the build.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0152, EV-0153, EV-0159]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-ARCH-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: the module decomposition and the process decomposition are
separate decisions, and forcing them to be one buys the wrong boundary
at the highest price (EV-0152, EV-0153). Shopify (EV-0159) is the
existence proof that a very large codebase can hold boundaries inside
one process.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:001`, lines 144-149, SHA-256 `526696b42718e95429b01ff806a4386b1d05383c6106df0faf467e8b271c0e78`.
