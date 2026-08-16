---
summary: Whether documentation lives with the code or in its own repository.
type: doctrine
tags: [eos]
id: DOC-DOCS-017
statement: Whether documentation lives with the code or in its own repository.
kind: doctrine
authority: preference
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0095]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:preferences:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DOCS-017

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Edit-on-encounter (EV-0095) argues for beside the code
  and this repository takes that bet, but it is not evidenced.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:preferences:004`, lines 273-275, SHA-256 `6d35c67933a5d23ccf40f1b1975833e8e224d95d81257868e173fa352a7327a8`.
