---
id: GD-DATAENG-004
summary: Drop at the watermark, hold the window open and restate, reprocess a fixed lookback every run, or recompute everything?
kind: wargame
type: wargame
tags: [data, eos, ops, realtime, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DATAENG-003]
applies_when: [processes_event_time_data]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [pending-import]
review: 2028-03
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DATAENG-004: how are late and out-of-order arrivals handled?

## Decision question and stakes

A record for Tuesday arrives on Thursday. A phone was offline, a
retrying webhook got through, a source replayed a day, a consumer
lagged. The fork is what the pipeline does with it, and it has to be
answered before anybody asks, because the default answer is to throw it
away without a line in a log.

The premise is where the peer-reviewed source earns its place:
completeness is never known, so every option below is a choice about
which error to accept.

## Doctrines or coverage gap under pressure

- `DOC-DATAENG-003` (binding): A pipeline over event-time data declares its lateness horizon and where arrivals past it go. Nothing is dropped silently.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- The observed lateness of this source, which almost nobody has
  measured, and which is the first thing to go and look at.
- Whether a consumer has already acted on that period's answer.
  Restating a number somebody invoiced against is not restating a chart.
- Whether the store can rewrite a past period cheaply, which is
  `packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md`.
- Whether the pipeline is a stream holding windows in memory, or a batch
  that can simply be rerun.

Applicability is `processes_event_time_data`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Drop at the progress marker

Assume `A. Drop at the progress marker` was selected and the outcome failed. Test this option's stated failure mechanism first: , and a single answer per period that never changes.

### Premortem for B. Hold the window open, then restate

Assume `B. Hold the window open, then restate` was selected and the outcome failed. Test this option's stated failure mechanism first: * Every downstream consumer must accept a revised number, which is a contract rather than a setting. State is held for the whole allowance, so cost scales with how generous it is, and the tail is still a guess.

### Premortem for C. Reprocess a fixed lookback every run

Assume `C. Reprocess a fixed lookback every run` was selected and the outcome failed. Test this option's stated failure mechanism first: * Cost is multiplied by N on every run, for ever, whether or not anything was late. Anything later than N windows is silently missed, so this is option A with a longer fuse unless it is paired with a quarantine. The default value of N in the tooling is a guess, not a finding.

### Premortem for D. Recompute from the beginning

Assume `D. Recompute from the beginning` was selected and the outcome failed. Test this option's stated failure mechanism first: * Cost grows with history rather than with change, so it has a cliff that arrives without warning. It rewrites periods nobody asked about, which makes a downstream snapshot or audit trail harder to trust.

### Premortem for E. Quarantine and count

Assume `E. Quarantine and count` was selected and the outcome failed. Test this option's stated failure mechanism first: * A table to keep, and somebody has to look at it. An unread quarantine is a drop with extra storage.

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

## Safe default

C with a lookback of one window and a quarantine, revised upward once
the quarantine has a month of evidence in it. Start with the tooling's
default only because a declared guess beats an undeclared one, and
replace it with a measurement as soon as there is one.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **The observed lateness of this source, which almost nobody has measured, and which is the first thing to go and look at.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C with a lookback of one window and a quarantine, revised upward once the quarantine has a month of evidence in it. Start with the tooling's default only because a declared guess beats an undeclared one, and replace it with a measurement as soon as there is one.

**Exit condition:** Stop or roll back the selected branch when , and a single answer per period that never changes, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: The observed lateness of this source, which almost nobody has measured, and which is the first thing to go and look at.

## Counter-evidence and transfer limits

### Preserved reasoning: The number nobody has

No published figure was found for how much late data a real source
produces, so every horizon here is declared rather than derived, and
`packs/data-engineering/PACK.md` records that as an open question. The
lookback is a venture fact to be measured locally, and a pipeline
running a month without reading its quarantine has the measurement and
is ignoring it.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
