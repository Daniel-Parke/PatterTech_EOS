---
summary: How is spend governed: unwatched, budget-gated, or hard-capped?
type: wargame
tags: [ops, infra, money]
status: archived
review_by: 2027-07
---

# WG-OPS-004: How is infrastructure spend governed?

## The question

Usage-priced platforms turn architecture mistakes into invoices, and
agent fleets can spend faster than a human notices. The fork is the
governing mechanism: nothing, a budget with approval gates, or hard
caps, and it applies to agent spend as much as to hosting.

## It depends on

- Whose money it is: the operator's own, or a client's under contract
  (prior-approval clauses).
- Whether costs are usage-priced (unbounded by design) or tiered
  (cliff-edged).
- How much unattended work runs (agents, schedulers, cron fleets).

## Options

### A. Unwatched
Pay the invoice when it comes. Fine for pennies; how the surprise
invoice stories all begin.

### B. Budget with approval gates
A monthly figure in the state file, spend logged per session
(estimates acceptable), paid tiers enabled only with the named
approver's yes, and triage pausing low-priority work when the figure
is breached.

### C. Hard caps
Platform-enforced ceilings that stop service rather than overspend.
Honest and blunt; the outage it causes is chosen, not accidental.

## Decision rule

Contract money or any second stakeholder: B, with the approval rule
written where the operator boots (the state file) and the approver
named. Own money, real workloads: B without the second signature.
Experiments, scratch estates and anything an unattended fleet can
scale: C where the platform offers it, on top of B. A only where the
worst month is lunch money. Tier cliffs are design inputs: the
retention and storage decisions that keep a venture inside its tier
belong in the architecture rulings (WG-ARCH-008), not in the invoice
post-mortem.

## Default

B. Spend is a line in STATE, not a surprise in the inbox.

## Worked rulings

- **AutoWatt (2026-07, argued)**: B by contract: material third-party
  costs need Gareth's prior approval (Heads of Terms), the budget line
  sits in org/STATE.md pending Q-004, nothing paid enabled before it,
  and the operating model's triage pauses P2 and P3 work over budget.
- **WiseWattage (2026, argued)**: B in substance: the 500MB storage
  tier was treated as a design constraint (compression, batching, a
  dropped consumer-less table) rather than upgraded away; the invoice
  shaped the architecture.
