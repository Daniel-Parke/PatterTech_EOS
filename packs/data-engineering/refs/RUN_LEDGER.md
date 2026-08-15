---
summary: The fields a pipeline run records, what each one is for, and the two comparisons that make the ledger worth keeping
type: implementation
tags: [data, ops, tooling]
kind: recipe
scope: estate
review: 2028-07
sources: [pending-import]
---

# The run ledger

Level-3 reference for default D7 in `packs/data-engineering/PACK.md`.
One row per pipeline run, written by the pipeline, in a table or a file
beside the output. It exists so that three questions have answers
without anybody reading logs: which window did this run cover, what did
it read up to, and did anything go missing or double.

## The fields

| Field | Type | What it is for |
| --- | --- | --- |
| `run_id` | string | Ties the row to the orchestrator's own record. |
| `pipeline` | string | Which pipeline. One name, stable across versions. |
| `window_start` | timestamp | Inclusive start of the period this run claimed. |
| `window_end` | timestamp | Exclusive end. Half-open, always, so two windows cannot both own a boundary row. |
| `window_source` | enum | `scheduler`, `event-time`, `high-water-mark`. Never `clock`. |
| `high_water_mark_in` | string | The input position read up to: a log position, a modified-at value, an offset. |
| `rows_in` | integer | Records read. |
| `rows_out` | integer | Records written. |
| `rows_quarantined` | integer | Records that missed the lateness horizon or failed validation. |
| `strategy` | enum | `partition-replace`, `merge-on-key`, `append-with-view`, `write-token`. |
| `code_version` | string | Commit of the code that ran. |
| `started_at` | timestamp | Wall clock, and the only place in the pipeline where a wall clock is allowed. |
| `result` | enum | `pass`, `fail`, `partial`. |

`window_source` carrying `clock` is not an enum value, because a
pipeline that could write it is one D1 already refused. If a run cannot
name where its window came from, that is the finding.

## The two comparisons

The fields exist for these, and a ledger nobody compares is storage.

**Reconciliation.** `rows_in` against `rows_out` plus
`rows_quarantined`, per run. A gap is either a filter nobody documented
or a loss nobody noticed, and the ledger cannot tell you which, only
that one of them happened.

**Rerun equality.** Rerun a past window and compare the new row against
the old one. Same `window_start` and `window_end`, same `rows_out`, and
the same table afterwards, is what B2 in
`packs/data-engineering/PACK.md` claims and what C1 in
`packs/data-engineering/CHECKS.md` proves. A `rows_out` that changed on
a rerun with the same input is either a non-idempotent write or a
non-deterministic transform, and both are defects.

## What it is not

Not observability, not a metrics store, and not a place for durations
and costs. Those belong to
`packs/devops-reliability/refs/SLO_AND_ERROR_BUDGET.md` and are a
different question from whether the data is right. Not an audit table
for the records themselves: the quarantine holds payloads, the ledger
holds counts.

## The smallest honest version

A venture with one pipeline and no warehouse can satisfy this with a
JSON file per run in an object store, keyed by run id. Thirteen fields
written by the function that already knows all of them. The point is
that the window and the mark are recorded at all, not the shape of the
thing recording them.
