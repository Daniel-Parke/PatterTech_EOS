---
summary: Whether the merge key is the source's natural key or a hash of it.
type: doctrine
tags: [eos]
id: DOC-DATAENG-013
statement: Whether the merge key is the source's natural key or a hash of it.
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
migration_sources: [packs/data-engineering/PACK.md:preferences:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DATAENG-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No separate rationale was recorded.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:preferences:002`, lines 250-250, SHA-256 `f667e29d3f71784dc4a5b9d464bd79de255be55a5deab63dffcd46b36fc8fa13`.
