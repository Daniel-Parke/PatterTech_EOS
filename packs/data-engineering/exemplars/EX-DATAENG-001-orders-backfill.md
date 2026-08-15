---
summary: Worked example, a nightly orders pipeline from a third-party system, repaired over six weeks of history after a time-zone bug
type: example
tags: [data, ops, state]
kind: exemplar
scope: estate
sources: [pending-import]
---

# EX-DATAENG-001: six weeks of orders, put right

The situation this pack was built for. A venture pulls orders nightly
from a third-party commerce system it does not own, lands them, and
builds a daily orders table other things read. Six weeks ago a change
made the pipeline derive its partition date by formatting the order
timestamp in the machine's local time rather than in UTC, so every order
placed in the last hour of a UK summer day landed in the wrong day. It
was found because a weekly total disagreed with the vendor's own
dashboard by a few orders.

This walks the whole repair, and the redesign that stops it recurring.

## 1. Route the task

The work reruns periods already processed, so `reprocesses_data` is
true, along with `ingests_external_data`, `runs_scheduled_pipeline`,
`processes_event_time_data` and `stores_persistent_data`. The pack
activates on all five.

The repair replaces forty-two days of a production table, which is
production-data handling under `kernel/GUARD_SPEC.md`, and the delete
half of a replace is a deletion whatever it is called. The router in
`kernel/POLICY_SPEC.md` sets the tier; the agent prepares the run and
the operator approves the first destructive step.

## 2. Rule the four forks before touching anything

Ruled in the order the pack argues them, because each one constrains the
next.

| Fork | Ruling | Why |
| --- | --- | --- |
| Ingestion shape (GD-DATAENG-001) | Scheduled batch, extracting by polling a modified-at value | No log access to a third-party system, so option C was never available |
| Reprocessing (GD-DATAENG-002) | Append-only landing, replace-the-partition transform | Landing must stay as received; the transform's correction is scoped by day |
| Processing window (GD-DATAENG-003) | Scheduler interval for the extract, event time for the transform | The extract has only arrival time; the order carries its own timestamp |
| Late arrivals (GD-DATAENG-004) | Three-day lookback plus quarantine | The quarantine had five weeks of evidence in it, and the tail sat at two days |

The delete gap gets written down on the way past: polling cannot see a
cancelled order that the vendor hard-deletes. The vendor sets a status
instead, which is confirmed with them rather than assumed, and the note
goes in the pipeline's documentation as a known limit of the shape.

## 3. Fix the derivation, not the data

The partition date was being formatted at the call site, which is the
pattern D4 refuses. One function now takes the order timestamp and
returns the partition date in UTC, every call site uses it, and it has
its own test with an hour on each side of a British Summer Time
boundary. That test is worth more than the test for the transform,
because the partitioning documentation's point is that a wrong partition
value produces a wrong answer while every query keeps succeeding, so
nothing downstream would ever have caught it.

The repair is deliberately second. Repairing before fixing the
derivation would have rewritten the same defect in newer files.

## 4. Write down the hops before claiming anything about them

Three hops, per `packs/data-engineering/refs/DELIVERY_GUARANTEES.md`.

| from | to | guarantee | sink_idempotence | dedupe_key | position_store |
| --- | --- | --- | --- | --- | --- |
| `vendor-orders-api` | `landing.orders_raw` | at-least-once | append-with-view | `order_id, vendor_updated_at` | `run_ledger.high_water_mark_in` |
| `landing.orders_raw` | `warehouse.orders_daily` | at-least-once | partition-replace | null | `run_ledger.window_end` |
| `warehouse.orders_daily` | `warehouse.orders_lifetime` | at-least-once | merge-on-key | `order_id` | null |

Nothing here claims exactly-once and nothing needs to. The vendor's API
makes no guarantee at all, so the first hop assumes repeats and the
landing table absorbs them by never modifying anything. B1 is satisfied
by the sinks, not by a promise.

The third hop is the case that forces a merge. A cancellation arriving
today moves an order out of the day it was placed in, so a
partition-replace of today would never touch the row sitting in a
partition six weeks back. GD-DATAENG-002 names this as the case where A
loses to B, and the key is confirmed unique with the vendor rather than
assumed from the column name.

## 5. Reprocess by window, through the ordinary path

The backfill is the nightly pipeline with a start date and an end date,
per D2. No script, no notebook.

- Forty-two runs, one per day, each replacing one partition.
- Each run takes its window as a parameter and consults no clock.
- The first run goes to the operator for approval, because it is the
  first destructive step. The remaining forty-one follow the approved
  shape.
- Each writes a run ledger row per
  `packs/data-engineering/refs/RUN_LEDGER.md`, with `window_source` set
  to `event-time` and `strategy` set to `partition-replace`.

The landing table is untouched throughout. That is the whole reason it
is append-only: the repair reads the same raw records the broken run
read, so a disagreement afterwards is a transform defect and cannot be
an extract defect.

## 6. Prove the rerun rather than assert it

Before the forty-two runs, one day already known to be correct is rerun
and its ledger row compared with the original: same window, same
`rows_out`, and the table byte-identical afterwards. That is C1 in
`packs/data-engineering/CHECKS.md`, and it is what makes the other
forty-one runs a repair rather than a second experiment.

After the repair, `rows_in` against `rows_out` plus `rows_quarantined`
reconciles for every one of the forty-two days. Eleven orders moved day,
which matches the count of orders placed in the affected hour, and that
number is written into the change record because a repair whose size
nobody predicted is a repair nobody understands.

## 7. Set the lookback from the quarantine, not from the default

The quarantine table had been collecting for five weeks. Its arrival
delays put the longest genuine late order at just under two days, with
one outlier at nine days that turned out to be a vendor replay rather
than a late order. The lookback goes to three days: two for the observed
tail and one for the schedule's own slack.

This is the only defensible way to set it. The tooling's default of one
prior batch would have missed the second day, and nothing would have
reported that it had, which is the failure B3 exists to prevent.

## What the change record carries

The four rulings with their reasons, the hop table, the run ledger rows
for all forty-three runs including the verification one, the eleven
moved orders, the quarantine evidence behind the three-day lookback, the
delete gap confirmed with the vendor, and the operator's approval of the
first destructive step. Every one of those is a field something can
read.

## Where this could still go wrong

The vendor's modified-at column is trusted, and nothing in the pipeline
can check that it is set on every write path inside a system the venture
cannot see. If the vendor updates a row without touching it, the order
never arrives and no count anywhere reconciles differently, because the
record was never read. That is the permanent cost of the ingestion shape
that was available, and the pipeline's documentation says so rather than
letting the next person discover it.
