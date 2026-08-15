---
id: GD-DEVOPS-002
summary: All at once, watched canary, analysis-gated rollout, or flag-decoupled release?
kind: wargame
type: wargame
tags: [delivery, eos, infra, ops, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DEVOPS-008]
applies_when: [deploys_to_environment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0026, EV-0059, EV-0204, EV-0209]
review: 2027-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DEVOPS-002: How does a change reach users once it is deployed?

## Decision question and stakes

Deploying code and exposing behaviour are two different events, and
conflating them means every deploy is a bet on the whole user base at
once. The fork is what stands between the artefact landing and the
behaviour reaching everyone, and who or what decides to continue.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-008` (default): Progressive rollout with an automated abort condition for user-facing change.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `deploys_to_environment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Deploy is release

Assume `A. Deploy is release` was selected and the outcome failed. Test this option's stated failure mechanism first: * Every deploy is a full-population bet, and the recovery path is another deploy, which is the slowest tool available. Fine for a service with no users yet, indefensible once there are.

### Premortem for B. Watched canary

Assume `B. Watched canary` was selected and the outcome failed. Test this option's stated failure mechanism first: * The decision depends on a person being present, awake and honest about what the graph says. Under time pressure, watched canaries get promoted because everyone wants to go home.

### Premortem for C. Analysis-gated progressive rollout

Assume `C. Analysis-gated progressive rollout` was selected and the outcome failed. Test this option's stated failure mechanism first: * Needs a traffic router and a metrics backend, and it is Kubernetes-shaped in its best-documented form. It protects the serving tier only: rows the canary wrote are still there after the abort.

### Premortem for D. Flag-decoupled release

Assume `D. Flag-decoupled release` was selected and the outcome failed. Test this option's stated failure mechanism first: * Flag debt is the standing bill, and the flag standard says nothing about lifecycle (EV-0026). Every flag is an untested code path until it is removed, which is why an owner and an expiry are declared at creation (EV-0209). Combinatorial state grows fast.

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

## Safe default

C for user-facing change where the machinery exists, D where it does
not. A machine that aborts on a declared condition beats a person who
meant to watch.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Blast radius. A change that can only be wrong for one tenant is not the same as one that can corrupt every row.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C for user-facing change where the machinery exists, D where it does not. A machine that aborts on a declared condition beats a person who meant to watch.

**Exit condition:** Stop or roll back the selected branch when * Every deploy is a full-population bet, and the recovery path is another deploy, which is the slowest tool available. Fine for a service with no users yet, indefensible once there are, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Blast radius. A change that can only be wrong for one tenant is not the same as one that can corrupt every row.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
