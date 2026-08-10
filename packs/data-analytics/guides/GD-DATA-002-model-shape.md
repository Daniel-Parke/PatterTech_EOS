---
summary: What shape does the analytics model take, a source mirror, layered wide entities, a dimensional star, or one metrics layer over any of them?
type: guide
tags: [data, arch]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0057, EV-0307, EV-0308]
review: 2027-12
---

# GD-DATA-002: What shape does the analytics model take?

## The question

Raw rows are landed. Between them and the person asking a question sits
some number of models. How many layers, how wide, and where does the
business logic live? This is the fork that decides whether two people
asking the same question get the same answer.

## It depends on

- How many people write queries against this, and how many of them know
  the source system?
- How often does the source schema change under you?
- Does the same business number get computed in more than one place
  today?
- Is anyone querying this interactively, where a wide pre-joined table
  is the difference between two seconds and thirty?

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

## Default

B, with grain declared per fact model. The layering makes review
mechanical, the grain statement gives the auditability that C's
discipline was really buying, and nothing in the default depends on
picking a side in the wide-against-star argument.

## The contested part, stated plainly

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

## Worked rulings

- **PatterTech EOS data-analytics pack (2026-08, argued)**: B as the
  default, grain declaration carried across as D11. Argued from EV-0307
  for the layering and EV-0308 for grain-first.
- **Signup and checkout event model (2026-08, argued)**: B, with one
  fact model at one row per checkout order and a wide user entity. Grain
  stated in the model documentation. See
  `packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`.
- **Public model contract scope (2026-08, inherited)**: contracts on
  marts only, private staging and intermediate models uncontracted,
  inherited from EV-0057.
