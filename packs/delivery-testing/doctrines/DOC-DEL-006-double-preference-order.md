---
summary: Double preference order.
type: doctrine
tags: [eos]
id: DOC-DEL-006
statement: Double preference order.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0093, EV-0187]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

real implementation, then a real
  dependency in a throwaway container, then a verified fake with a
  contract suite, then a narrow stub, and interaction mocking last
  (EV-0187, EV-0093). Reason: each step down the ladder buys speed and
  pays in fidelity, and the last step couples the test to how the code
  works. Argued in WG-DEL-005.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:001`, lines 159-164, SHA-256 `ba693fe245b7b474711acacf56b6790752115b06c0d0ca4eac6823fa871d48a9`.
