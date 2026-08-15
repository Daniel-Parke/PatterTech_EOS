---
summary: How data arrives and is reprocessed, delivery guarantees per hop, idempotent reruns, the processing window, backfill, late and duplicate records and partitioning
type: playbook
tags: [data, ops, state, realtime]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data, runs_scheduled_pipeline, reprocesses_data, processes_event_time_data]
activation_paths: [**/pipelines/**, **/ingest/**, **/ingestion/**, **/etl/**, **/elt/**, **/dags/**, **/airflow/**, **/connectors/**, **/cdc/**, **/streams/**, **/*backfill*, **/*reprocess*, **/*debezium*, **/*kafka*]
volatility: slow
review: 2028-04
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
---

# Data engineering

This pack covers how data gets in and how it is put right: ingestion by
batch, stream or change capture, delivery guarantees, idempotent
reprocessing, backfill, late and duplicate records, and partitioning. It
activates when a pipeline pulls from a system the venture does not own,
when a run repeats a period already processed, or when records carry a
time of occurrence separate from their arrival. What a number means
belongs to data-analytics.

## Activation

Load this pack when any of the following is true. Paths and keywords are
cheap and noisy; the predicates decide, and a task that trips a path
trigger but satisfies no predicate loads nothing beyond the paragraph
above.

**Path triggers.** Pipeline, ingestion and extract directories; DAG or
workflow definitions; connector configuration; change-capture
configuration; stream consumer and producer code; anything whose name
carries backfill or reprocess; landing, raw and staging trees.

**Task types.** Add or change a source of data. Change how often a
pipeline runs or how wide its window is. Repair a period that was
already processed. Load history for the first time. Change a partition
scheme. Move a step between batch and streaming. Investigate duplicate
or missing rows in a landed table.

**Keyword fallback.** Ingest, pipeline, backfill, reprocess, replay,
watermark, late data, out of order, deduplicate, idempotent,
at-least-once, exactly-once, change data capture, high-water mark,
partition, snapshot, incremental, batch window. Keywords are the weakest
signal and never on their own justify the requirements below.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| `ingests_external_data` | The venture takes data in from a system it does not own and lands it somewhere of its own. |
| `runs_scheduled_pipeline` | Data processing runs on a schedule or a trigger rather than in response to a user request. |
| `reprocesses_data` | The work reruns a period that has already been processed: a retry, a correction or a backfill. |
| `processes_event_time_data` | Records carry a time at which the thing happened, distinct from the time they arrived. |
| `stores_persistent_data` | State outlives a single run and matters if lost. |

The first four are proposed rather than adopted. They are argued in
`packs/data-engineering/research/NOTES.md` under the predicates section,
with what settles each and why none of them is an existing row wearing a
new name. Check S021 fails until the integrator rules on them, and that
failure is expected rather than a defect in this pack.

B1 needs `ingests_external_data` or `runs_scheduled_pipeline`. B2 needs
`reprocesses_data`. B3 needs `processes_event_time_data`. A one-off
export somebody reads and deletes trips nothing.

**Policy and guard contact.** Overwriting a partition and deleting a
window before rewriting it are both production-data handling under
`kernel/GUARD_SPEC.md`, and a backfill that deletes before it writes is
a deletion whatever the intent. This pack sets no tiers; the router in
`kernel/POLICY_SPEC.md` does. What the pack adds is what a task at that
tier has to produce.

## Outcomes and non-goals

**Outcomes.** A pipeline can be rerun over any period without anybody
first working out what it already wrote. The answer for a given window
does not depend on when the run happened. A duplicate arriving twice
lands once, because the sink was built expecting it rather than because
the source promised not to. Late records have a declared destination
rather than a silent one. A backfill is the ordinary pipeline given
different dates, so the code that repairs history is the code that
produced it.

**Non-goals.** This pack stops where correct bytes have landed in a
correct partition. What the number means, how an event is named, what
gates publication of an analytics table, how an experiment ends and what
the analytics layer may hold about a person are all
`packs/data-analytics/PACK.md`, and none of it is restated here. Schema
migration mechanics, restore proof and rollout are
`packs/devops-reliability/PACK.md`. Envelope, transport and webhook
contract shape are `packs/api-integration/PACK.md`. Lawful basis for a
column that identifies a person is `packs/security-privacy/PACK.md` and
data-analytics B3. This pack picks no orchestrator, no table format and
no broker.

**One explicit non-requirement.** No target for freshness or for lag as
an estate number. Both are properties of a particular source and a
particular consumer's need, and a fleet-wide figure over them is
arithmetic with no referent. Declare the freshness a consumer needs per
table, and check that; never average it.

## Binding requirements

Three. Each names the failure it prevents, what the evidence is and the
basis it rests on. Departure needs an accepted ADR. The list is short on
purpose: it was tested against the two-limb rule in ADR-0008, and the
rules that failed it are defaults below with the reason recorded.

**Evidence pointer.** This pack has not been imported into
`registry/evidence.json`, so it carries no `EV-` ids yet. The twelve
sources are frozen at
`packs/data-engineering/research/sources.fragment.json` with the
eighteen-field record shape, the synthesis is in
`packs/data-engineering/research/NOTES.md`, and the licence and
quotation sweep is at
`packs/data-engineering/research/provenance.fragment.json`. Until the
import assigns ids, prose here names sources by short label, and the
notes carry the label-to-fragment table under the heading about how the
read surface cites. Inventing an id would be worse than naming the
source.

**B1. Every hop between two systems states its delivery guarantee, and a
sink that is not idempotent or transactional is treated as
at-least-once.** `ingests_external_data`, `runs_scheduled_pipeline`. The
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

**B2. Reprocessing a window replaces a bounded unit or merges on a
declared key. Bare append is not a reprocessing strategy.**
`reprocesses_data`. The incremental-strategy documentation is explicit
that append checks nothing, so a rerun duplicates, and that every other
strategy rests on a key whose reliability is the strategy's real value:
a merge with no key degrades into an append without saying so. The
atomic primitive underneath is the table format specification's pointer
swap, which is what makes "replace the partition" a single commit rather
than a delete with a window in the middle where the table is wrong.
*Prevents*: duplicate rows that compound on every retry and cannot be
told apart afterwards, which is the one data defect with no clean
recovery short of a full rebuild. *Basis*: standard, on one format
specification for the primitive and one maintainer document for the
strategies.

**B3. A pipeline over event-time data declares its lateness horizon and
where arrivals past it go. Nothing is dropped silently.**
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

## Defaults

Starting positions. Override any of them with a reason recorded in the
change record or the lock-book; an unrecorded override is the finding.

**D1. The processing window comes from the scheduler or from the data,
never from the run's own clock, and it is written down with the
output.** The orchestrator's best-practice documentation puts the
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

**D2. Backfill is the scheduled pipeline given different dates.** No
separate backfill script, no notebook, no one-off query. The microbatch
documentation makes this the shape rather than the exception: the same
model run with an explicit start and end, batch by batch, each one
replaced atomically. *Reason to depart*: a first historical load whose
volume genuinely cannot go through the ordinary path, which is a
capacity argument to record rather than a habit.

**D3. Log-based change capture over polling, where the venture is
allowed to read the source's log.** Polling a modified-at column cannot
see a delete, cannot see a row that changed twice between polls, and
needs a column the source's data model did not want. *Reason to depart*:
no log access, which is the common case for third-party systems, and
then the deletes have to be handled another way and the pipeline says
how.

**D4. The partition value is derived by the engine from a real column,
or in exactly one place in code, and never written by hand at the call
site.** Where the format supports a declared transform of the event-time
column, use it and let the engine apply it. Where it does not, one
function owns the derivation. *Reason to depart*: a table small enough
that it is not partitioned at all, which is most tables in a young
venture.

**D5. One bounded window per run, sized so a single window can be
reprocessed inside the schedule interval.** If a day's window takes
thirty hours to rerun, the window is wrong, and the pipeline has no
recovery path that does not fall further behind.

**D6. Start in batch. Move a step to streaming only when a named
decision cannot wait for the next run.** Streaming buys latency and
charges for it in operational surface, an event-time clock, a lateness
policy and a process to keep alive. *Reason to depart*: the decision
exists and is named, or the source is a stream already and batching it
would mean inventing a landing area.

**D7. Every run records its window, the input position it read to, the
row counts in and out, and the version of the code that ran.** Without
the input position a rerun cannot be reasoned about, and without the
counts nobody can tell a quiet loss from a quiet duplicate. The fields
are in `packs/data-engineering/refs/RUN_LEDGER.md`.

**D8. Rejected and very-late records go to a quarantine table with the
reason and the raw payload, not to a log line.** A log line is not a
record you can reprocess from.

## Preferences

Taste. Record them, do not gate on them, override without asking.

- The table format. An open format with hidden partitioning and one with
  a transaction log both meet B2, and the argument between them is
  unsettled.
- Whether the merge key is the source's natural key or a hash of it.
- The orchestrator, and whether the window arrives as a CLI flag or a
  configuration value.
- Compaction cadence and small-file policy, until the read time
  complains.
- Whether quarantine is a table per source or one table with a source
  column.

## Decision map

The material forks, each argued in a guide.

| Fork | Guide | Default |
| --- | --- | --- |
| How does the data get here: batch, stream or change capture | `packs/data-engineering/guides/GD-DATAENG-001-ingestion-shape.md` | Scheduled batch, change capture where the log is readable |
| How is a reprocess made idempotent | `packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md` | Replace a bounded unit |
| Where does the processing date come from | `packs/data-engineering/guides/GD-DATAENG-003-processing-window.md` | The scheduler's interval, or the event time in the data |
| How are late and out-of-order arrivals handled | `packs/data-engineering/guides/GD-DATAENG-004-late-arrivals.md` | A declared lookback, with a quarantine beyond it |

Level-three detail sits in `packs/data-engineering/refs/`: the per-hop
guarantee table, the run ledger fields, and partition choice and
evolution. A full worked application is in
`packs/data-engineering/exemplars/EX-DATAENG-001-orders-backfill.md`.
The pack's own evaluation criteria are in
`packs/data-engineering/CHECKS.md`.

## Failure modes and anti-patterns

- **The wall-clock window.** The run computes its own dates from the
  machine's clock, so a rerun on Thursday reprocesses Thursday and the
  Tuesday that failed stays broken. D1.
- **The partition column written by hand.** The writer formats the date
  itself and gets the format, the time zone or the source column wrong.
  Every query keeps working and the answers are wrong. D4.
- **The backfill that is not the pipeline.** A one-off script repairs
  history using logic that has since diverged, and the repaired period
  no longer agrees with the periods either side of it. D2.
- **Bare append plus a retry.** The job failed at eighty per cent, the
  retry appended the whole window again, and there is now no way to tell
  the second copy from the first. B2.
- **Exactly-once taken from a feature list.** A guarantee scoped to one
  hop between two systems read as a property of the whole pipeline. The
  change-capture project's own exactly-once page is the antidote: it
  says it cannot tell whether the underlying implementation is correct in
  every case. B1.
- **The watermark tuned until the late count reads zero.** Moving the
  threshold until nothing is reported late does not mean nothing is
  late. B3.
- **The unbounded lookback.** Reprocessing thirty days every night to
  avoid choosing a horizon, so the pipeline cost grows with history and
  the real lateness is still unknown.
- **Over-partitioning.** Hourly partitions on a table taking a thousand
  rows a day, which buys a small-file problem and no pruning.
- **The dedupe key that is not unique in the source.** A merge on a key
  the source reuses quietly overwrites a different row. The
  incremental-strategy documentation says the strategy is only worth its
  key.
- **Polling and assuming deletes do not happen.** A modified-at poll
  cannot see a row that went away, so the target keeps it for ever. D3.
- **The snapshot restarted from scratch.** A change-capture snapshot
  that never completes, restarted repeatedly, each attempt loading more
  duplicates into a target that was never built to expect them.
- **Reading whatever the source holds now.** A transform with no window
  at all, so two runs of the same code disagree and neither is wrong.
- **Partition evolution treated as a rewrite.** Changing the layout is a
  metadata change: old files keep the old scheme and the reader plans
  both. Cheap to declare, not free to read.
- **The idempotent-write token reused after a reset.** The counter
  starts again below the recorded high-water mark and the table silently
  ignores good writes, which fails in the dangerous direction.

## Open questions and counter-evidence

Named honestly, because the sources disagree in places and are thin in
others.

**Exactly-once is contested by one of the projects that ships it.** The
broker documents a real mechanism and scopes it carefully. The
change-capture project, building on that mechanism, publishes a warning
that it cannot tell whether the implementation is correct in every case,
that no thorough analysis of it exists, that independent testing of other
systems speaking the same protocol raised correctness concerns, and that
protocol issues are open. That is a maintainer reading another project's
open issues rather than a demonstrated defect, and open issues are not
proof of failure in practice. B1 does not resolve the argument. It
assumes at-least-once and requires an idempotent sink, which is correct
whichever way the argument goes.

**The rule this pack most wanted to bind is a default.** D1, the
processing window, prevents exactly the kind of silent, hard-to-reverse
corruption that ADR-0008's first limb is about, and its basis is two
maintainer documents, which fails the second. Rather than inflate the
basis field to keep the authority, the rule is a default and this
paragraph is the record of why. If a standard or a measurement for it
turns up, it should be re-argued for binding.

**The streaming model paper is not disinterested and is from 2015.** It
argues against running batch and streaming systems side by side on
complexity grounds while its authors sell the unified alternative, and
several systems it criticises have changed substantially since. Only the
completeness argument and the two watermark failure directions are taken
from it here, because those are structural rather than comparative. It
is also the one source in this pack whose licence restricts reuse of
wording, so it is paraphrased throughout and never quoted.

**Nobody has measured the reprocessing fork.** No study was found
comparing partition replacement against merge for correctness or cost at
any scale. The cost claims in the maintainer documentation carry no
numbers, and the case where the two genuinely disagree, a correction
that moves a row from one partition to another, is addressed by no
source found. GD-DATAENG-002 argues it from mechanism, which is weaker
than evidence and is labelled as such.

**Every lateness horizon in this pack is declared, not derived.** No
published figure was found for how much late data a real source
produces. B3 therefore requires the number to exist and be defended, and
refuses to name a right one. The microbatch documentation's default of
one prior batch is a guess wearing a default's clothes, and a source
with a longer tail loses records under it silently.

**The table format argument is unsettled and this pack does not take a
side.** Two actively maintained open formats cover the same ground with
different designs, one specification openly says its next version is not
adopted, and the idempotent-write token that is useful for keyless
payloads exists in only one of them. Picking one is a bet, so it sits in
preferences rather than in defaults.

**Warehouse support for the mechanisms is uneven.** The strategies
documented are not all available on every platform, and the atomic
replacement a framework promises is whichever mechanism its adapter
happens to have, which means the guarantee is really the warehouse's. A
venture reading this pack has to check what its own platform actually
does before relying on B2.

**Every source assumes a data team.** Not one was written for a one or
two person venture, which is the same gap `packs/data-analytics/PACK.md`
records. D5, D7 and the run ledger are written to be satisfiable by one
table and one function, which is a judgement rather than a finding.

**Refresh triggers.** Re-argue this pack on: any independent analysis of
the transaction protocol behind the exactly-once claims; a published
measurement of late-arrival distributions from a real source; a
resolution of the open table format argument; a standard, as opposed to
a maintainer document, covering the processing window, which would move
D1; and a change to what the venture's own warehouse supports.
