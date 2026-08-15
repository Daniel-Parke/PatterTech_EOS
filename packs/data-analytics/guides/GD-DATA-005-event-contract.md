---
id: GD-DATA-005
summary: How are product events named and validated, hosted SDK defaults, a written convention, a reviewed tracking plan, or a registry that quarantines invalid events?
kind: wargame
type: wargame
tags: [data, delivery, eos, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATA-012]
applies_when: [publishes_analytics_table]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0138, EV-0139, EV-0318, EV-0319]
review: 2028-02
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DATA-005: How are events named and validated?

## Decision question and stakes

Somebody is about to add a tracked event. What is it allowed to be
called, what has to be true about its payload, and what happens when a
client sends something that does not match? Event taxonomies decay
quietly, and the decay is invisible until the day someone tries to
answer a question that spans a year.

## Doctrines or coverage gap under pressure

- `DOC-DATA-012` (default): Every published table and every tracked event has one named owner, and its schema, quality rules, freshness expectation and owner live in one document.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Do you own the collection path, or does a hosted SDK own it?
- How many people can add an event without asking anyone?
- Does anything replay the event log from its start?
- What is the cost of a malformed event: a gap in a chart, or a wrong
  number in a report that reads as correct?

Applicability is `publishes_analytics_table`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Hosted SDK defaults

Whatever the analytics vendor's SDK does. Buys: nothing to build. Costs:
no taxonomy, no validation, and the catalogue grows one ad hoc name at a
time until it has thousands of near-duplicates.

### B. Written convention, generated names

Names are generated rather than enumerated: pick the objects in the
product and the actions available on them, and every event name is an
object-action pair. Anything that varies per occurrence goes in a
property, never in the name (EV-0319). Buys: the taxonomy stays finite
and a new event's name is derivable rather than invented. Costs: the
convention is enforced by review, which means it is enforced by whoever
is paying attention. The source is vendor guidance with assertion behind
it and is silent on who owns the plan.

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
additive ones (EV-0318). Buys: a malformed event cannot land, and the
compatibility question is answered at authoring time. Costs: registry,
resolver and validation infrastructure is real operational weight and it
fits a pipeline you control end to end. It validates structure, not
whether the event fires at the right moment or means what its name says.

## Failure premises

### Premortem for A. Hosted SDK defaults

Assume `A. Hosted SDK defaults` was selected and the outcome failed. Test this option's stated failure mechanism first: no taxonomy, no validation, and the catalogue grows one ad hoc name at a time until it has thousands of near-duplicates.

### Premortem for B. Written convention, generated names

Assume `B. Written convention, generated names` was selected and the outcome failed. Test this option's stated failure mechanism first: the convention is enforced by review, which means it is enforced by whoever is paying attention. The source is vendor guidance with assertion behind it and is silent on who owns the plan.

### Premortem for C. Reviewed tracking plan

Assume `C. Reviewed tracking plan` was selected and the outcome failed. Test this option's stated failure mechanism first: a review step in the path of every new event, which people route around when it is slow.

### Premortem for D. Registry-enforced schemas

Assume `D. Registry-enforced schemas` was selected and the outcome failed. Test this option's stated failure mechanism first: registry, resolver and validation infrastructure is real operational weight and it fits a pipeline you control end to end. It validates structure, not whether the event fires at the right moment or means what its name says.

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

## Safe default

C. B is the naming discipline and C is the ownership that makes it
survive contact with a second person. D is a deliberate escalation, not
a starting point.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Do you own the collection path, or does a hosted SDK own it?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. B is the naming discipline and C is the ownership that makes it survive contact with a second person. D is a deliberate escalation, not a starting point.

**Exit condition:** Stop or roll back the selected branch when no taxonomy, no validation, and the catalogue grows one ad hoc name at a time until it has thousands of near-duplicates, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Do you own the collection path, or does a hosted SDK own it?

## Counter-evidence and transfer limits

### Preserved reasoning: What the envelope decides, and what it does not

Standardising the envelope (id, source, type, version, time) separately
from the payload makes routing, deduplication and tracing work across
transports without every consumer relearning a bespoke metadata layout
(EV-0138). It governs metadata only. The payload schema and its
evolution stay the producer's problem, which is where most event
breakage actually happens. Whichever option you pick, decide the upgrade
order before the first change: consumers first, producers first, either
order with optional fields only, or lockstep (EV-0139).
### Preserved reasoning: The unmeasured comparison

No comparison exists in the sources found between registry-enforced
schemas and convention plus review. Both are asserted, neither is
measured. The choice rests on whether you own the collection path, which
is a fit argument. Anyone claiming one is better in general is claiming
more than the evidence supports.
### Preserved reasoning: Naming shape, concretely

An event name is an object and a past-tense action: `Order Placed`,
`Signup Completed`, `Checkout Started`. No identifiers, no counters, no
variant names, no dates. Every one of those belongs in a property. The
casing is taste and only consistency matters; the object-action shape is
not taste, because it is what makes the taxonomy generated rather than
enumerated.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
