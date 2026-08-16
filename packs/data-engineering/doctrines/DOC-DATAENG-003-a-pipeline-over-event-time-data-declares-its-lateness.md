---
summary: A pipeline over event-time data declares its lateness horizon and where arrivals past it go. Nothing is dropped silently.
type: doctrine
tags: [eos]
id: DOC-DATAENG-003
statement: A pipeline over event-time data declares its lateness horizon and where arrivals past it go. Nothing is dropped silently.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [processes_event_time_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-DATAENG-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`processes_event_time_data`. The streaming model paper's argument is
that completeness is never known, and that a progress marker fails in
two directions rather than one: too fast, and records arrive behind it,
so trusting it alone is knowingly lossy; too slow, and one straggler
holds the whole pipeline's output back. The stream processor's time
documentation states that no time can be named by which every record of
a given timestamp will have arrived. *Prevents*: the quietest loss in
this domain, a record discarded for being late by a threshold nobody
chose, in a pipeline whose row counts all reconcile. *Basis*:
empirical-evidence, on peer-reviewed work, with the engine documentation
as the mechanism.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:requirements:003`, lines 160-172, SHA-256 `19974c7e9340e68c0f7445b473aae2b1e143c7398e5aa94ba03bf2a260d013e9`.
