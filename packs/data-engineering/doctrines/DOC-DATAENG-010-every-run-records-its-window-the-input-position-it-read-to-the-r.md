---
summary: Every run records its window, the input position it read to, the row counts in and out, and the version of the code that ran.
type: doctrine
tags: [eos]
id: DOC-DATAENG-010
statement: Every run records its window, the input position it read to, the row counts in and out, and the version of the code that ran.
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
migration_sources: [packs/data-engineering/PACK.md:defaults:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D7]
---

# DOC-DATAENG-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Without
the input position a rerun cannot be reasoned about, and without the
counts nobody can tell a quiet loss from a quiet duplicate. The fields
are in `packs/data-engineering/refs/RUN_LEDGER.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:007`, lines 233-237, SHA-256 `8284f612e80a9fe4576f557954d2e87a170882519140bc2800992a0419689f02`.
