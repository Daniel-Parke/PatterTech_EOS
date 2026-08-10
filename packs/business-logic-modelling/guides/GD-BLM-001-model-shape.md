---
summary: How much model does this domain earn, from plain procedures to declared decisions?
kind: guide
authority: default
basis: decision
evidence_grade: anecdotal
scope: estate
sources: [EV-0269, EV-0270, EV-0272, EV-0273, EV-0277, EV-0285, EV-0286]
review: 2027-09
type: guide
tags: [arch, data, product]
---

# GD-BLM-001: How much model does this domain earn?

## The question

Four shapes are available and they are not a maturity ladder. The fork
is which one this domain has earned today, given that the wrong answer
costs in both directions: too little model and the same condition gets
re-checked in four places, too much and every later change routes
around scaffolding nobody needed (EV-0273).

## It depends on

- **Whether you can name an invariant.** Not a validation rule, an
  invariant: a statement that must never be observed false, spanning
  more than one object.
- **How many places check the same fact.** One condition re-checked in
  four places is the tell that the shape is behind the rules.
- **Whether concurrent writes hit the same cluster.** Contention is
  what makes a boundary load-bearing rather than decorative.
- **Whether the rules change on the code's clock.** Rules that move
  weekly while the code ships quarterly want a different home.
- **How many condition combinations exist.** Past what one person holds
  in their head, control flow stops being readable.

## Options

### A. Procedures over data
Logic in ordinary functions that read, decide and write. No domain
layer, no mapping, no ubiquitous-language ceremony. Buys the lowest
carry cost in the pack and a shape any reader follows. Costs nothing
until the rules thicken, at which point the same condition appears in
several handlers and nobody notices, because the tell is only visible
if somebody looks.

### B. Types that make the illegal state unrepresentable
Push the invariant into the shape of the data: money as minor units
plus currency, a date range that cannot be constructed backwards, a
status as a closed set. A parsing function returns a value carrying its
proof, so nothing downstream re-checks and nothing forgets (EV-0285).
Buys the cheapest enforcement available, costing nothing at runtime and
impossible to bypass. Costs a constructor per concept, and it does not
reach invariants that span several objects.

### C. Aggregates around a transactional boundary
Cluster what must never be observed inconsistent, make one thing the
entry point, reconcile the rest afterwards (EV-0269). Buys a place to
put a multi-object invariant and an honest answer to what may be stale.
Costs eventual consistency everywhere outside the boundary, which
brings the outbox and idempotent consumers with it, and it costs a
written boundary in the canvas field set (EV-0270).

### D. Declared decisions and machines
Take the decision out of control flow: a decision table with declared
inputs, outputs and overlap handling (EV-0277), or a statechart for a
lifecycle. Buys machine-checkable completeness and a form a
non-programmer can read. Costs an artefact to version, test and deploy,
and for a handful of rules that cost buys nothing.

## Decision rule

Start at A. Move to B the moment a scalar is not really a scalar, which
is nearly always immediately for money, dates, identifiers and
quantities with units: B is additive and combines with everything else.
Move to C only when you can write the invariant in one sentence, it
spans more than one object, and you can name what may be stale outside
the boundary. Move to D when the rules change on a different clock from
the code, or when the condition combinations exceed what one person
holds in their head, or when a lifecycle has transitions that must
never happen.

The shapes compose. B under C is the normal end state. A with B is a
legitimate final answer for most venture software.

## Default

A plus B. Growth is earned, one step at a time, against a named
trigger. The worst position is the middle one: full mapping and
lifecycle cost paid while every rule still sits in a service
(EV-0272).

## Worked rulings

- **Subscription renewal exemplar (2026-08, argued)**: took A plus B,
  then C for the one invariant that spanned the subscription and its
  ledger entries. Money and the renewal instant were B from the first
  commit. See
  `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`.
- **Four statuses is not an engine (estate, argued)**: a lifecycle with
  four states and five legal transitions takes a hand-written
  transition table under B, not a state machine library and not D. The
  threshold for D is combinations nobody holds in their head, and five
  is not that.
- **Boundaries are provisional (external, inherited)**: the source
  behind C spends its third part on first designs being wrong and
  superseded (EV-0269), so a boundary is revisited when the invariant
  changes, not defended because it is written down.

## Counter-evidence

The systematic review finds DDD's demonstrated value is decomposing
systems into services, and that several of its primary studies carried
no empirical evaluation at all (EV-0286). Nothing here is measured. C
and D are argued from consulting experience and standards adoption, so
treat the thresholds as this estate's decision rather than a finding.
