---
summary: Nothing, delivery keys only, SLO plus customer impact, or a multi-dimension set?
type: guide
tags: [ops, delivery, perf]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
review: 2028-02
sources: [EV-0199, EV-0210, EV-0211, EV-0020]
---

# GD-DEVOPS-004: Which reliability and delivery numbers are kept?

## The question

Every number that gets reported becomes a target, and every target gets
gamed. The fork is which small set of numbers a venture keeps, and the
research behind the popular answers openly disagrees with itself, so
this one is ruled with the disagreement visible rather than hidden.

## It depends on

- Team size. Perceptual measures need people to survey.
- Who reads the number. An operator steering their own work needs
  something different from a board.
- Whether the data volume supports the statistics being done to it. A
  handful of incidents a year cannot carry a distributional claim.
- Whether the number will ever be attached to a person. If it might be,
  it should not be collected.

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

## Default

C, with B added once the deploy history supports it.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C plus B, with the DORA and VOID
  disagreement recorded in the pack's open questions rather than
  resolved. Recovery time is kept per event. The fleet-wide mean is
  refused, which is a departure from the plain DORA reading and is
  argued on EV-0211.
- **Venture A (2026-07, inherited)**: no formal set. Deployment frequency
  was visible from the git history and read informally, which is B by
  accident and not by design.
