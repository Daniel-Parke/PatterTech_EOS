---
summary: Property tests are seeded and replayable in CI.
type: doctrine
tags: [eos]
id: DOC-DEL-013
statement: Property tests are seeded and replayable in CI.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0017, EV-0188]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

(EV-0188,
  EV-0017). Reason: an unseeded property test in a blocking gate
  manufactures flake.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:008`, lines 249-251, SHA-256 `5279b3af3fbd3c4a12325542bab20ed955da6f4f2b0c741a5f747194116256ce`.
