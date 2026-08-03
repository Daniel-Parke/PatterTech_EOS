---
summary: No budget, advisory budget, enforced budget policy, or calendar change freezes?
type: guide
tags: [ops, delivery]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2028-03
review_by: 2028-03
sources: [EV-0020, EV-0096, EV-0199, EV-0211]
---

# GD-DEVOPS-003: What governs the release rate when reliability slips?

## The question

Shipping faster raises the chance of breaking something, and every
venture eventually has the argument about whether to keep shipping while
the service is wobbling. The fork is what settles that argument, and the
only useful time to rule it is before the wobble, because during one
every position is motivated.

## It depends on

- Whether an SLO exists at all. Without a target there is no budget and
  the argument has no referent.
- Who bears the cost of unreliability. A single operator who is also the
  only user can absorb what a paying customer cannot.
- Whether the venture can actually stop shipping. A one-person venture
  halting features halts everything.
- Whether the reliability signal is trustworthy enough to hang a freeze
  on. A noisy SLI turns the dial into a nuisance.

## Options

### A. No budget, judgement each time

*What it is.* Reliability is discussed when someone raises it.

*Buys.* Zero setup, and full flexibility for a venture with no users.

*Costs.* The argument is re-run every time under pressure, and the
person who most wants to ship usually wins it. There is no record of the
decision and no way to notice a pattern.

### B. SLO with an advisory budget

*What it is.* A machine-readable SLO and error budget object exists
(EV-0020) and burn is visible, but nothing is automatic. A spent budget
is information.

*Buys.* A shared referent, so the argument is about a number rather than
about vibes. Cheap to run and honest about its own limits.

*Costs.* Advisory means ignorable, and budgets that are always ignored
train everyone to ignore them. The dashboard becomes decoration.

### C. Enforced error budget policy

*What it is.* The budget is a governance dial, paraphrasing the SRE
Workbook (EV-0096, CC BY-NC-ND, so paraphrase only). While budget
remains, changes ship with low ceremony. Once it is spent, changes halt
except P0 fixes and security until the service is back inside the SLO.
The policy is written and agreed before it fires.

*Buys.* The argument is settled once, in the calm, and then executed.
Reliability work gets prioritised by the mechanism rather than by
whoever shouts.

*Costs.* Google-scale practice with no controlled comparison behind it
(EV-0096). It needs an SLI trustworthy enough to justify stopping work,
and a venture small enough that stopping feature work stops everything
will find the freeze hard to honour. A badly chosen SLO produces
freezes that teach people to game the SLO.

### D. Calendar change freezes

*What it is.* Release windows and blackout periods set by date: no
deploys on Fridays, none in December.

*Buys.* Predictability, and it is sometimes contractually required.

*Costs.* It responds to the calendar rather than to the service. It
suppresses deploy frequency without improving stability, which is
precisely the trade-off the delivery evidence says does not exist
(EV-0199). Large batches accumulate against the window and land
together, which is worse.

## Decision rule

Pre-production or no users: A, with B stood up as soon as the first SLO
is written. Users exist and the reliability signal is trustworthy: C,
with the policy written before the first burn and naming what counts as
P0. Users exist but the SLI is still noisy: B, with an explicit note
that it is a stepping stone and a date to revisit. D only where a
contract or a regulator demands it, and never as a substitute for C.

Whatever is chosen, the halt condition must never be a mean time to
recovery target: EV-0211 shows that number is not sound enough to hang a
freeze on. Burn against a declared SLO is.

## Default

C once there are users, B before that. A budget nobody enforces is a
dashboard, and a freeze nobody agreed to is an argument.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C as a default rather than
  binding. The mechanism is well described but its evidence is a
  single organisation's practice with no comparison, so it does not meet
  the bar for a binding requirement. What binds is that an SLO exists
  and is machine-readable (EV-0020), because that is what the dial needs
  to read.
- **AutoWatt (2026-07, inherited)**: no error budget, reliability
  handled by attention. Recorded here as the gap this guide addresses.
