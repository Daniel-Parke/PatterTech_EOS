---
id: WG-BLM-001
summary: How much model does this domain earn, from plain procedures to declared decisions?
kind: wargame
type: wargame
tags: [arch, data, eos, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-BLM-003]
applies_when: [encodes_domain_rule]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: anecdotal
sources: [EV-0269, EV-0270, EV-0272, EV-0273, EV-0277, EV-0285, EV-0286]
review: 2027-09
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-BLM-001: How much model does this domain earn?

## Decision question and stakes

Four shapes are available and they are not a maturity ladder. The fork
is which one this domain has earned today, given that the wrong answer
costs in both directions: too little model and the same condition gets
re-checked in four places, too much and every later change routes
around scaffolding nobody needed (EV-0273).

## Doctrines or coverage gap under pressure

- `DOC-BLM-003` (default): Start with no model and earn the next step.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `encodes_domain_rule`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Procedures over data

Assume `A. Procedures over data` was selected and the outcome failed. Test this option's stated failure mechanism first: in the pack and a shape any reader follows. Costs nothing until the rules thicken, at which point the same condition appears in several handlers and nobody notices, because the tell is only visible if somebody looks.

### Premortem for B. Types that make the illegal state unrepresentable

Assume `B. Types that make the illegal state unrepresentable` was selected and the outcome failed. Test this option's stated failure mechanism first: a constructor per concept, and it does not reach invariants that span several objects.

### Premortem for C. Aggregates around a transactional boundary

Assume `C. Aggregates around a transactional boundary` was selected and the outcome failed. Test this option's stated failure mechanism first: eventual consistency everywhere outside the boundary, which brings the outbox and idempotent consumers with it, and it costs a written boundary in the canvas field set (EV-0270).

### Premortem for D. Declared decisions and machines

Assume `D. Declared decisions and machines` was selected and the outcome failed. Test this option's stated failure mechanism first: an artefact to version, test and deploy, and for a handful of rules that cost buys nothing.

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

## Safe default

A plus B. Growth is earned, one step at a time, against a named
trigger. The worst position is the middle one: full mapping and
lifecycle cost paid while every rule still sits in a service
(EV-0272).

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether you can name an invariant.** Not a validation rule, an invariant: a statement that must never be observed false, spanning more than one object.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A plus B. Growth is earned, one step at a time, against a named trigger. The worst position is the middle one: full mapping and lifecycle cost paid while every rule still sits in a service (EV-0272).

**Exit condition:** Stop or roll back the selected branch when in the pack and a shape any reader follows. Costs nothing until the rules thicken, at which point the same condition appears in several handlers and nobody notices, because the tell is only visible if somebody looks, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether you can name an invariant.** Not a validation rule, an invariant: a statement that must never be observed false, spanning more than one object.

## Counter-evidence and transfer limits

The systematic review finds DDD's demonstrated value is decomposing
systems into services, and that several of its primary studies carried
no empirical evaluation at all (EV-0286). Nothing here is measured. C
and D are argued from consulting experience and standards adoption, so
treat the thresholds as this estate's decision rather than a finding.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
