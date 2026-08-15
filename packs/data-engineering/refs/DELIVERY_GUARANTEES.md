---
summary: What a hop is, the three guarantees, what each sink type can actually promise, and the fields that record a hop
type: implementation
tags: [data, ops, state]
kind: recipe
scope: estate
review: 2028-05
sources: [pending-import]
---

# Delivery guarantees, per hop

Level-3 reference for binding requirement B1 in
`packs/data-engineering/PACK.md`. A guarantee is never a property of a
pipeline. It is a property of one hop between two named systems, and a
pipeline's real guarantee is the weakest hop in it.

## What counts as a hop

Two systems and the movement of records between them, where a failure
between the read and the write is possible. Draw them before arguing
about them. A four-box pipeline usually has three hops, and the one
people forget is the last, from the transform into the table people
read.

## The three guarantees, stated usefully

| Guarantee | What it means at this hop | What it costs downstream |
| --- | --- | --- |
| At most once | Records may be lost, never repeated. Position is saved before the work. | Silent loss. Nothing downstream can detect it. |
| At least once | Records are never lost, may be repeated. Position is saved after the work. | The sink must be able to absorb a repeat. |
| Exactly once | Position and output move together, or not at all. | Only available where the sink takes part. |

The broker's delivery-semantics documentation makes the first two a
consequence of the order of two lines of code: save the position, then
work, gives at most once; work, then save the position, gives at least
once. That is worth knowing because it means a hop's guarantee is
usually decided by accident.

## What a sink can actually promise

| Sink | Best available | Why |
| --- | --- | --- |
| The same broker's topic | Exactly once | Position and output commit in one transaction. |
| A table with a unique key and a merge | Effectively exactly once | A repeat updates the row it already wrote. |
| A table replaced whole per window | Effectively exactly once | The second write overwrites the first. |
| A store taking part in two-phase commit | Exactly once | The engine and the store agree on the commit. |
| A store holding the position beside the output | Exactly once | Both move in one write, so neither can lead. |
| An appending table with no key | At least once | Nothing distinguishes the second copy. |
| An HTTP endpoint or a file drop | At least once | No transaction, no key, no position. |

The stream processor's checkpointing documentation is the source for
rows four and five: the engine's own exactly-once setting is about its
state and its stream positions, and carrying that outward needs the sink
to take part, either transactionally or by being unchanged when the same
write happens twice.

## The claim to refuse

An exactly-once claim on a feature list, applied to a whole pipeline.
The broker's own documentation says such claims need their fine print
read because they usually assume nobody fails. The change-capture
project's exactly-once page goes further about the mechanism everyone
builds on: it says it cannot tell whether the implementation is correct
in every case, that no thorough analysis of it exists, that independent
testing of other systems speaking the same protocol raised correctness
concerns, and that protocol issues are open.

The safe position costs nothing: assume at-least-once, make the sink
idempotent, and treat any exactly-once claim as a bonus that changes no
design decision.

## The fields that record a hop

One row per hop in the change record or the pipeline's own
documentation. All six are facts, not judgements.

| Field | Example value |
| --- | --- |
| `from` | `vendor-orders-api` |
| `to` | `landing.orders_raw` |
| `guarantee` | `at-least-once` |
| `sink_idempotence` | `partition-replace` |
| `dedupe_key` | `null` |
| `position_store` | `run_ledger.high_water_mark` |

`sink_idempotence` takes one of `partition-replace`, `merge-on-key`,
`append-with-view`, `write-token` or `none`. A hop whose guarantee is
`at-least-once` and whose `sink_idempotence` is `none` is the finding.
That pair is what C3 in `packs/data-engineering/CHECKS.md` looks for.
