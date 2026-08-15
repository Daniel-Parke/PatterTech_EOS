---
summary: Every double standing in for a dependency outside the venture's control has a contract suite that runs the same cases against the double and the real implementation, on a stated cadence.
type: doctrine
tags: [eos]
id: DOC-DEL-002
statement: Every double standing in for a dependency outside the venture's control has a contract suite that runs the same cases against the double and the real implementation, on a stated cadence.
kind: doctrine
authority: binding
basis: standard
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0186, EV-0187]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Outside
   the venture's control means a third-party API, a payment provider, a
   service another team ships. Basis standard, from the contract-test
   practice in EV-0186 and the fidelity requirement in EV-0187.
   Prevents: silent drift, where the fake keeps answering a question the
   real service stopped answering months ago, which nobody sees until
   production. Doubles for something inside the repository are a default
   below, because there the real thing is available and the drift shows
   up at the next integration rather than at a customer.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:requirements:003`, lines 109-119, SHA-256 `71be7db78a0f3fd8ca69a9f1fa46afc1da3e72f917388b28cbd386ecdc4f475b`.
