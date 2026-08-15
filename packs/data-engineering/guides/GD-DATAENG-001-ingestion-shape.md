---
id: GD-DATAENG-001
summary: Scheduled batch extract, a subscribed stream, log-based change capture, or polling a modified-at column?
kind: wargame
type: wargame
tags: [data, eos, ops, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATAENG-001, DOC-DATAENG-009]
applies_when: [ingests_external_data]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0505, EV-0507, EV-0509, EV-0510]
review: 2027-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DATAENG-001: how does the data get here?

## Decision question and stakes

Something outside the venture holds data the venture needs. The fork is
the mechanism that moves it, and it is ruled before the first row lands,
because afterwards the answer is whatever somebody already built and the
gaps in it become permanent features.

This is not a tooling question. Each option sees a different set of
facts, and two of them cannot see a delete at all.

## Doctrines or coverage gap under pressure

- `DOC-DATAENG-001` (binding): Every hop between two systems states its delivery guarantee, and a sink that is not idempotent or transactional is treated as at-least-once.
- `DOC-DATAENG-009` (default): Start in batch. Move a step to streaming only when a named decision cannot wait for the next run.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether the venture may read the source's replication log. Most
  third-party systems say no, and that ends the argument.
- Whether the source can delete rows, and whether a delete matters
  downstream.
- Whether a row can change twice between two reads.
- How fresh the consumer actually needs the data, as a number, not as
  an adjective.
- Whether anybody will operate a long-running process, or whether the
  venture only has room for jobs that start, finish and exit.
- Whether history exists that the source's log no longer holds.

Applicability is `ingests_external_data`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Scheduled batch extract over a bounded window

*What it is.* On a schedule, ask the source for everything in a named
window, land it, transform it.

*Buys.* The simplest thing that can be reprocessed. The window is the
unit of retry, of backfill and of correctness, and everything else in
this pack composes with it. No process to keep alive.

*Costs.* Latency is the schedule interval. The source has to support a
range query on something, and that something is usually a modified-at
column, which drags option D's problems along with it.

### B. Subscribed stream with an event-time clock

*What it is.* Consume records as they are published, group them by when
they happened, emit when a progress marker says the group is probably
complete.

*Buys.* Latency measured in seconds. Where the source is already a
stream, this avoids inventing a landing area to batch it out of.

*Costs.* Completeness is never known, so the pipeline needs a lateness
policy before it is correct at all, and the streaming model paper's two
watermark failure directions both apply. It adds an always-on process,
a state store and a checkpointing story. Reprocessing means replay, and
replay is only as good as the retention behind it.

### C. Log-based change capture

*What it is.* Read the log the source database already writes, and turn
each entry into a change event carrying the operation, the previous
values where the engine offers them, and the log position.

*Buys.* The only option that reliably sees a delete, sees a row that
changed twice between reads, and needs no column added to the source's
data model. The change-capture project's feature documentation is
explicit on all three. The log position travels with the event, so a
consumer can recognise a repeat.

*Costs.* A recorded position that has to survive restarts, an initial
snapshot for history the log no longer holds, and a process to operate.
After an ungraceful stop it resumes from the last flushed position and
replays whatever came after it, so the target must be idempotent before
this is safe. Needs log access the venture is often not granted.

### D. Polling a modified-at column

*What it is.* Ask the source for rows whose modified-at is greater than
the last high-water mark.

*Buys.* Works against almost any source, including ones that expose
nothing but a table or an API. Needs no privileges anybody will refuse.

*Costs.* Cannot see a delete, so the target keeps rows the source no
longer has, for ever, unless the source owner agrees to a soft-delete
column. Cannot see an intermediate state where a row changed twice
between polls. Depends on the source populating the column correctly on
every write path, including the ones nobody remembered.

## Failure premises

### Premortem for A. Scheduled batch extract over a bounded window

Assume `A. Scheduled batch extract over a bounded window` was selected and the outcome failed. Test this option's stated failure mechanism first: * Latency is the schedule interval. The source has to support a range query on something, and that something is usually a modified-at column, which drags option D's problems along with it.

### Premortem for B. Subscribed stream with an event-time clock

Assume `B. Subscribed stream with an event-time clock` was selected and the outcome failed. Test this option's stated failure mechanism first: * Completeness is never known, so the pipeline needs a lateness policy before it is correct at all, and the streaming model paper's two watermark failure directions both apply. It adds an always-on process, a state store and a checkpointing story. Reprocessing means replay, and replay is only as good as the retention behind it.

### Premortem for C. Log-based change capture

Assume `C. Log-based change capture` was selected and the outcome failed. Test this option's stated failure mechanism first: * A recorded position that has to survive restarts, an initial snapshot for history the log no longer holds, and a process to operate. After an ungraceful stop it resumes from the last flushed position and replays whatever came after it, so the target must be idempotent before this is safe. Needs log access the venture is often not granted.

### Premortem for D. Polling a modified-at column

Assume `D. Polling a modified-at column` was selected and the outcome failed. Test this option's stated failure mechanism first: * Cannot see a delete, so the target keeps rows the source no longer has, for ever, unless the source owner agrees to a soft-delete column. Cannot see an intermediate state where a row changed twice between polls. Depends on the source populating the column correctly on every write path, including the ones nobody remembered.

## Decision rule

Source is a database the venture may read the log of, and deletes or
intermediate states matter: C, landing into a store the scheduled
pipeline then reads in windows. Source is already a stream and the
consumer needs an answer faster than the next scheduled run: B, and the
lateness policy is part of shipping it, not a follow-up. Everything
else: A, with D as the extraction mechanism inside it and the delete
problem written down as a known gap rather than discovered later.

Whichever is chosen, the hop into the venture's own store is
at-least-once until the sink proves otherwise, per B1, and the landing
store is the boundary where that stops being someone else's problem.

## Safe default

A, with C where the log is readable. Batch first is not conservatism: it
is that the window is the unit everything else in this pack is built on,
and a venture that starts with a stream has to build a landing area
later anyway to reprocess anything.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether the venture may read the source's replication log. Most third-party systems say no, and that ends the argument.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with C where the log is readable. Batch first is not conservatism: it is that the window is the unit everything else in this pack is built on, and a venture that starts with a stream has to build a landing area later anyway to reprocess anything.

**Exit condition:** Stop or roll back the selected branch when * Latency is the schedule interval. The source has to support a range query on something, and that something is usually a modified-at column, which drags option D's problems along with it, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether the venture may read the source's replication log. Most third-party systems say no, and that ends the argument.

## Counter-evidence and transfer limits

### Preserved reasoning: What this does not decide

Whether the landed data is modelled as events, and what the events are
called, is `packs/data-analytics/PACK.md`. The shape of the envelope on
the wire, and any webhook contract, is `packs/api-integration/PACK.md`.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
