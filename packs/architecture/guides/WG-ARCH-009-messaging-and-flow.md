---
id: WG-ARCH-009
summary: Should a flow remain synchronous, use a durable claim queue, publish events or become a replayable stream?
kind: wargame
type: wargame
tags: [arch, data, eos, state, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-ARCH-009, DOC-DATAENG-001, DOC-DATAENG-009, DOC-ARCH-018]
gap_domain: messaging-flow-contract
applies_when: [has_server_code, ingests_external_data, publishes_events]
engages_when: [requires_asynchronous_delivery]
consequence: high
relations: []
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0151, EV-0157, EV-0162, EV-0163, EV-0563, EV-0564]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-ARCH-009: What carries the flow?

## Decision question and stakes

Choose the interaction contract when a producer cannot safely wait for the
consumer: synchronous request, durable claim queue, event notification or a
replayable stream. The mechanism decides what the user is told, where work is
owned, whether duplicates and reordering are legal, how state is recovered and
whether replay repeats external effects.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-009` defaults background jobs to a durable database claim queue.
- `DOC-DATAENG-001` requires every hop to state its delivery guarantee and
  treats a non-idempotent or non-transactional sink as at-least-once.
- `DOC-DATAENG-009` starts in batch until a named decision needs lower latency.
- `DOC-ARCH-018` requires the actual event pattern to be named.
- The uncovered domain is `messaging-flow-contract`: job machinery alone does
  not settle latency, acknowledgement, ordering, retry, replay and user state.

## Preconditions and engagement triggers

Draw the state transition before choosing a broker. Name the unit of work,
producer acknowledgement point, durable owner, delivery guarantee,
idempotency key, ordering scope, retry and poison-work policy, replay boundary,
user-visible pending state and recovery owner. State whether a database write
and message publication must succeed together.

Applicability is any of `has_server_code`, `ingests_external_data` or
`publishes_events`. Engage when `requires_asynchronous_delivery` is true.

## Options

### A. Synchronous request and response

Complete the work inside the caller's wait, returning one final outcome. This
has the clearest error path and consistency story. It couples availability and
latency, and becomes unsafe when work exceeds the caller's deadline or the
consumer must absorb bursts independently.

### B. Durable database claim queue with transactional outbox

Write the job or outbound message in the same transactional boundary as the
state change, then claim and process it idempotently. This avoids a dual-write
gap and fits a single deployable. It is normally at-least-once, adds queue
monitoring and can overload the primary database (EV-0157).

### C. Brokered command or event notification

Publish to an external broker so consumers scale and fail independently. This
can isolate bursts and fan out work. It adds another authority for delivery,
usually permits duplicates, and can hide the end-to-end flow behind loosely
named events.

### D. Replayable event or stream log

Retain an ordered log as an integration or analytical source and let consumers
track positions. This supports replay and several derived views. It introduces
retention, schema evolution and partition-order decisions, and replay is unsafe
when a consumer repeats an external action. Event notification, state transfer,
event sourcing and CQRS are distinct patterns, not interchangeable labels
(EV-0163).

## Failure premises

### Premortem for A. Synchronous request and response

Assume A failed. A downstream slowdown exhausted caller deadlines and worker
capacity, while retries repeated a state change whose outcome had already
committed.

### Premortem for B. Durable database claim queue with transactional outbox

Assume B failed. The worker was not idempotent, poison work blocked progress,
or the relay lagged without an SLO. The transaction closed the dual-write gap
but did not provide exactly-once processing.

### Premortem for C. Brokered command or event notification

Assume C failed. The producer acknowledged work before durable acceptance,
consumer retries produced duplicates, or no operator could reconstruct the
business flow across broker and service telemetry.

### Premortem for D. Replayable event or stream log

Assume D failed. Partitioning broke the ordering users expected, an evolved
schema made historical events unreadable, or replay sent money, messages or
other external effects twice.

## Decision rule

Keep A when the operation completes within the caller's proven deadline and
joint availability is acceptable. Under the engagement pressure, default to B
when one transactional store can durably own the work. Choose C when independent
scaling, isolation or fan-out is demonstrated and the broker's delivery and
recovery path are tested. Choose D only when retained ordered history and
replay are product requirements, with external effects fenced from replay.

Every asynchronous option must name acknowledgement, idempotency, ordering,
retry, poison-work and user-visible pending state. If those are unknown, the
architecture is not ready for selection.

## Safe default

For one deployable with a transactional store, use a durable claim queue or
transactional outbox, at-least-once processing and an explicit idempotency key.
Do not claim exactly-once behaviour from infrastructure alone.

## Cheapest discriminating test

Run one representative operation, then inject failure immediately before and
after acknowledgement and after the state write. Deliver one duplicate and one
out-of-order item. Record user-visible state, latency, retry, duplicate effect,
ordering, poison handling and whether the operation can be replayed without
repeating an external action.

## Fallback, exit and revisit

**Fallback `durable-local-claim`:** stop accepting new asynchronous work,
retain already accepted jobs in the transactional store, and drain them with
one idempotent worker while the wider flow is repaired.

**Exit condition:** leave the selected pattern when acknowledged work can be
lost, duplicates violate an invariant, ordering assumptions are unstated, or
operators cannot identify and recover stuck work.

**Revisit trigger:** repeat when the acknowledgement boundary, fan-out,
latency objective, ownership, partitioning, replay need or external side-effect
surface changes.

## Counter-evidence and transfer limits

The cited patterns explain mechanisms and trade-offs, not volume thresholds.
A broker does not create independence if producer and consumer still require a
joint release, and a database queue is not automatically simpler under high
contention. A passing fault injection proves only the tested flow, guarantee
and state transition. It does not authorise the phrase `event-driven` for
unrelated interactions.
