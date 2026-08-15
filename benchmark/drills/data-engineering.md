---
summary: Single-run cold-agent acceptance drill for the data-engineering pack, testing idempotent reprocessing, backfill, and late and duplicate records
type: example
tags: [eos]
---

# Drill: backfill three months without double-counting

## Scenario

A cold agent is given the `data-engineering` pack and a seeded fixture
repository holding a nightly ingest job that has been running since
1 May 2026. One run, no human turns.

The tree:

- `pipeline/run_daily.py`, the entry point the scheduler calls. It takes
  no arguments today.
- `pipeline/ingest.py`, which chooses the landing files to read. It
  calls `date.today()` to work out which drop is the current one.
- `pipeline/transform.py`, which derives `units` and `net_pence` for
  each order.
- `pipeline/load.py`, which appends the day's aggregate to the table.
- `landing/orders/`, ninety-two daily drops from `2026-05-01.jsonl` to
  `2026-07-31.jsonl`, two to four order rows each, about two hundred and
  seventy rows in all. Each row carries `order_id`, `order_date`,
  `quantity`, `net_pence` and `updated_at`. The whole tree is under a
  hundred kilobytes.
- `warehouse/orders_daily.csv`, the table as the nightly job has left
  it: columns `order_date`, `orders`, `units`, `net_pence`, one row per
  date.
- `pyproject.toml` and `docs/PIPELINE.md`.

Four things are planted, and the change request names only the first.

1. `pipeline/transform.py` counts a returned unit as a sold one. It
   takes the absolute value of `quantity`, so a return of two units adds
   two instead of taking two away. Returns sit in the drops for 22 May,
   18 June and 6 July.
2. The drop for 17 May carries an order whose `order_date` is 14 May. It
   arrived three days late and belongs to the fourteenth.
3. An order appears in the drop for 9 June and again in the drop for
   11 June, corrected, with a later `updated_at`. Both copies carry an
   `order_date` of 9 June.
4. `pipeline/load.py` appends. Nothing in the job makes a second run of
   the same day replace the first.

`TASK.md` holds the change request:

> The nightly job has been counting returns as sales since 1 May. Fix
> the transform and reprocess 1 May to 31 July inclusive so the table is
> right. Keep `pipeline/run_daily.py` as the entry point and give it a
> `--date YYYY-MM-DD` argument, because that is how our scheduler calls
> it and how we will ask for a day to be redone. The scheduler always
> passes the date, so the job never has to work out which day it is.
> Keep `pipeline/ingest.py` as the module that chooses input and
> `pipeline/transform.py` as the module that derives values. Keep the
> table at `warehouse/orders_daily.csv` with the columns it has now.

## Deterministic pass criteria

Every check must return true. Each is a file existence, exit code or
parse assertion, no judgement.

1. From a clean copy of the fixture,
   `python pipeline/run_daily.py --date 2026-06-02` exits 0, and the
   same command with no `--date` exits non-zero. The partition is an
   argument, never a default.
2. **Prohibition.** No wall-clock read survives in `pipeline/ingest.py`
   or `pipeline/transform.py`. Both files return zero matches for
   `datetime.now`, `datetime.utcnow`, `date.today`, `time.time`,
   `Timestamp.now` and `pendulum.now`. The change request keeps those
   two modules in their roles, so a clock read in either is a job that
   cannot be asked for a day other than the one it is run on.
3. The ninety-two dates run in the fixed shuffled order stored with this
   drill produce the same parsed rows as the same dates run in ascending
   order, compared after sorting by `order_date`. A job whose answer
   depends on the order its partitions are processed in is carrying
   state the partition key does not name.
4. After the ascending pass, running `--date 2026-05-14`,
   `--date 2026-06-09` and `--date 2026-07-06` four times each leaves
   the parsed table unchanged. The write replaces its partition rather
   than adding to it.
5. `warehouse/orders_daily.csv` parses, holds exactly ninety-two rows,
   carries every date from 2026-05-01 to 2026-07-31 inclusive exactly
   once, and carries no date outside that range.
6. `units` for 2026-05-22, 2026-06-18 and 2026-07-06 equal the reference
   aggregate stored with the graders, in which returned quantity is
   subtracted. The shipped fixture is higher than the reference on all
   three dates, so this criterion cannot pass on an untouched tree.
7. The row for 2026-05-14 equals the reference on `orders`, `units` and
   `net_pence`, counting the order that arrived in the 17 May drop, and
   the row for 2026-05-17 excludes that order.
8. The row for 2026-06-09 equals the reference on `orders`, `units` and
   `net_pence`: the twice-sent order counted once, at the quantity
   carried by the copy with the later `updated_at`.
9. **Prohibition.** Nothing under `landing/` changes. The file list and
   the sha256 of every file match the capture taken before criterion 1,
   after every command in criteria 1 to 8 has run. A pipeline that
   repairs its own source cannot be reprocessed a second time.
10. **Prohibition.** No broker or stream-processing requirement appears
    in `pyproject.toml`. Zero case-insensitive matches for kafka,
    pulsar, flink, beam, faust and spark. A daily batch handed a
    backfill request stays a daily batch.
11. `warehouse/orders_daily.csv` is deleted, all ninety-two dates are
    run in ascending order with the delivered code, and the result
    parses to the same rows as the table the agent delivered. The table
    came from the pipeline and not from an editor.

## Scoring

11 binary checks, pass threshold 11 of 11. Partial credit is recorded
for diagnosis only and is not a pass.

## Fail conditions worth logging separately

- 1 and 5 pass, 4 fails: the agent gave the job a date and left the
  append, so a rerun doubles the day. This is the failure a backfill
  produces most often.
- 2 fails and everything else passes: the answer is right for the run
  that produced it and cannot be asked for any other day. Worth logging
  on its own, because nothing in the output shows it.
- 6 passes and 7 fails: the named bug was fixed and the record that
  arrived late was dropped without a word.

## What this drill does not test

Nothing here asks what a number means. There is no metric definition,
no event taxonomy, no data contract, no experiment and no question about
what the analytics layer may hold about a person. Those sit in
`packs/data-analytics/PACK.md` and its own drill grades them. Criterion
5 counts partitions and does not read a declared grain: a tree that
states its grain in words and still double-counts fails it, and a tree
that states nothing and reprocesses correctly passes.

## Freeze note

Criteria 1 to 11 are frozen before any `data-engineering` pack content
is authored. `registry/coverage.json` carries the capability as
registry-only on the day this was written, so the spec cannot have been
written to suit a pack, and `frozen_before_authoring` is true in
`benchmark/drills/MANIFEST.json`. The ninety-two drops, the three return
dates, the 14 May late arrival, the 9 June re-send, the fixed shuffled
order and the reference aggregate are fixed inputs stored with the
drill. The reference aggregate is never materialised into the agent's
tree.
