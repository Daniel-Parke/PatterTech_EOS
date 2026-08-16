---
id: WG-DATA-001
summary: Which tabular engine and execution mode fits the measured workload without importing unnecessary distribution or losing required semantics?
kind: wargame
type: wargame
tags: [data, eos, perf, tooling, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-DATA-008, DOC-DATAENG-009, DOC-DATA-020, DOC-DATA-021]
gap_domain: data-compute-engine-selection
applies_when: [reads_for_decision, publishes_analytics_table, ingests_external_data]
engages_when: [requires_tabular_engine_choice, working_set_exceeds_memory]
consequence: high
relations: []
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0563, EV-0564, EV-0566, EV-0567, EV-0568, EV-0572, EV-0573, EV-0574]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-DATA-001: Which analytical engine and execution mode?

## Decision question and stakes

Choose the smallest tabular engine and execution mode that preserves the
workload's required semantics and meets its measured time, memory and
operability objective. The choice affects more than speed. Index behaviour,
ordering, type conversion, inspection, spilling, deployment and recovery can
all change when a pipeline moves between a dataframe, local SQL and a
distributed engine.

This Wargame covers two separately ruleable pressures: engine selection and
eager, lazy, streaming or out-of-core execution. A ruling records both even
when the answer is one tool and one mode.

## Doctrines or coverage gap under pressure

- `DOC-DATA-008` keeps analytical storage simple until the working set argues
  otherwise.
- `DOC-DATAENG-009` starts data movement in batch until a named decision needs
  lower latency.
- `DOC-DATA-020` requires representative measurement before a material
  performance, capacity or tool claim.
- `DOC-DATA-021` promotes compute only after the simpler measured rung fails.
- The uncovered domain is `data-compute-engine-selection`: no standing rule
  names a universal engine or data-size threshold, because the evidence does
  not support one.

## Preconditions and engagement triggers

Record the consumer-visible semantics, representative input, target hardware,
time objective, memory ceiling, concurrency, required integrations and
recovery route. State whether intermediate inspection is part of the job,
whether stable ordering matters, and whether the query must be repeatable from
pinned inputs.

Applicability is any of `reads_for_decision`, `publishes_analytics_table` or
`ingests_external_data`. Engage when `requires_tabular_engine_choice` or
`working_set_exceeds_memory` is true. Unknown memory pressure is measured
before it is treated as distribution pressure.

## Options

### A. Eager dataframe in the required ecosystem

Keep the work in the dataframe whose semantics and integrations are already
the contract, executing each operation eagerly. This makes intermediate state
easy to inspect and keeps index-sensitive or library-specific behaviour
intact. It also materialises intermediates and may repeat work that a planner
could remove (EV-0566, EV-0567).

### B. Lazy or streaming single-machine dataframe

Express the pipeline as a plan, inspect that plan, and let the engine push
filters and projections or stream supported operators. This can reduce memory
and wasted work while retaining a dataframe surface. It can also obscure the
moment an error occurs, alter assumptions about ordering, and fall back to
materialisation for unsupported operators (EV-0566, EV-0567).

### C. In-process analytical SQL with controlled spill

Use local analytical SQL for joins, aggregation and file scans, with the
storage path and spill behaviour made explicit. It can query common dataframe
representations and bridge an awkward pipeline without becoming a service
database (EV-0572). Out-of-core support is bounded by operator shape, disk and
concurrency, not an unlimited-memory promise (EV-0573).

### D. Distributed analytical execution

Partition the work across workers and accept shuffle, coordination, remote
state and a larger operational surface. This is the correct rung when a
representative one-node route cannot meet capacity, elapsed-time or
concurrency objectives. Distributed controls are real and useful, but the
maintainer evidence does not make them an upgrade for small work
(EV-0574).

## Failure premises

### Premortem for A. Eager dataframe in the required ecosystem

Assume A failed. Intermediates multiplied peak memory, one high-cardinality
join exhausted the process, and the team had no plan or spill trace showing
where capacity went. Alternatively, an engine migration done for fashion
broke an index or ecosystem contract that the benchmark never checked.

### Premortem for B. Lazy or streaming single-machine dataframe

Assume B failed. A blocking operation silently materialised the working set,
ordering changed, or the optimised plan was irreproducible because inputs,
versions and the plan were not recorded. The throughput number passed while
the output oracle was too weak to notice semantic drift.

### Premortem for C. In-process analytical SQL with controlled spill

Assume C failed. Spill turned a memory failure into unacceptable disk traffic,
concurrent jobs contended for the same resources, or an analytical engine was
misused as a transactional or multi-user serving store. Interoperability hid
copies at the boundary.

### Premortem for D. Distributed analytical execution

Assume D failed. Shuffle and coordination dominated the job, the deployment
became harder to reproduce than the pipeline, and nobody could show that a
single-node out-of-core route had failed the stated objective first.

## Decision rule

1. If dataframe semantics or a dependent ecosystem are contractual, start
   with A in that ecosystem.
2. If the same semantics hold and redundant materialisation causes the measured
   miss, test B against A with the plan and output oracle recorded.
3. If relational joins, scans or bounded spill are the dominant work, test C
   against the leading dataframe route.
4. Select D only when representative A to C probes fail a named capacity,
   duration or concurrency objective and partitioning can be stated before the
   cluster exists.
5. If `working_set_exceeds_memory` is true but C meets the objective with
   acceptable spill and recovery, remain local. Memory pressure alone does not
   choose distribution.

The ruling records engine and execution mode separately. A faster result loses
if it changes required semantics or cannot be reproduced twice from pinned
inputs.

## Safe default

Use the required ecosystem's simplest eager route for a small representative
baseline, then test the smallest single-machine planned or local-SQL route
that addresses the observed miss. No distributed default is safe without a
demonstrated distributed need.

## Cheapest discriminating test

Run one representative query or pipeline at target shape on the simplest two
credible candidates. Record output hash or numerical tolerance, wall time,
peak memory, spill, copies, plan, clean-run repeatability and the integration
work needed to put it into production. Include one input that exercises the
semantic difference most likely to matter, such as index alignment, nulls,
ordering or categorical values.

## Fallback, exit and revisit

**Fallback `known-semantic-baseline`:** return to A in the ecosystem whose
behaviour is already understood, reduce scope or process a bounded partition
while the capacity decision remains open.

**Exit condition:** leave the selected route when it violates required
semantics, cannot meet the recorded objective on representative work, or
cannot be restored and reproduced on the supported environment.

**Revisit trigger:** repeat the Wargame when working-set shape, concurrency,
latency objective, integration contract, engine version or deployment
boundary changes materially.

## Counter-evidence and transfer limits

The cited project documentation establishes supported behaviour, not an
independent performance ranking. No retained source supplies a universal
row-count or byte threshold. Lazy, streaming, out-of-core and distributed
execution each trade visibility and operating cost for a different capacity
property. Benchmark results transfer only with their input shape, environment,
versions and correctness oracle. Package names and versions belong in the
dated stack profile, not in this decision rule.
