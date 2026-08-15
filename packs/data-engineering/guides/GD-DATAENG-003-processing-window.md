---
summary: The run's own clock, the scheduler's interval, a high-water mark read from the target, or the event time carried in the record?
type: guide
tags: [data, ops, state]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2028-02
sources: [pending-import]
---

# GD-DATAENG-003: where does the processing date come from?

## The question

Every scheduled run has to decide which rows are its business. That
decision is a date or a pair of dates, and where those dates come from
is the fork. It looks like plumbing and it is the difference between a
pipeline that can be rerun and one that cannot.

The wall clock is one of the options below and it is the wrong one. It
is listed because it is what a pipeline does by default when nobody
rules, and because the argument against it has to be available at the
moment somebody reaches for it.

## It depends on

- Whether an orchestrator exists that owns a schedule, or whether the
  job is a cron line and a script.
- Whether records carry a time of occurrence at all, or only a time of
  arrival.
- Whether the source can hand back the same range twice and mean it.
- Whether more than one run may be in flight at once.
- Whether history has to be loaded, because a mechanism that cannot
  express an old window cannot backfill.

## Options

### A. The run's own clock

*What it is.* The job asks the machine what time it is and derives its
window from that: yesterday, the last hour, since midnight.

*Buys.* Nothing that the others do not, which is the point of listing
it. It needs no configuration and no orchestrator.

*Costs.* The window is a function of when the process started, so a
rerun of Tuesday's failed job on Thursday processes Thursday and Tuesday
stays broken. Backfill is impossible without editing the code. The
orchestrator's best-practice documentation puts the current-time call
out of bounds inside a task, and most firmly out of bounds in the
arithmetic that matters. The table format's partitioning documentation
supplies the sharpest version of the failure: using the processing time
in place of the event time to derive a partition value lands a wrong
answer while every query keeps succeeding.

### B. The scheduler's interval, passed in

*What it is.* The orchestrator owns the schedule, computes the interval
each run covers, and hands it to the task as a parameter. The task uses
nothing else.

*Buys.* A rerun of a past interval reprocesses that interval, because
the interval is an input rather than a discovery. Backfill is the same
code with different dates, which is D2 in
`packs/data-engineering/PACK.md`. Two runs can be in flight over
different windows without racing.

*Costs.* Needs an orchestrator, and ties the pipeline to that
orchestrator's model of time, which has changed across major versions of
the ones in common use. A manually triggered run may carry an interval
that is not what the operator meant, so the task should take the window
it is given rather than reconstructing it.

### C. A high-water mark read from the target

*What it is.* The run asks its own output what the latest value it holds
is, and processes everything after that.

*Buys.* Works with no orchestrator at all. Self-healing after a missed
run, because the gap is visible in the mark.

*Costs.* The window is derived from state, so the same code produces
different windows depending on what ran before, and reprocessing a
period in the middle of history means lying to the mark. Two concurrent
runs read the same mark and do the same work. A partially failed run
leaves the mark and the data disagreeing, and which one is right is not
recorded anywhere.

### D. The event time carried in the record

*What it is.* The window is declared over a column in the data that says
when the thing happened. Configuration names the column, the batch
width, and how far back history begins; the tool derives each batch.

*Buys.* The window means what a reader thinks it means, because it is a
property of the data rather than of the run. Backfill is a start date
and an end date. The microbatch documentation is this option written
down as configuration.

*Costs.* Requires a trustworthy occurrence time in the records, and
every upstream input has to declare its own or the read cannot be
narrowed and each batch scans everything. Silent about arrival: a record
that shows up a week late belongs to an old window and will not be
picked up unless the lateness policy says so, which is
`packs/data-engineering/guides/GD-DATAENG-004-late-arrivals.md`.

## Decision rule

Records carry a usable occurrence time and the transform tool supports
declaring it: D. An orchestrator owns the schedule and the records carry
only arrival time: B, with the interval passed in and the task
forbidden from consulting a clock. No orchestrator and no occurrence
time: C, with the mark stored beside the output, written in the same
commit as the data it describes, and a documented procedure for
reprocessing an interior period. A: never, and the pack's D1 says so.

Whichever is chosen, the window that ran is written into the run ledger
in `packs/data-engineering/refs/RUN_LEDGER.md`, because a window nobody
recorded cannot be argued about afterwards.

## Default

D where the data supports it, B otherwise.

## Why this is a default and not a requirement

It prevents a serious and quiet corruption, which is the first limb of
the ADR-0008 test, and its basis is two maintainer documents rather than
a law, a standard or a measurement, which fails the second. Rather than
inflate the basis to keep the authority, it is D1 in
`packs/data-engineering/PACK.md` and the open questions there record
that it is the rule the pack would most like to bind.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: D preferred, B accepted, C
  admitted for a venture with no orchestrator, A refused. The refusal is
  worth stating as a refusal rather than as a preference, because A is
  what a pipeline does when nobody decides.
- **Worked application**:
  `packs/data-engineering/exemplars/EX-DATAENG-001-orders-backfill.md`
  takes B for the extract, where only arrival time exists, and D for the
  transform, where the order's own timestamp does.
