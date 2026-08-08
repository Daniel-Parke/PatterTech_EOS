---
summary: All at once, watched canary, analysis-gated rollout, or flag-decoupled release?
type: guide
tags: [ops, delivery, infra]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-12
sources: [EV-0026, EV-0059, EV-0204, EV-0209]
---

# GD-DEVOPS-002: How does a change reach users once it is deployed?

## The question

Deploying code and exposing behaviour are two different events, and
conflating them means every deploy is a bet on the whole user base at
once. The fork is what stands between the artefact landing and the
behaviour reaching everyone, and who or what decides to continue.

## It depends on

- Blast radius. A change that can only be wrong for one tenant is not
  the same as one that can corrupt every row.
- Whether a traffic router and a metrics backend already exist. A
  promotion query needs something to query.
- How quickly a bad signal shows up. A latency regression appears in
  minutes; a data corruption may appear in a fortnight.
- Whether the change writes data. Shifting traffic back does not unwrite
  rows (EV-0204).
- Whether anyone is awake. Automation matters most for the changes that
  land at eleven at night.

## Options

### A. Deploy is release

*What it is.* The artefact lands and every user gets the new behaviour
immediately. Recovery is a redeploy of the previous artefact.

*Buys.* Nothing to build, nothing to maintain, no flag debt, no
half-states to reason about.

*Costs.* Every deploy is a full-population bet, and the recovery path is
another deploy, which is the slowest tool available. Fine for a service
with no users yet, indefensible once there are.

### B. Watched canary

*What it is.* A fraction of traffic goes to the new version and a human
watches a dashboard, then promotes or rolls back by hand.

*Buys.* Real blast-radius reduction with almost no machinery. Works on
topologies where declarative rollout objects do not.

*Costs.* The decision depends on a person being present, awake and
honest about what the graph says. Under time pressure, watched canaries
get promoted because everyone wants to go home.

### C. Analysis-gated progressive rollout

*What it is.* The rollout object names a metric provider, a success
condition, a failure condition and a failure limit that tolerates
transient noise. Breaching the limit aborts and shifts traffic back to
the last stable version automatically (EV-0204).

*Buys.* The rollback path lives inside the deployment object rather than
in a runbook someone has to find in the middle of the night. The
promotion decision is auditable because the query is declared up front.

*Costs.* Needs a traffic router and a metrics backend, and it is
Kubernetes-shaped in its best-documented form. It protects the serving
tier only: rows the canary wrote are still there after the abort.

### D. Flag-decoupled release

*What it is.* The artefact ships dark. Behaviour is exposed by a flag
evaluated at runtime through a vendor-agnostic API, so release is a
configuration change rather than a deploy (EV-0026).

*Buys.* The fastest kill switch available, per-cohort exposure, and the
ability to deploy continuously while releasing deliberately. Experiment
flags can use asymmetric gating, where goal metrics drive the decision
and guardrails block only on significant harm (EV-0059).

*Costs.* Flag debt is the standing bill, and the flag standard says
nothing about lifecycle (EV-0026). Every flag is an untested code path
until it is removed, which is why an owner and an expiry are declared at
creation (EV-0209). Combinatorial state grows fast.

## Decision rule

No users yet: A, and say so in the change record rather than pretending
otherwise. Users exist, no traffic router or metrics backend: D for
anything user-visible, B for infrastructure-level change, with the kill
switch tested once before it is needed. Router and metrics backend
exist and the change is user-facing: C as the default, with D layered on
top for anything whose blast radius is larger than the serving tier. Any
change that writes data under the new path: C or D is necessary but not
sufficient, and the write must be compatible with the old reader, which
puts you back in GD-DEVOPS-001 option B.

Every flag created under D carries a non-empty owner and an expiry date
in the future. See
`packs/devops-reliability/refs/FLAG_AND_ROLLOUT_LIFECYCLE.md`.

## Default

C for user-facing change where the machinery exists, D where it does
not. A machine that aborts on a declared condition beats a person who
meant to watch.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C as the estate default rather
  than a binding requirement, because EV-0204 does not transfer to
  single-instance or serverless topologies and binding a requirement to
  a platform the estate has not standardised on would be asserted taste
  wearing a citation.
- **Venture A (2026-07, inherited)**: D in practice through configuration
  rather than a flag SDK, with no expiry field. The re-grade adds owner
  and expiry as binding, which is the part v1 never had.
