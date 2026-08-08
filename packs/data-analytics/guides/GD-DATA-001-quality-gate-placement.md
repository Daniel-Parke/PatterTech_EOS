---
summary: Where does the data quality rule live, a declared contract, computed metrics with anomaly detection, both, or no gate at all?
type: guide
tags: [data, testing, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0056, EV-0057]
review: 2027-12
---

# GD-DATA-001: Where does the quality rule live?

## The question

A table is about to be published. Something is going to be wrong with it
one day. Where does the rule that catches that sit, what does it check,
and what happens when it fires? The choice looks like a tool choice and
is actually a choice about which failures you are able to name in
advance.

## It depends on

- Does this table have consumers outside the team that wrote it, and do
  you know who they are?
- Do you already know the invariants, or are you still learning what
  normal looks like?
- What does a wrong number cost? A wasted afternoon, a wrong pricing
  decision, or a statement to a customer?
- Who is on the hook when it fires at 2am, and does that person exist?

## Options

### A. Contract-first

The producer declares the interface (columns, types, constraints,
freshness, owner) and the build refuses to publish anything that breaks
it (EV-0057, `EV-0305`). Buys: consumers can write
against a promise, and a breaking change is impossible to make by
accident. Costs: it checks shape, not meaning, so a column that changes
from pence to pounds passes every gate. You also own the declaration and
have to maintain it.

### B. Observability-first

Compute metrics over the data each run (row counts, null rates,
distributions) and alert on deviation from the historic series, with
incremental computation so cost does not scale with history
(`EV-0306`). Buys: it catches drift nobody wrote a rule
for, which is most of what actually goes wrong. Costs: constraint
suggestion learns from the data as it is, so it will happily propose a
rule that encodes a current bug as the norm, and it needs history before
it says anything useful.

### C. Both, layered

Contract on the published interface, computed metrics behind it. Buys:
the contract stops breaking changes and the metrics catch the drift the
contract cannot see. Costs: two things to maintain, and two places an
alert can come from.

### D. No gate, fast repair

Land raw, fix in the transformation layer, notice problems when a human
queries. Buys: nothing to build. Costs: every consumer discovers the
problem separately, and the discovery is a wrong decision. Honestly
fits exactly one case: a single-consumer pipeline where the consumer is
the author and a wrong number costs an afternoon.

## Decision rule

- No named consumer outside the author, and a wrong number is cheap: D,
  and write down that you chose it.
- One named consumer, invariants known: A.
- New pipeline where you do not yet know what normal looks like: B
  first, and promote the invariants you learn into A.
- Any table a decision or a customer-facing number rests on: C.
- Whatever you pick, the rule and the owner live in one document (B1),
  and a failure blocks publication rather than raising a ticket (B2).

## Default

A on public models, B behind them, which is C in practice for anything
that matters and A alone for the rest. Private models carry no contract
ceremony (EV-0057).

## The trap all four share

The unowned gap. A schema contract with no freshness rule and a
freshness monitor with no named owner produce the same outage: the table
is technically correct and eight hours stale, and nobody is responsible
for noticing. Putting schema, quality rules, service level and owner in
one document is the structural point behind the data contract standard,
and it matters more than which format the document is in
(`EV-0305`).

## What none of these catch

Semantic drift. A column whose meaning changes while its type does not
passes shape checks, and its distribution may move too little for
anomaly detection to fire. No source found offers a gate for it. The
partial mitigations are putting the unit in the column name, and
treating any unexplained metric step change as a bug until proven
otherwise.

## Worked rulings

- **PatterTech EOS data-analytics pack (2026-08, argued)**: C as the
  default shape, with B1 and B2 binding the ownership and the blocking
  behaviour rather than the tool. Argued from EV-0057 for the
  interface-only scope and `EV-0306` for the drift case.
- **Signup and checkout event model (2026-08, argued)**: A on the
  published fact model with a not-null rule on the order total, run in
  the build so a seeded null batch fails the pipeline. See
  `packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`.
- **Personal scratch analysis (2026-08, inherited)**: D, inherited. One
  consumer, who is the author, and nothing leaves the room.
