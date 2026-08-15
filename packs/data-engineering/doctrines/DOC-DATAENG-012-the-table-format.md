---
summary: The table format.
type: doctrine
tags: [eos]
id: DOC-DATAENG-012
statement: The table format.
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
migration_sources: [packs/data-engineering/PACK.md:preferences:001]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DATAENG-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

An open format with hidden partitioning and one with a transaction log both meet B2, and the argument between them is unsettled.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:preferences:001`, lines 247-249, SHA-256 `655edd79d0b244d9b118266ed55fa960c2bb7a5b79a7039912cf9b7aab323e53`.
