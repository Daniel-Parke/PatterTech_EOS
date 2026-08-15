---
summary: Research synthesis for the data-engineering pack, covering ingestion shape, delivery guarantees, idempotent reprocessing, the processing window, late arrivals and partitioning
type: example
tags: [eos]
---

# Data engineering: what the evidence actually supports

Research cutoff 2026-08-15. Twelve sources in `sources.fragment.json`,
all fetched on 2026-08-15, all primary: two protocol and format
specifications, eight maintainer documentation sets, one peer-reviewed
model paper, and one maintainer page whose whole content is a warning
about its own strongest feature.

The subject is how bytes arrive and how they are reprocessed. What a
number means, how an event is named, how an experiment ends and what the
analytics layer may hold about a person all belong to
`packs/data-analytics/PACK.md` and are not re-argued here.

## Three materially different philosophies

**1. Scheduled batch over a bounded window.** The pipeline wakes on a
schedule, claims a window of time, reads everything in it, and writes a
result for that window. Reprocessing is rerunning the same code with the
same window. It fits anything whose consumers read on a human cadence,
which is nearly every venture. The trade is latency measured in the
schedule interval, and the failure is a window boundary taken from the
machine's clock rather than from the schedule, which makes a rerun
process a different set of rows from the original (FRAG-DATA-ENGINEERING-09).

**2. Continuous stream with an event-time clock.** Records are consumed
as they arrive, grouped by when they happened rather than when they were
seen, and results are emitted when a progress marker says the group is
probably complete. It fits a decision that cannot wait for the next run.
The trade is that completeness is never known: the marker can be too
fast, in which case records arrive behind it, or too slow, in which case
one straggler delays everything (FRAG-DATA-ENGINEERING-04). Both
directions are named in the peer-reviewed source and both bite.

**3. Change data capture from the source's own log.** Rather than asking
the source what changed, read the log it already writes. This is the
only one of the three that reliably sees a delete, sees a row that
changed twice between polls, and needs no column added to the source
(FRAG-DATA-ENGINEERING-05). The trade is a position that must survive
restarts, a snapshot for the history the log no longer holds, and a
process to operate rather than a job to schedule.

The three are not exclusive. The common estate shape is change capture
or batch extract into a landing area, then a scheduled batch transform
over bounded windows, with streaming used only where a named decision
cannot wait.

## The delivery-guarantee question, which the marketing gets wrong

This is where the sources are most useful and most at odds with the
surrounding industry noise.

The broker's own documentation says the quiet part first: exactly-once
claims elsewhere need their fine print read, because they usually assume
nobody fails (FRAG-DATA-ENGINEERING-01). It then scopes its own to the
case it can actually cover, reading from the log and writing back to the
log, where the consumer's position is committed inside the same
transaction as the output. Write anywhere else and the choice is a
two-phase commit the sink probably does not support, or storing the
position in the same place as the output so both move together. Absent
either, the guarantee is at-least-once.

The stream processor says the same from the other side
(FRAG-DATA-ENGINEERING-03). Its exactly-once setting is about its own
state and its own stream positions. Carrying that to an external system
needs the sink to take part, by transaction or by being unchanged when
the same write happens twice.

The change-capture project goes furthest and is the most valuable
counter-evidence in the set (FRAG-DATA-ENGINEERING-06). It provides
at-least-once, has no deduplication of its own, and says it cannot tell
whether the underlying transaction implementation is correct in every
case, that no thorough analysis exists, that independent testing of other
systems speaking the same protocol raised correctness concerns, and that
several protocol issues are open. It carries a warning box saying so.
A maintainer publishing that about the feature everyone else sells as
solved is the strongest single reason the pack refuses to let a pipeline
rest on an exactly-once claim.

So the position the pack takes: assume at-least-once everywhere, make
the sink idempotent, and treat any exactly-once claim as a property of
one hop between two named systems rather than of the pipeline.

## Idempotent reprocessing has three real mechanisms

Not one, and the choice has costs the sources state plainly
(FRAG-DATA-ENGINEERING-11).

- **Replace a bounded unit.** Delete the window and write it again, or
  overwrite the partition. Cheapest, needs the table partitioned on the
  thing being corrected, and breaks when a correction moves a row from
  one partition to another.
- **Merge on a declared key.** Update what matches, insert what does
  not. Safest and most expensive, because deciding what matches means
  reading the destination. The documentation is explicit that the value
  of the strategy is the reliability of the key, and that a merge with
  no key degrades into an append without saying so.
- **Append only, with a view that picks the winner.** Keep every version
  and resolve at read time. Cheapest to write, and it pushes the cost
  and the correctness onto every reader.

A fourth mechanism exists for the case where the rows have no natural
key at all: make the write itself idempotent with an application
identifier and an increasing version, so a repeat of the same logical
write is ignored (FRAG-DATA-ENGINEERING-12). The same page names the
failure honestly: reuse the identifier after resetting the counter and
the table silently swallows good writes.

The atomic primitive underneath all of this is the metadata pointer swap
described in the table format specification (FRAG-DATA-ENGINEERING-07):
a commit is one swap, readers keep the snapshot they started with, and a
writer that lost a race retries against the new current version. Without
something of that shape, "replace the partition" is a delete followed by
an insert with a window in the middle where the table is wrong.

## Where the processing date comes from

Two sources converge on this and neither is arguing about the other.

The orchestrator's documentation puts the current-time call out of
bounds inside a task, and most firmly out of bounds in the arithmetic
that matters, and says a task should read and write a named window
rather than whatever the source happens to hold at that moment, because
the input can change between runs (FRAG-DATA-ENGINEERING-09). The transformation framework encodes
the same idea as configuration: declare which column carries the time
the event happened, declare how wide a batch is, and let the tool derive
the window (FRAG-DATA-ENGINEERING-10).

The table format documentation supplies the failure this prevents, and
it is the best sentence found in the whole sweep: when the writer
supplies the partition value, using the wrong source column, and it
names the processing time in place of the event time as exactly that
mistake, lands a wrong answer while every query keeps succeeding
(FRAG-DATA-ENGINEERING-08). Wrong format and wrong time zone are in the
same list. Nothing catches any of them.

That is why the rule is not "prefer the data interval". It is that the
wall clock is a defect, because the answer it produces is wrong in a way
no check downstream can see.

## Late and out-of-order arrivals

The peer-reviewed source is the one that makes this a design decision
rather than a bug report (FRAG-DATA-ENGINEERING-04). Completeness is
never known. A progress marker has two failure directions rather than
one, and a pipeline that trusts it alone is knowingly lossy in the first
direction and knowingly slow in the second. The stream processor turns
this into two knobs, an allowed lateness and a route for what arrives
after it (FRAG-DATA-ENGINEERING-02); the transformation framework turns
it into one, a lookback of N batches on every ordinary run
(FRAG-DATA-ENGINEERING-10).

The honest reading is that all three answer the same question with a
number nobody can derive for you. So the pack requires the number to be
declared and the destination for the overshoot to be named, and refuses
to pretend there is a right value.

## Partitioning

One source, and it is enough (FRAG-DATA-ENGINEERING-08). A partition
value the writer supplies cannot be checked, so a mistake in it is
silent. A partition value the engine derives from a real column by a
declared transform is correct by construction, and it decouples queries
from the physical layout, which is what makes the layout changeable
later. Evolution is then a metadata change with no rewrite, at the cost
of a table carrying two layouts and planning them separately.

Where hidden partitioning is not available, which is most small
ventures, the transferable rule is that the partition value is derived
in exactly one place in code from the event-time column, and never
written by hand at the call site.

## What was deliberately left to data-analytics

The boundary was tested against every source and held. Left alone:
metric definition and the grain of a fact table, event naming and the
tracking plan, quality gates as a publication gate, experiment
statistics, and the lawful basis for any column that identifies a
person. Where the two meet, this pack stops at the point where correct
bytes have landed in a correct partition, and the other starts at the
point where somebody asks what the number means.

## Predicates proposed

The vocabulary in `kernel/PREDICATES.md` is integrator-owned, so these
are proposals. Check S021 will fail on all four until they are added,
which is expected. Each one was tested against the existing rows first.

| Proposed | True when | Settled by |
| --- | --- | --- |
| `ingests_external_data` | the venture takes data in from a system it does not own, by pull, subscription or change feed, and lands it somewhere of its own | 17 |
| `runs_scheduled_pipeline` | data processing runs on a schedule or a trigger rather than in response to a user request | 18 |
| `processes_event_time_data` | records carry a time at which the thing happened, distinct from the time they arrived | 18 |
| `reprocesses_data` | the work reruns a period that has already been processed: a retry, a correction or a backfill | task |

Why each is new rather than an existing row:

- `ingests_external_data` against `consumes_external_api` (question 17,
  api-integration). Calling somebody's service is a request and a
  response inside a user-facing path; ingesting is a recurring transfer
  that lands and accumulates. A venture can be true on one and false on
  the other in both directions, and the pack that should load differs.
  If the integrator judges them one fact, this pack should take the
  existing spelling rather than add a second.
- `runs_scheduled_pipeline` against `deploys_to_environment` and
  `stores_persistent_data` (devops-reliability). Those are about
  something running and something surviving; neither says work happens
  on a cadence against a window, which is the fact that makes the
  window-boundary rules apply at all.
- `processes_event_time_data` against `models_time` (question 18,
  business-logic-modelling). That row is about dates and durations
  carrying business meaning, a domain-modelling fact. This one is about
  two clocks disagreeing in a pipeline, and it is what turns on the
  lateness horizon.
- `reprocesses_data` against `runs_schema_migrations` (task,
  devops-reliability). That is the shape of stored data changing. This
  is the same shape being rewritten with different contents.

Reused unchanged: `stores_persistent_data`, question 6, for the landing
store. Nothing here needs a new spelling of it.

## Evidence ids and how the read surface cites

The fragment ids above are the pack-local namespace. The read surface
carries no fragment ids, because check S014 fails them there, and it
carries no evidence ids either, because the import that assigns them has
not run and inventing one would be worse than naming the source. Until
the integrator imports, the pack cites by the short labels below, and
the front-matter `sources` field reads `pending-import`.

| Label used in the read surface | Fragment |
| --- | --- |
| the broker's delivery-semantics documentation | FRAG-DATA-ENGINEERING-01 |
| the stream processor's time documentation | FRAG-DATA-ENGINEERING-02 |
| the stream processor's checkpointing documentation | FRAG-DATA-ENGINEERING-03 |
| the streaming model paper | FRAG-DATA-ENGINEERING-04 |
| the change-capture project's feature documentation | FRAG-DATA-ENGINEERING-05 |
| the change-capture project's exactly-once page | FRAG-DATA-ENGINEERING-06 |
| the table format specification | FRAG-DATA-ENGINEERING-07 |
| the table format's partitioning documentation | FRAG-DATA-ENGINEERING-08 |
| the orchestrator's best-practice documentation | FRAG-DATA-ENGINEERING-09 |
| the microbatch documentation | FRAG-DATA-ENGINEERING-10 |
| the incremental-strategy documentation | FRAG-DATA-ENGINEERING-11 |
| the idempotent-write documentation | FRAG-DATA-ENGINEERING-12 |

## What the sweep did not find

- No study comparing partition replacement against merge for
  correctness or cost at any scale, let alone a venture's.
- No published figure for how much late data a real source produces, so
  every lateness horizon in the pack is declared rather than derived.
- No independent analysis of the correctness of the transaction
  protocol that all the exactly-once claims rest on. The
  change-capture project says so itself.
- No source written for a one or two person venture. Every one assumes
  a data team, which is the same gap `packs/data-analytics/PACK.md`
  records.

No page fetched during this sweep carried text addressed to an agent,
and nothing was installed, run or followed. All twelve were read as
documents.


## Integrator note, 2026-08-15

`stores_persistent_data` was proposed for reuse and is removed from
`applies_when`. It is true of every venture with a database, and the
activation corpus in `tests/fixtures/activation/profiles.json` showed
the cost: with it declared, this pack activated for the SaaS and the
public API archetypes, neither of which is a data-engineering venture.
The four remaining predicates carry the real trigger, and the batch
pipeline archetype still activates on them. The predicate stays where
it belongs, with devops-reliability.
