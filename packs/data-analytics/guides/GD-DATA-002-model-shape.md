---
id: GD-DATA-002
summary: What shape does the analytics model take, a source mirror, layered wide entities, a dimensional star, or one metrics layer over any of them?
kind: wargame
type: wargame
tags: [arch, data, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATA-014]
applies_when: [publishes_analytics_table]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0057, EV-0307, EV-0308]
review: 2027-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DATA-002: What shape does the analytics model take?

## Decision question and stakes

Raw rows are landed. Between them and the person asking a question sits
some number of models. How many layers, how wide, and where does the
business logic live? This is the fork that decides whether two people
asking the same question get the same answer.

## Doctrines or coverage gap under pressure

- `DOC-DATA-014` (default): A fact model declares its grain in words before it declares columns.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How many people write queries against this, and how many of them know
  the source system?
- How often does the source schema change under you?
- Does the same business number get computed in more than one place
  today?
- Is anyone querying this interactively, where a wide pre-joined table
  is the difference between two seconds and thirty?

Applicability is `publishes_analytics_table`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Normalised source mirror

Keep the warehouse close to the source schema and push all logic into
the query. Buys: cheapest to build, and nothing to maintain when the
source changes shape. Costs: every consumer re-derives the same business
logic slightly differently, which is the failure the other three options
exist to prevent. Also couples every analyst to the source system's
internal design.

### B. Layered transformations to wide business entities

Staging models one to one with sources doing only cleaning and renaming,
intermediate models holding joins and logic, marts holding wide business
entities (EV-0307). Buys: a prefix tells a reviewer what a model is
allowed to do, so review is mechanical, and one route to each business
number. Costs: model count and build time, which is real on a small
warehouse. It says nothing about the design inside the marts layer.

### C. Dimensional star

Declare the grain of the fact table first, then the dimensions that
apply at that grain, then the facts. Integrate through conformed
dimensions so separate fact tables can be compared without a central
model. Pick a numbered slowly-changing-dimension policy rather than
arguing about history each time (EV-0308). Buys: the grain discipline, a
menu instead of an argument about history, and a shape most analysts
already know. Costs: the physical prescriptions (surrogate keys, narrow
facts) were formalised when storage and joins were expensive, and that
cost argument is much weaker on columnar storage.

### D. Layers plus a declared metrics layer

Any of the above, with the business definitions themselves declared once
in a semantic or metrics layer that queries resolve against. Buys: the
definition of "active user" lives in one place and cannot be forked by a
dashboard. Costs: another tool in the path and a tighter coupling to it.

## Failure premises

### Premortem for A. Normalised source mirror

Assume `A. Normalised source mirror` was selected and the outcome failed. Test this option's stated failure mechanism first: every consumer re-derives the same business logic slightly differently, which is the failure the other three options exist to prevent. Also couples every analyst to the source system's internal design.

### Premortem for B. Layered transformations to wide business entities

Assume `B. Layered transformations to wide business entities` was selected and the outcome failed. Test this option's stated failure mechanism first: model count and build time, which is real on a small warehouse. It says nothing about the design inside the marts layer.

### Premortem for C. Dimensional star

Assume `C. Dimensional star` was selected and the outcome failed. Test this option's stated failure mechanism first: the physical prescriptions (surrogate keys, narrow facts) were formalised when storage and joins were expensive, and that cost argument is much weaker on columnar storage.

### Premortem for D. Layers plus a declared metrics layer

Assume `D. Layers plus a declared metrics layer` was selected and the outcome failed. Test this option's stated failure mechanism first: another tool in the path and a tighter coupling to it.

## Decision rule

- One analyst who wrote the source system: A, and expect to leave it.
- More than one consumer, or any dashboard: B.
- Comparing facts across subject areas, or history policy is a live
  argument: C, taking grain-first and conformed dimensions and ignoring
  the physical prescriptions unless you measured a reason for them.
- The same business number already exists in two places: D, or fix it in
  B by deleting one route.
- In every case, declare the grain in words before you declare columns
  (D11). One sentence: one row per what.

## Safe default

B, with grain declared per fact model. The layering makes review
mechanical, the grain statement gives the auditability that C's
discipline was really buying, and nothing in the default depends on
picking a side in the wide-against-star argument.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How many people write queries against this, and how many of them know the source system?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B, with grain declared per fact model. The layering makes review mechanical, the grain statement gives the auditability that C's discipline was really buying, and nothing in the default depends on picking a side in the wide-against-star argument.

**Exit condition:** Stop or roll back the selected branch when every consumer re-derives the same business logic slightly differently, which is the failure the other three options exist to prevent. Also couples every analyst to the source system's internal design, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How many people write queries against this, and how many of them know the source system?

## Counter-evidence and transfer limits

### Preserved reasoning: The contested part, stated plainly

The dimensional source keeps facts narrow and joins to conformed
dimensions. The transformation-tool guide lands on wide denormalised
entities and does not mention star schemas at all. Neither argues the
difference and no measurement decides it. What survives both: declare
the grain, name the entity, and never let two models compute the same
business number by different routes. Treat the rest as taste.

Note the maintenance state on each side. The dimensional material has
not been substantially updated since its authors wound down, so read it
as a settled body of technique rather than a maintained one. The
layering guidance is vendor documentation for one tool with no
measurement behind it.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
