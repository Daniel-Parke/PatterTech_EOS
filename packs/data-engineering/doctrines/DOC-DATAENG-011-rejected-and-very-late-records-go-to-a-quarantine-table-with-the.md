---
summary: Rejected and very-late records go to a quarantine table with the reason and the raw payload, not to a log line.
type: doctrine
tags: [eos]
id: DOC-DATAENG-011
statement: Rejected and very-late records go to a quarantine table with the reason and the raw payload, not to a log line.
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
migration_sources: [packs/data-engineering/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-DATAENG-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A log line is not a
record you can reprocess from.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:008`, lines 239-241, SHA-256 `400f9bfb230e96dcd6597498bdc1285a57b1888fc559df58b76ef9cef94d48c0`.
