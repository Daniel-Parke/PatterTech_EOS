---
id: GD-BLM-005
summary: Is the record of truth the current state or the sequence of events?
kind: wargame
type: wargame
tags: [arch, data, eos, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-BLM-012]
applies_when: [encodes_domain_rule]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: anecdotal
sources: [EV-0138, EV-0157, EV-0163, EV-0269, EV-0275, EV-0276]
review: 2027-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-BLM-005: State or events as the record?

## Decision question and stakes

Whether the durable truth is the current state of a thing or the
sequence of events that produced it. The question gets muddled because
four separate patterns travel under one name, so name which is meant
before arguing: event notification, event-carried state transfer, event
sourcing, and CQRS (EV-0163). This guide is about the third.

## Doctrines or coverage gap under pressure

- `DOC-BLM-012` (default): A state change and its outbound message are committed together or not at all.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `encodes_domain_rule`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. State-stored, with a plain audit log

Assume `A. State-stored, with a plain audit log` was selected and the outcome failed. Test this option's stated failure mechanism first: the ability to rebuild past state cheaply: a log records cheaply and reconstructs expensively (EV-0275).

### Premortem for B. State-stored, with domain events published through an outbox

Assume `B. State-stored, with domain events published through an outbox` was selected and the outcome failed. Test this option's stated failure mechanism first: an outbox table, a relay and idempotent consumers, because the pattern buys at-least-once delivery and nothing more.

### Premortem for C. Event-sourced aggregate, state as a projection

Assume `C. Event-sourced aggregate, state as a projection` was selected and the outcome failed. Test this option's stated failure mechanism first: the three named traps: effects on replay, external reads on replay, and old event shapes that must stay readable forever or be upgraded deliberately (EV-0276). Also costs snapshot policy, which the source does not cover.

### Premortem for D. C, plus separated read models

Assume `D. C, plus separated read models` was selected and the outcome failed. Test this option's stated failure mechanism first: a second consistency story that every user-facing feature has to understand.

## Decision rule

A until something outside the boundary needs to know. Then B, which is
where most venture software stops and which default D10 in PACK.md
binds the mechanics of. Choose C only when replay or as-at-past-instant
state is a stated requirement with a named question behind it, never
for audit alone, because a log is cheaper (EV-0276). Choose D only
after C, and only when a read shape genuinely cannot be served from the
projection you already keep.

Whichever is chosen, the event envelope is a wire contract and belongs
to `packs/api-integration/PACK.md` and EV-0138, not to the domain
model.

## Safe default

B. State-stored, domain events through an outbox, idempotent consumers.
Event sourcing is a recorded decision with the replay questions
answered in advance, not a default shape.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether anyone needs the state as at a past instant.** Not a history table, the actual state, rebuilt.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B. State-stored, domain events through an outbox, idempotent consumers. Event sourcing is a recorded decision with the replay questions answered in advance, not a default shape.

**Exit condition:** Stop or roll back the selected branch when the ability to rebuild past state cheaply: a log records cheaply and reconstructs expensively (EV-0275), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether anyone needs the state as at a past instant.** Not a history table, the actual state, rebuilt.

## Counter-evidence and transfer limits

The event sourcing description is from 2005, has no operational data on
cost at scale, no guidance on snapshot cadence, and no treatment of
erasure obligations against an immutable log, which is now a first-order
constraint (EV-0276). The same author warns that failures get
attributed to event-driven architecture in general when one of four
distinct patterns was responsible (EV-0163), which is why this guide
refuses to let the four travel together. Nobody here has measured any
of it.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
