---
id: GD-DEVOPS-004
summary: Nothing, delivery keys only, SLO plus customer impact, or a multi-dimension set?
kind: wargame
type: wargame
tags: [delivery, eos, ops, perf, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DEVOPS-004]
applies_when: [deploys_to_environment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0199, EV-0210, EV-0211, EV-0020]
review: 2028-02
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DEVOPS-004: Which reliability and delivery numbers are kept?

## Decision question and stakes

Every number that gets reported becomes a target, and every target gets
gamed. The fork is which small set of numbers a venture keeps, and the
research behind the popular answers openly disagrees with itself, so
this one is ruled with the disagreement visible rather than hidden.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-004` (binding): Every service carries at least one SLI and SLO as a machine-readable object.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Team size. Perceptual measures need people to survey.
- Who reads the number. An operator steering their own work needs
  something different from a board.
- Whether the data volume supports the statistics being done to it. A
  handful of incidents a year cannot carry a distributional claim.
- Whether the number will ever be attached to a person. If it might be,
  it should not be collected.

Applicability is `deploys_to_environment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Nothing formal

*What it is.* Notice problems when users report them.

*Buys.* No instrumentation, no gaming, no dashboards to maintain.

*Costs.* No trend, no way to tell whether a change helped, and the first
signal of decay is a complaint.

### B. Delivery keys only

*What it is.* The DORA set: deployment frequency and change lead time on
the throughput axis, change fail rate, failed deployment recovery time
and deployment rework rate on the instability axis (EV-0199).

*Buys.* Pairing throughput with instability means neither can be gamed
alone, which is the whole point of the set. Cheap to derive from the
version control and deployment systems already in place.

*Costs.* Self-reported survey data behind it, correlational, and the
published benchmark bands do not transfer to a one-person venture.
Says nothing about whether users are actually having a good time.

### C. SLO and customer impact, per event

*What it is.* A machine-readable SLO and error budget (EV-0020), plus
per-incident customer impact, cost of coordination, and lightweight
near-miss reports. Recovery time is recorded per event and never
aggregated into a mean, because incident duration is skewed, low
fidelity and uncorrelated with severity in the VOID corpus (EV-0211).

*Buys.* Measures the thing the user experiences rather than the thing
the pipeline does. Near-miss reporting surfaces the cheap lessons, and
keeping it lightweight is what keeps people filing them.

*Costs.* Needs an SLI worth trusting. Customer impact is harder to
compute than deployment frequency, so it degrades into a guess unless
someone defines it.

### D. Multi-dimension productivity set

*What it is.* SPACE: satisfaction and well-being, performance, activity,
communication and collaboration, efficiency and flow, measured across at
least three dimensions with system telemetry mixed with perceptual data
(EV-0210).

*Buys.* The most honest account of why a single number misleads, and the
only option that treats how the work feels as data.

*Costs.* The perceptual half needs surveys and a population to survey.
A solo operator running only the telemetry half has reintroduced exactly
the single-axis risk the paper warns about, which makes D-in-name-only
worse than B done knowingly.

## Failure premises

### Premortem for A. Nothing formal

Assume `A. Nothing formal` was selected and the outcome failed. Test this option's stated failure mechanism first: * No trend, no way to tell whether a change helped, and the first signal of decay is a complaint.

### Premortem for B. Delivery keys only

Assume `B. Delivery keys only` was selected and the outcome failed. Test this option's stated failure mechanism first: * Self-reported survey data behind it, correlational, and the published benchmark bands do not transfer to a one-person venture. Says nothing about whether users are actually having a good time.

### Premortem for C. SLO and customer impact, per event

Assume `C. SLO and customer impact, per event` was selected and the outcome failed. Test this option's stated failure mechanism first: of coordination, and lightweight near-miss reports. Recovery time is recorded per event and never aggregated into a mean, because incident duration is skewed, low fidelity and uncorrelated with severity in the VOID corpus (EV-0211).

### Premortem for D. Multi-dimension productivity set

Assume `D. Multi-dimension productivity set` was selected and the outcome failed. Test this option's stated failure mechanism first: * The perceptual half needs surveys and a population to survey. A solo operator running only the telemetry half has reintroduced exactly the single-axis risk the paper warns about, which makes D-in-name-only worse than B done knowingly.

## Decision rule

Users exist: C, always, because the SLO is a binding requirement anyway
and impact per event is the number that matters. Add B once there is
enough deployment history for the rates to mean anything, roughly a
month of regular deploys, and read it as a description of the delivery
system. Three or more people: consider D, and only then, because below
that the perceptual half is unavailable and the telemetry half worn as D
is a costume. A alone is acceptable only before there are users.

Two things are forbidden at every option: a fleet-wide mean time to
recovery as a target (EV-0211), and presenting any of these numbers as a
measure of a person (EV-0210).

## Safe default

C, with B added once the deploy history supports it.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Team size. Perceptual measures need people to survey.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C, with B added once the deploy history supports it.

**Exit condition:** Stop or roll back the selected branch when * No trend, no way to tell whether a change helped, and the first signal of decay is a complaint, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Team size. Perceptual measures need people to survey.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Team size. Perceptual measures need people to survey.** and **Who reads the number. An operator steering their own work needs something different from a board.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
