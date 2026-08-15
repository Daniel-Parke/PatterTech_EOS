---
summary: Every hop between two systems states its delivery guarantee, and a sink that is not idempotent or transactional is treated as at-least-once.
type: doctrine
tags: [eos]
id: DOC-DATAENG-001
statement: Every hop between two systems states its delivery guarantee, and a sink that is not idempotent or transactional is treated as at-least-once.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-DATAENG-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`ingests_external_data`, `runs_scheduled_pipeline`. The
broker's own delivery-semantics documentation says exactly-once claims
need their fine print read because they usually assume nobody fails, and
then scopes its own to reading from the log and writing back to it,
where the consumer's position commits inside the same transaction as the
output. Write anywhere else and the choices are a two-phase commit the
sink probably does not support, or storing the position in the same
place as the output. The stream processor's checkpointing documentation
says the same from the other side: its exactly-once setting is about its
own state, and carrying that outward needs the sink to take part.
*Prevents*: a pipeline built on a guarantee that stops at a boundary
nobody drew, so duplicates land in the table of record and nothing is
looking for them. *Basis*: standard, on two protocol and engine
documentation sets that agree against the marketing around them.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:requirements:001`, lines 128-143, SHA-256 `03b22fd75f84a8352944e0fe01fb6aa0ab05e1ae19cc4b72359f766bfcfbc355`.
