---
summary: Log-based change capture over polling, where the venture is allowed to read the source's log.
type: doctrine
tags: [eos]
id: DOC-DATAENG-006
statement: Log-based change capture over polling, where the venture is allowed to read the source's log.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D3]
---

# DOC-DATAENG-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Polling a modified-at column cannot
see a delete, cannot see a row that changed twice between polls, and
needs a column the source's data model did not want. *Reason to depart*:
no log access, which is the common case for third-party systems, and
then the deletes have to be handled another way and the pipeline says
how.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:003`, lines 205-211, SHA-256 `6fca658e4fb843397fba699a6a98f2697c7fe4796007a6419535762a20663bd7`.
