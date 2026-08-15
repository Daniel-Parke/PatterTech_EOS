---
summary: Start in batch. Move a step to streaming only when a named decision cannot wait for the next run.
type: doctrine
tags: [eos]
id: DOC-DATAENG-009
statement: Start in batch. Move a step to streaming only when a named decision cannot wait for the next run.
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
migration_sources: [packs/data-engineering/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-DATAENG-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Streaming buys latency and
charges for it in operational surface, an event-time clock, a lateness
policy and a process to keep alive. *Reason to depart*: the decision
exists and is named, or the source is a stream already and batching it
would mean inventing a landing area.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:006`, lines 226-231, SHA-256 `ac11c8608e5b64db3bdd43169c2595c34ec3a3eeef620115ce7aacab39a564fe`.
