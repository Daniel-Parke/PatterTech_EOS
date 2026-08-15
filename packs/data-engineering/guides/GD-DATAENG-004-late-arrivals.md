---
summary: Drop at the watermark, hold the window open and restate, reprocess a fixed lookback every run, or recompute everything?
type: guide
tags: [data, ops, realtime]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
review: 2028-03
sources: [pending-import]
---

# GD-DATAENG-004: how are late and out-of-order arrivals handled?

## The question

A record for Tuesday arrives on Thursday. A phone was offline, a
retrying webhook got through, a source replayed a day, a consumer
lagged. The fork is what the pipeline does with it, and it has to be
answered before anybody asks, because the default answer is to throw it
away without a line in a log.

The premise is where the peer-reviewed source earns its place:
completeness is never known, so every option below is a choice about
which error to accept.

## It depends on

- The observed lateness of this source, which almost nobody has
  measured, and which is the first thing to go and look at.
- Whether a consumer has already acted on that period's answer.
  Restating a number somebody invoiced against is not restating a chart.
- Whether the store can rewrite a past period cheaply, which is
  `packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md`.
- Whether the pipeline is a stream holding windows in memory, or a batch
  that can simply be rerun.

## Options

### A. Drop at the progress marker

*What it is.* Emit when the marker passes the end of the window, and
discard whatever turns up afterwards.

*Buys.* Bounded state, bounded cost, and a single answer per period that
never changes.

*Costs.* Knowingly lossy, and the loss is invisible: row counts
reconcile because the record was never counted. The streaming model
paper names both failure directions of the marker, and this option takes
the first one whole. Only defensible with the drop counted.

### B. Hold the window open, then restate

*What it is.* Emit a result when the marker passes, keep the window's
state for a declared allowance, and emit a revision when a late record
lands inside it.

*Buys.* Correct inside the allowance, with a first answer available
immediately. This is what a stream processor's allowed lateness is for.

*Costs.* Every downstream consumer must accept a revised number, which
is a contract rather than a setting. State is held for the whole
allowance, so cost scales with how generous it is, and the tail is still
a guess.

### C. Reprocess a fixed lookback every run

*What it is.* On every ordinary run, reprocess the last N windows as
well as the current one, replacing each.

*Buys.* No streaming machinery, no held state, and it composes exactly
with the replace-a-window strategy. The microbatch documentation ships
this as a single setting. Late records inside the lookback are picked up
without anybody noticing, which is the point.

*Costs.* Cost is multiplied by N on every run, for ever, whether or not
anything was late. Anything later than N windows is silently missed, so
this is option A with a longer fuse unless it is paired with a
quarantine. The default value of N in the tooling is a guess, not a
finding.

### D. Recompute from the beginning

*What it is.* Rebuild the whole table every run.

*Buys.* Correct by construction for any lateness, and the simplest thing
to reason about. For a table of a few million rows it is genuinely the
right answer and it is under-used.

*Costs.* Cost grows with history rather than with change, so it has a
cliff that arrives without warning. It rewrites periods nobody asked
about, which makes a downstream snapshot or audit trail harder to trust.

### E. Quarantine and count

*What it is.* Not a substitute for the others but the thing that has to
sit under whichever is chosen. Records past the horizon land in a table
with the reason, the raw payload and the arrival time, and the count is
visible.

*Buys.* Turns the unknown into a number. After a month it says what the
source's real lateness distribution is, which is the figure no published
source supplies and the only honest way to set the horizon.

*Costs.* A table to keep, and somebody has to look at it. An unread
quarantine is a drop with extra storage.

## Decision rule

Batch pipeline over windows, which is most of them: C with a lookback
argued from the quarantine's numbers. Table small enough that a full
rebuild fits the schedule: D, and stop thinking about it until the cliff
is in sight. Streaming pipeline whose consumers can take a revision: B
with a declared allowance. A: only where the drop is counted, which
makes it C with a lookback of zero.

E sits under every one of those, because B3 in
`packs/data-engineering/PACK.md` requires that nothing is dropped
silently and the quarantine is what makes that a fact rather than a
claim.

## Default

C with a lookback of one window and a quarantine, revised upward once
the quarantine has a month of evidence in it. Start with the tooling's
default only because a declared guess beats an undeclared one, and
replace it with a measurement as soon as there is one.

## The number nobody has

No published figure was found for how much late data a real source
produces, so every horizon here is declared rather than derived, and
`packs/data-engineering/PACK.md` records that as an open question. The
lookback is a venture fact to be measured locally, and a pipeline
running a month without reading its quarantine has the measurement and
is ignoring it.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C plus E as the estate default,
  D named as legitimately correct for small tables rather than as a
  naive option, and A refused unless the drop is counted, at which point
  it stops being A.
- **Worked application**:
  `packs/data-engineering/exemplars/EX-DATAENG-001-orders-backfill.md`
  runs C with a three-day lookback, set from a quarantine that had been
  collecting for five weeks.
