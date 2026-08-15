---
id: GD-DEVOPS-003
summary: No budget, advisory budget, enforced budget policy, or calendar change freezes?
kind: wargame
type: wargame
tags: [delivery, eos, ops, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DEVOPS-009]
applies_when: [deploys_to_environment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0020, EV-0096, EV-0199, EV-0211]
review: 2028-03
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DEVOPS-003: What governs the release rate when reliability slips?

## Decision question and stakes

Shipping faster raises the chance of breaking something, and every
venture eventually has the argument about whether to keep shipping while
the service is wobbling. The fork is what settles that argument, and the
only useful time to rule it is before the wobble, because during one
every position is motivated.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-009` (default): An error budget policy in the shape the SRE Workbook describes, paraphrased.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether an SLO exists at all. Without a target there is no budget and
  the argument has no referent.
- Who bears the cost of unreliability. A single operator who is also the
  only user can absorb what a paying customer cannot.
- Whether the venture can actually stop shipping. A one-person venture
  halting features halts everything.
- Whether the reliability signal is trustworthy enough to hang a freeze
  on. A noisy SLI turns the dial into a nuisance.

Applicability is `deploys_to_environment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. No budget, judgement each time

Assume `A. No budget, judgement each time` was selected and the outcome failed. Test this option's stated failure mechanism first: * The argument is re-run every time under pressure, and the person who most wants to ship usually wins it. There is no record of the decision and no way to notice a pattern.

### Premortem for B. SLO with an advisory budget

Assume `B. SLO with an advisory budget` was selected and the outcome failed. Test this option's stated failure mechanism first: * Advisory means ignorable, and budgets that are always ignored train everyone to ignore them. The dashboard becomes decoration.

### Premortem for C. Enforced error budget policy

Assume `C. Enforced error budget policy` was selected and the outcome failed. Test this option's stated failure mechanism first: * Google-scale practice with no controlled comparison behind it (EV-0096). It needs an SLI trustworthy enough to justify stopping work, and a venture small enough that stopping feature work stops everything will find the freeze hard to honour. A badly chosen SLO produces freezes that teach people to game the SLO.

### Premortem for D. Calendar change freezes

Assume `D. Calendar change freezes` was selected and the outcome failed. Test this option's stated failure mechanism first: * It responds to the calendar rather than to the service. It suppresses deploy frequency without improving stability, which is precisely the trade-off the delivery evidence says does not exist (EV-0199). Large batches accumulate against the window and land together, which is worse.

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

## Safe default

C once there are users, B before that. A budget nobody enforces is a
dashboard, and a freeze nobody agreed to is an argument.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether an SLO exists at all. Without a target there is no budget and the argument has no referent.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C once there are users, B before that. A budget nobody enforces is a dashboard, and a freeze nobody agreed to is an argument.

**Exit condition:** Stop or roll back the selected branch when * The argument is re-run every time under pressure, and the person who most wants to ship usually wins it. There is no record of the decision and no way to notice a pattern, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether an SLO exists at all. Without a target there is no budget and the argument has no referent.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Whether an SLO exists at all. Without a target there is no budget and the argument has no referent.** and **Who bears the cost of unreliability. A single operator who is also the only user can absorb what a paying customer cannot.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
