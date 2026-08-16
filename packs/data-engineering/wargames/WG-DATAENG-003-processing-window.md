---
id: WG-DATAENG-003
summary: The run's own clock, the scheduler's interval, a high-water mark read from the target, or the event time carried in the record?
kind: wargame
type: wargame
tags: [data, eos, ops, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATAENG-005, DOC-DATAENG-004]
applies_when: [ingests_external_data]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0506, EV-0508, EV-0512, EV-0513, EV-0514]
review: 2028-02
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DATAENG-003: where does the processing date come from?

## Decision question and stakes

Every scheduled run has to decide which rows are its business. That
decision is a date or a pair of dates, and where those dates come from
is the fork. It looks like plumbing and it is the difference between a
pipeline that can be rerun and one that cannot.

The wall clock is one of the options below and it is the wrong one. It
is listed because it is what a pipeline does by default when nobody
rules, and because the argument against it has to be available at the
moment somebody reaches for it.

## Doctrines or coverage gap under pressure

- `DOC-DATAENG-005` (default): Backfill is the scheduled pipeline given different dates.
- `DOC-DATAENG-004` (default): The processing window comes from the scheduler or from the data, never from the run's own clock, and it is written down with the output.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether an orchestrator exists that owns a schedule, or whether the
  job is a cron line and a script.
- Whether records carry a time of occurrence at all, or only a time of
  arrival.
- Whether the source can hand back the same range twice and mean it.
- Whether more than one run may be in flight at once.
- Whether history has to be loaded, because a mechanism that cannot
  express an old window cannot backfill.

Applicability is `ingests_external_data`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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
`packs/data-engineering/wargames/WG-DATAENG-004-late-arrivals.md`.

## Failure premises

### Premortem for A. The run's own clock

Assume `A. The run's own clock` was selected and the outcome failed. Test this option's stated failure mechanism first: * The window is a function of when the process started, so a rerun of Tuesday's failed job on Thursday processes Thursday and Tuesday stays broken. Backfill is impossible without editing the code. The orchestrator's best-practice documentation puts the current-time call out of bounds inside a task, and most firmly out of bounds in the arithmetic that matters. The table format's partitioning documentation supplies the sharpest version of the failure: using the processing time in place of the event time to derive a.

### Premortem for B. The scheduler's interval, passed in

Assume `B. The scheduler's interval, passed in` was selected and the outcome failed. Test this option's stated failure mechanism first: * Needs an orchestrator, and ties the pipeline to that orchestrator's model of time, which has changed across major versions of the ones in common use. A manually triggered run may carry an interval that is not what the operator meant, so the task should take the window it is given rather than reconstructing it.

### Premortem for C. A high-water mark read from the target

Assume `C. A high-water mark read from the target` was selected and the outcome failed. Test this option's stated failure mechanism first: * The window is derived from state, so the same code produces different windows depending on what ran before, and reprocessing a period in the middle of history means lying to the mark. Two concurrent runs read the same mark and do the same work. A partially failed run leaves the mark and the data disagreeing, and which one is right is not recorded anywhere.

### Premortem for D. The event time carried in the record

Assume `D. The event time carried in the record` was selected and the outcome failed. Test this option's stated failure mechanism first: * Requires a trustworthy occurrence time in the records, and every upstream input has to declare its own or the read cannot be narrowed and each batch scans everything. Silent about arrival: a record that shows up a week late belongs to an old window and will not be picked up unless the lateness policy says so, which is `packs/data-engineering/wargames/WG-DATAENG-004-late-arrivals.md`.

## Decision rule

Records carry a usable occurrence time and the transform tool supports
declaring it: D. An orchestrator owns the schedule and the records carry
only arrival time: B, with the interval passed in and the task
forbidden from consulting a clock. No orchestrator and no occurrence
time: C, with the mark stored beside the output, written in the same
commit as the data it describes, and a documented procedure for
reprocessing an interior period. A: never, and the pack's D1 says so.

Whichever is chosen, the window that ran is written into the run ledger
in `packs/data-engineering/references/RUN_LEDGER.md`, because a window nobody
recorded cannot be argued about afterwards.

## Safe default

D where the data supports it, B otherwise.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether an orchestrator exists that owns a schedule, or whether the job is a cron line and a script.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** D where the data supports it, B otherwise.

**Exit condition:** Stop or roll back the selected branch when * The window is a function of when the process started, so a rerun of Tuesday's failed job on Thursday processes Thursday and Tuesday stays broken. Backfill is impossible without editing the code. The orchestrator's best-practice documentation puts the current-time call out of bounds inside a task, and most firmly out of bounds in the arithmetic that matters. The table format's partitioning documentation supplies the sharpest version of the failure: using the processing time in place of the event time to derive a, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether an orchestrator exists that owns a schedule, or whether the job is a cron line and a script.

## Counter-evidence and transfer limits

### Preserved reasoning: Why this is a default and not a requirement

It prevents a serious and quiet corruption, which is the first limb of
the ADR-0008 test, and its basis is two maintainer documents rather than
a law, a standard or a measurement, which fails the second. Rather than
inflate the basis to keep the authority, it is D1 in
`packs/data-engineering/PACK.md` and the open questions there record
that it is the rule the pack would most like to bind.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
