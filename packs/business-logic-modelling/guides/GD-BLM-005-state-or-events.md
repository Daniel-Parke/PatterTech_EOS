---
summary: Is the record of truth the current state or the sequence of events?
kind: guide
authority: default
basis: decision
evidence_grade: anecdotal
scope: estate
sources: [EV-0138, EV-0157, EV-0163, EV-0269, EV-0275, EV-0276]
review: 2027-12
type: guide
tags: [arch, data, state]
---

# GD-BLM-005: State or events as the record?

## The question

Whether the durable truth is the current state of a thing or the
sequence of events that produced it. The question gets muddled because
four separate patterns travel under one name, so name which is meant
before arguing: event notification, event-carried state transfer, event
sourcing, and CQRS (EV-0163). This guide is about the third.

## It depends on

- **Whether anyone needs the state as at a past instant.** Not a
  history table, the actual state, rebuilt.
- **Whether decisions must be replayable.** Reprocessing a month of
  billing with a corrected rule is the case that earns it.
- **Whether external effects sit in the flow.** Replay must not re-fire
  them, and that gateway is work (EV-0276).
- **Whether external answers feed decisions.** Replay must not re-read
  them at today's values, so they have to be recorded with the event.
- **Whether the data includes personal data.** An append-only log and
  an erasure obligation are unresolved together by every source here.

## Options

### A. State-stored, with a plain audit log
The row holds the truth; a log records what happened. Buys the simplest
reader, the simplest query and the simplest erasure story. Costs the
ability to rebuild past state cheaply: a log records cheaply and
reconstructs expensively (EV-0275).

### B. State-stored, with domain events published through an outbox
The row holds the truth and the event is a fact published to others,
written in the same transaction as the state change and relayed
afterwards (EV-0157). Buys integration without the divergence between
state and message, and it is what makes the eventual consistency
outside an aggregate boundary honest (EV-0269). Costs an outbox table,
a relay and idempotent consumers, because the pattern buys at-least-once
delivery and nothing more.

### C. Event-sourced aggregate, state as a projection
The events are the record; current state is derived. Buys rebuild,
temporal query and replay. Costs the three named traps: effects on
replay, external reads on replay, and old event shapes that must stay
readable forever or be upgraded deliberately (EV-0276). Also costs
snapshot policy, which the source does not cover.

### D. C, plus separated read models
CQRS on top: writes go to the event stream, reads to purpose-built
projections. Buys read shapes independent of the write model. Costs a
second consistency story that every user-facing feature has to
understand.

## Decision rule

A until something outside the boundary needs to know. Then B, which is
where most venture software stops and which requirement B4 in PACK.md
binds the mechanics of. Choose C only when replay or as-at-past-instant
state is a stated requirement with a named question behind it, never
for audit alone, because a log is cheaper (EV-0276). Choose D only
after C, and only when a read shape genuinely cannot be served from the
projection you already keep.

Whichever is chosen, the event envelope is a wire contract and belongs
to `packs/api-integration/PACK.md` and EV-0138, not to the domain
model.

## Default

B. State-stored, domain events through an outbox, idempotent consumers.
Event sourcing is a recorded decision with the replay questions
answered in advance, not a default shape.

## Worked rulings

- **Subscription renewal (2026-08, argued)**: took B. Ledger entries
  are state, the renewal event goes out through the outbox in the same
  transaction, and the consumer is keyed on the renewal identity so a
  redelivery is a no-op. See
  `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`.
- **Audit is not a reason (external, inherited)**: the pattern's own
  description names audit alone as the wrong reason to adopt event
  sourcing (EV-0276), so an audit requirement routes to A or B with a
  log, not to C.

## Counter-evidence

The event sourcing description is from 2005, has no operational data on
cost at scale, no guidance on snapshot cadence, and no treatment of
erasure obligations against an immutable log, which is now a first-order
constraint (EV-0276). The same author warns that failures get
attributed to event-driven architecture in general when one of four
distinct patterns was responsible (EV-0163), which is why this guide
refuses to let the four travel together. Nobody here has measured any
of it.
