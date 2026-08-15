---
summary: The processing window comes from the scheduler or from the data, never from the run's own clock, and it is written down with the output.
type: doctrine
tags: [eos]
id: DOC-DATAENG-004
statement: The processing window comes from the scheduler or from the data, never from the run's own clock, and it is written down with the output.
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
migration_sources: [packs/data-engineering/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-DATAENG-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The orchestrator's best-practice documentation puts the
current-time call out of bounds inside a task, and most firmly out of
bounds in the arithmetic that matters, and says a task reads and writes
a named window rather than whatever the source happens to hold at that
moment. The table format's partitioning documentation supplies the
failure: when the writer supplies the partition value, using the wrong
source column, and it names the processing time in place of the event
time as exactly that mistake, lands a wrong answer while every query
keeps succeeding. *Reason to depart*: a source that carries no usable
time at all, in which case the arrival window is the honest answer and
the table says so in its own column name. *Why this is a default rather
than binding*: it prevents a serious and quiet failure, so it passes the
first limb of ADR-0008, but its basis is two maintainer documents and it
fails the second. It is the rule this pack would most like to bind, and
the open questions below say so plainly.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:001`, lines 179-195, SHA-256 `3809fb6a16a3ec19ce382d56296e01470935d541f40243c3a12627b1e17bbf75`.
