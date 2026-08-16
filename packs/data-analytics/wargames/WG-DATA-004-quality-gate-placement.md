---
id: WG-DATA-004
summary: Where does the data quality rule live, a declared contract, computed metrics with anomaly detection, both, or no gate at all?
kind: wargame
type: wargame
tags: [data, delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DATA-012, DOC-DATA-013]
applies_when: [publishes_analytics_table]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0056, EV-0057, EV-0305, EV-0306]
review: 2027-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DATA-004: Where does the quality rule live?

## Decision question and stakes

A table is about to be published. Something is going to be wrong with it
one day. Where does the rule that catches that sit, what does it check,
and what happens when it fires? The choice looks like a tool choice and
is actually a choice about which failures you are able to name in
advance.

## Doctrines or coverage gap under pressure

- `DOC-DATA-012` (default): Every published table and every tracked event has one named owner, and its schema, quality rules, freshness expectation and owner live in one document.
- `DOC-DATA-013` (default): A quality gate failure blocks publication.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Does this table have consumers outside the team that wrote it, and do
  you know who they are?
- Do you already know the invariants, or are you still learning what
  normal looks like?
- What does a wrong number cost? A wasted afternoon, a wrong pricing
  decision, or a statement to a customer?
- Who is on the hook when it fires at 2am, and does that person exist?

Applicability is `publishes_analytics_table`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Contract-first

The producer declares the interface (columns, types, constraints,
freshness, owner) and the build refuses to publish anything that breaks
it (EV-0057, EV-0305). Buys: consumers can write against a promise, and
a breaking change is impossible to make by accident. Costs: it checks
shape, not meaning, so a column that changes from pence to pounds passes
every gate. You also own the declaration and have to maintain it.

### B. Observability-first

Compute metrics over the data each run (row counts, null rates,
distributions) and alert on deviation from the historic series, with
incremental computation so cost does not scale with history (EV-0306).
Buys: it catches drift nobody wrote a rule for, which is most of what
actually goes wrong. Costs: constraint suggestion learns from the data
as it is, so it will happily propose a rule that encodes a current bug
as the norm, and it needs history before it says anything useful.

### C. Both, layered

Contract on the published interface, computed metrics behind it. Buys:
the contract stops breaking changes and the metrics catch the drift the
contract cannot see. Costs: two things to maintain, and two places an
alert can come from.

### D. No gate, fast repair

Land raw, fix in the transformation layer, notice problems when a human
queries. Buys: nothing to build. Costs: every consumer discovers the
problem separately, and the discovery is a wrong decision. Honestly fits
exactly one case: a single-consumer pipeline where the consumer is the
author and a wrong number costs an afternoon.

## Failure premises

### Premortem for A. Contract-first

Assume `A. Contract-first` was selected and the outcome failed. Test this option's stated failure mechanism first: it checks shape, not meaning, so a column that changes from pence to pounds passes every gate. You also own the declaration and have to maintain it.

### Premortem for B. Observability-first

Assume `B. Observability-first` was selected and the outcome failed. Test this option's stated failure mechanism first: does not scale with history (EV-0306). Buys: it catches drift nobody wrote a rule for, which is most of what actually goes wrong. Costs: constraint suggestion learns from the data as it is, so it will happily propose a rule that encodes a current bug as the norm, and it needs history before it says anything useful.

### Premortem for C. Both, layered

Assume `C. Both, layered` was selected and the outcome failed. Test this option's stated failure mechanism first: two things to maintain, and two places an alert can come from.

### Premortem for D. No gate, fast repair

Assume `D. No gate, fast repair` was selected and the outcome failed. Test this option's stated failure mechanism first: every consumer discovers the problem separately, and the discovery is a wrong decision. Honestly fits exactly one case: a single-consumer pipeline where the consumer is the author and a wrong number costs an afternoon.

## Decision rule

- No named consumer outside the author, and a wrong number is cheap: D,
  and write down that you chose it.
- One named consumer, invariants known: A.
- New pipeline where you do not yet know what normal looks like: B
  first, and promote the invariants you learn into A.
- Any table a decision or a customer-facing number rests on: C.
- Whatever you pick, the rule and the owner live in one document (D9),
  and a failure blocks publication rather than raising a ticket (D10).

## Safe default

A on public models, B behind them, which is C in practice for anything
that matters and A alone for the rest. Private models carry no contract
ceremony (EV-0057).

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Does this table have consumers outside the team that wrote it, and do you know who they are?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A on public models, B behind them, which is C in practice for anything that matters and A alone for the rest. Private models carry no contract ceremony (EV-0057).

**Exit condition:** Stop or roll back the selected branch when it checks shape, not meaning, so a column that changes from pence to pounds passes every gate. You also own the declaration and have to maintain it, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Does this table have consumers outside the team that wrote it, and do you know who they are?

## Counter-evidence and transfer limits

### Preserved reasoning: The trap all four share

The unowned gap. A schema contract with no freshness rule and a
freshness monitor with no named owner produce the same outage: the table
is technically correct and eight hours stale, and nobody is responsible
for noticing. Putting schema, quality rules, service level and owner in
one document is the structural point behind the data contract standard,
and it matters more than which format the document is in (EV-0305).
### Preserved reasoning: What none of these catch

Semantic drift. A column whose meaning changes while its type does not
passes shape checks, and its distribution may move too little for
anomaly detection to fire. No source found offers a gate for it. The
partial mitigations are putting the unit in the column name, and
treating any unexplained metric step change as a bug until proven
otherwise.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
