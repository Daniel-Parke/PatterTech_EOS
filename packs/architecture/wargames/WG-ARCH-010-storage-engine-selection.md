---
id: WG-ARCH-010
summary: Which storage engine owns a workload when transactional, analytical, search, graph, object or time-series needs pull in different directions?
kind: wargame
type: wargame
tags: [arch, data, eos, infra, wargame]
scenario_modes: [selection, conflict, gap]
applicable_doctrines: [DOC-ARCH-004, DOC-ARCH-011, DOC-DATA-008]
gap_domain: storage-engine-selection
applies_when: [has_database, stores_persistent_data]
engages_when: [requires_storage_engine_choice]
consequence: high
relations: [DREL-ARCH-001]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0057, EV-0151, EV-0162, EV-0309, EV-0310, EV-0311, EV-0572, EV-0573]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-ARCH-010: Which storage engine owns the workload?

## Decision question and stakes

Choose the authoritative storage shape for a named workload and decide whether
a specialist index or derived store is earned. Engine choice fixes transaction
and consistency guarantees, query shape, concurrency, backup and restoration,
operational ownership and exit cost. A benchmark that measures only one query
cannot settle that contract.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-004` starts with one deployable and one database.
- `DOC-ARCH-011` retains one database until a real owner or asymmetric volume
  appears.
- `DOC-DATA-008` keeps analytical storage simple until its working set argues
  otherwise.
- `DREL-ARCH-001` records the tension between one authoritative store and a
  materially different analytical or specialist workload.
- The uncovered domain is `storage-engine-selection`.

## Preconditions and engagement triggers

Describe the representative read and write trace, data model, invariants,
transaction boundary, query latency and throughput, concurrency, growth,
retention, consistency, search or traversal need, and recovery objectives.
Name the system of record and whether any candidate is derived and rebuildable.
Include export format, backup, restore and operator competence.

Applicability is `has_database` or `stores_persistent_data`. Engage when
`requires_storage_engine_choice` is true.

## Options

### A. One general-purpose transactional relational store

Keep records, constraints and ordinary queries in one transactional database,
using indexes and native capabilities before adding a new engine. This gives a
clear authority and recovery route. It may not meet a genuinely asymmetric
analytical, search, graph, object or time-series workload.

### B. One analytical or file-oriented engine for a bounded data product

Use an analytical engine or queryable files where append, scan, join and
aggregation dominate and multi-row transactional service writes do not. This
can be simple for local analysis (EV-0572, EV-0573), but is not a transactional
or high-concurrency service store.

### C. Authoritative store plus rebuildable specialist projection

Keep writes and invariants in A, then feed a search, analytical, graph or
time-series projection with a lag and rebuild contract. This earns specialist
reads without splitting truth. It adds delivery lag, dual schemas and a
reconciliation path.

### D. Separate authoritative specialist store

Let a specialist engine own the data because its model or guarantee is the
product requirement, not merely a faster query. This can avoid forcing the
workload into an unsuitable abstraction. It takes on separate operational,
transaction, backup, restore, migration and skill obligations.

## Failure premises

### Premortem for A. One general-purpose transactional relational store

Assume A failed. A large scan or index burden damaged transactional journeys,
or application code simulated specialist semantics poorly while the team
defended one database as an absolute rule.

### Premortem for B. One analytical or file-oriented engine for a bounded data product

Assume B failed. The bounded data product acquired concurrent writes,
authorisation or transactional invariants, and an analytical tool became an
unowned service database.

### Premortem for C. Authoritative store plus rebuildable specialist projection

Assume C failed. Projection lag was invisible, deletes or authorisation changes
did not propagate, and a rebuild could not reproduce the visible result. Users
treated stale derived state as truth.

### Premortem for D. Separate authoritative specialist store

Assume D failed. The engine met its headline query but lacked a proved restore,
export or transactional guarantee. The specialist choice became a permanent
operating cost for a workload that ordinary indexing could have served.

## Decision rule

Choose A when it meets the representative trace and recovery objective after
ordinary schema and index work. Choose B only for a bounded analytical data
product whose service-write invariants are elsewhere or absent. Choose C when a
specialist read model meets a named objective and can be rebuilt from the
authority within the recovery target. Choose D only when the specialist model
or guarantee is itself required and its write, consistency, restore and exit
tests pass.

Prefer C over a second authority. A faster specialist read does not justify D
unless ownership of truth also changes deliberately.

## Safe default

One general-purpose transactional store for authoritative records, with
ordinary indexes and one tested restore route. Add a rebuildable specialist
projection only after a representative trace shows a named miss.

## Cheapest discriminating test

Replay the representative read and write trace against A and the leading
alternative. Seed one invariant violation and one dependency outage. Measure
correctness, p95 latency, throughput, storage growth and operator work, then
restore or rebuild enough state to answer a named validation query within the
target.

## Fallback, exit and revisit

**Fallback `single-authority`:** keep the original transactional authority and
disable or rebuild the specialist projection. If the specialist is already
authoritative, stop writes and export to the last proved portable form.

**Exit condition:** leave a candidate when an invariant, consistency, restore,
export or representative performance objective fails, or when no named owner
can operate it.

**Revisit trigger:** repeat when the workload trace, authority, consistency,
recovery objective, owner, volume asymmetry or engine lifecycle changes.

## Counter-evidence and transfer limits

Database patterns and maintainer documentation describe mechanisms rather than
universal winners. The working set matters more than stored total for many
analytical decisions, but no retained source supplies a safe size threshold.
A local analytical engine's interoperability does not qualify it as a service
store. One trace cannot represent every future query, so the ruling carries the
recorded trace, growth assumption and restore evidence as transfer limits.
