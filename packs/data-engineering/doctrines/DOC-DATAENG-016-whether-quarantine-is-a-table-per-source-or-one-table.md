---
summary: Whether quarantine is a table per source or one table with a source column.
type: doctrine
tags: [eos]
id: DOC-DATAENG-016
statement: Whether quarantine is a table per source or one table with a source column.
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:preferences:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DATAENG-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No separate rationale was recorded.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:preferences:005`, lines 255-256, SHA-256 `2eeb96e06e508be4dccaad3e730b60da33f4394f74c05bfa9ae176ad1b752f2e`.
