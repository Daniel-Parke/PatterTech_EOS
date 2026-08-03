---
summary: How are product events named and validated, hosted SDK defaults, a written convention, a reviewed tracking plan, or a registry that quarantines invalid events?
type: guide
tags: [data, product, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0138, EV-0139]
review: 2028-02
review_by: 2028-02
---

# GD-DATA-005: How are events named and validated?

## The question

Somebody is about to add a tracked event. What is it allowed to be
called, what has to be true about its payload, and what happens when a
client sends something that does not match? Event taxonomies decay
quietly, and the decay is invisible until the day someone tries to
answer a question that spans a year.

## It depends on

- Do you own the collection path, or does a hosted SDK own it?
- How many people can add an event without asking anyone?
- Does anything replay the event log from its start?
- What is the cost of a malformed event: a gap in a chart, or a wrong
  number in a report that reads as correct?

## Options

### A. Hosted SDK defaults

Whatever the analytics vendor's SDK does. Buys: nothing to build. Costs:
no taxonomy, no validation, and the catalogue grows one ad hoc name at a
time until it has thousands of near-duplicates.

### B. Written convention, generated names

Names are generated rather than enumerated: pick the objects in the
product and the actions available on them, and every event name is an
object-action pair. Anything that varies per occurrence goes in a
property, never in the name (`FRAG-DATA-ANALYTICS-15`). Buys: the
taxonomy stays finite and a new event's name is derivable rather than
invented. Costs: the convention is enforced by review, which means it is
enforced by whoever is paying attention. The source is vendor guidance
with assertion behind it and is silent on who owns the plan.

### C. Reviewed tracking plan

B, plus one document that owns the full list, with a named owner and a
change review before an event ships. Buys: the part that actually decays
gets an owner, and a rename becomes a decision rather than an accident.
Costs: a review step in the path of every new event, which people route
around when it is slow.

### D. Registry-enforced schemas

Events are versioned, resolvable schemas held in a registry, validated
at collection time, with invalid events quarantined rather than silently
landed, and a versioning scheme that separates breaking changes from
additive ones (`FRAG-DATA-ANALYTICS-14`). Buys: a malformed event cannot
land, and the compatibility question is answered at authoring time.
Costs: registry, resolver and validation infrastructure is real
operational weight and it fits a pipeline you control end to end. It
validates structure, not whether the event fires at the right moment or
means what its name says.

## Decision rule

- Prototype, one person, throwaway: A, with a written intention to leave
  it.
- Anyone other than the author adds events: B, minimum.
- More than a handful of events, or any event feeding a reported number:
  C.
- You own the collection path and a malformed event would be expensive:
  D on top of C.
- Anything replays the log from its start: pick the transitive
  compatibility mode, because non-transitive modes only check the last
  version and give a false sense of safety to a replaying consumer
  (EV-0139).

## Default

C. B is the naming discipline and C is the ownership that makes it
survive contact with a second person. D is a deliberate escalation, not
a starting point.

## What the envelope decides, and what it does not

Standardising the envelope (id, source, type, version, time) separately
from the payload makes routing, deduplication and tracing work across
transports without every consumer relearning a bespoke metadata layout
(EV-0138). It governs metadata only. The payload schema and its
evolution stay the producer's problem, which is where most event
breakage actually happens. Whichever option you pick, decide the upgrade
order before the first change: consumers first, producers first, either
order with optional fields only, or lockstep (EV-0139).

## The unmeasured comparison

No comparison exists in the sources found between registry-enforced
schemas and convention plus review. Both are asserted, neither is
measured. The choice rests on whether you own the collection path, which
is a fit argument. Anyone claiming one is better in general is claiming
more than the evidence supports.

## Naming shape, concretely

An event name is an object and a past-tense action: `Order Placed`,
`Signup Completed`, `Checkout Started`. No identifiers, no counters, no
variant names, no dates. Every one of those belongs in a property. The
casing is taste and only consistency matters; the object-action shape is
not taste, because it is what makes the taxonomy generated rather than
enumerated.

## Worked rulings

- **PatterTech EOS data-analytics pack (2026-08, argued)**: C as the
  default, B1 binding the owner and the one document. Argued from
  `FRAG-DATA-ANALYTICS-15` for the generation rule and
  `FRAG-DATA-ANALYTICS-14` for what escalation buys.
- **Signup and checkout events (2026-08, argued)**: C. Six events, all
  object then past-tense action, tracking plan owned by the single
  engineer, no registry. See
  `packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`.
- **Replayable ledger topic (2026-08, inherited)**: transitive backward
  compatibility, inherited from EV-0139, because the ledger consumer
  rewinds to the start on rebuild.
