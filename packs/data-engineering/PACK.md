---
summary: Activation, outcomes and decision map for the data-engineering Doctrine and Wargames
type: pack
tags: [data, ops, state, realtime]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [ingests_external_data, runs_scheduled_pipeline, reprocesses_data, processes_event_time_data]
activation_paths: [**/pipelines/**, **/ingest/**, **/ingestion/**, **/etl/**, **/elt/**, **/dags/**, **/airflow/**, **/connectors/**, **/cdc/**, **/streams/**, **/*backfill*, **/*reprocess*, **/*debezium*, **/*kafka*]
volatility: slow
review: none
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
display_name: Data Engineering
category: data-ai
id_namespace: DATAENG
depends_on: [architecture, security-privacy]
---


# Data Engineering

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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-DATAENG-001](doctrines/DOC-DATAENG-001-every-hop-between-two-systems-states-its-delivery.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-DATAENG-002](doctrines/DOC-DATAENG-002-reprocessing-a-window-replaces-a-bounded-unit-or-merges.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-DATAENG-003](doctrines/DOC-DATAENG-003-a-pipeline-over-event-time-data-declares-its-lateness.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-DATAENG-004](doctrines/DOC-DATAENG-004-the-processing-window-comes-from-the-scheduler-or-from.md) (default)
<a id="D2"></a>
- `D2` to [DOC-DATAENG-005](doctrines/DOC-DATAENG-005-backfill-is-the-scheduled-pipeline-given-different-dates.md) (default)
<a id="D3"></a>
- `D3` to [DOC-DATAENG-006](doctrines/DOC-DATAENG-006-log-based-change-capture-over-polling-where-the-venture.md) (default)
<a id="D4"></a>
- `D4` to [DOC-DATAENG-007](doctrines/DOC-DATAENG-007-the-partition-value-is-derived-by-the-engine-from-a-real.md) (default)
<a id="D5"></a>
- `D5` to [DOC-DATAENG-008](doctrines/DOC-DATAENG-008-one-bounded-window-per-run-sized-so-a-single-window-can.md) (default)
<a id="D6"></a>
- `D6` to [DOC-DATAENG-009](doctrines/DOC-DATAENG-009-start-in-batch-move-a-step-to-streaming-only-when-a.md) (default)
<a id="D7"></a>
- `D7` to [DOC-DATAENG-010](doctrines/DOC-DATAENG-010-every-run-records-its-window-the-input-position-it-read.md) (default)
<a id="D8"></a>
- `D8` to [DOC-DATAENG-011](doctrines/DOC-DATAENG-011-rejected-and-very-late-records-go-to-a-quarantine-table.md) (default)
- source `preferences:001` to [DOC-DATAENG-012](doctrines/DOC-DATAENG-012-the-table-format.md) (preference)
- source `preferences:002` to [DOC-DATAENG-013](doctrines/DOC-DATAENG-013-whether-the-merge-key-is-the-sources-natural-key-or-a.md) (preference)
- source `preferences:003` to [DOC-DATAENG-014](doctrines/DOC-DATAENG-014-the-orchestrator-and-whether-the-window-arrives-as-a-cli.md) (preference)
- source `preferences:004` to [DOC-DATAENG-015](doctrines/DOC-DATAENG-015-compaction-cadence-and-small-file-policy-until-the-read.md) (preference)
- source `preferences:005` to [DOC-DATAENG-016](doctrines/DOC-DATAENG-016-whether-quarantine-is-a-table-per-source-or-one-table.md) (preference)

## Decision map

The material forks, each argued in a Wargame.

| Fork | Wargame | Default |
| --- | --- | --- |
| How does the data get here: batch, stream or change capture | `packs/data-engineering/wargames/WG-DATAENG-001-ingestion-shape.md` | Scheduled batch, change capture where the log is readable |
| How is a reprocess made idempotent | `packs/data-engineering/wargames/WG-DATAENG-002-idempotent-reprocess.md` | Replace a bounded unit |
| Where does the processing date come from | `packs/data-engineering/wargames/WG-DATAENG-003-processing-window.md` | The scheduler's interval, or the event time in the data |
| How are late and out-of-order arrivals handled | `packs/data-engineering/wargames/WG-DATAENG-004-late-arrivals.md` | A declared lookback, with a quarantine beyond it |

Level-three detail sits in `packs/data-engineering/references/`: the per-hop
guarantee table, the run ledger fields, and partition choice and
evolution. A full worked application is in
`packs/data-engineering/examples/EX-DATAENG-001-orders-backfill.md`.
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
source found. WG-DATAENG-002 argues it from mechanism, which is weaker
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
