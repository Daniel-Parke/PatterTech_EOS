---
id: WG-AIML-001
summary: Should model inference run locally, through a hosted service or through a hybrid route when data, latency, capability and availability constraints conflict?
kind: wargame
type: wargame
tags: [eos, ops, perf, security, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-AIML-003, DOC-AIML-013, DOC-SEC-002, DOC-SEC-005, DOC-ARCH-010]
gap_domain: model-execution-locality
applies_when: [calls_a_model]
engages_when: [model_residency_or_hosting_is_constrained]
consequence: high
relations: [DREL-AIML-001]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0041, EV-0218, EV-0220, EV-0258, EV-0259, EV-0260, EV-0564]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-AIML-001: Where should the model run?

## Decision question and stakes

Choose local, hosted, dedicated or hybrid model execution for one defined
feature. The decision moves data and trust boundaries and changes quality,
latency, capacity, cost, offline behaviour, update control, incident access and
fallback. A model family name does not settle any of those properties.

## Doctrines or coverage gap under pressure

- `DOC-AIML-003` pins model identity and records retirement.
- `DOC-AIML-013` keeps the evaluation reproducible without the network.
- `DOC-SEC-002` prevents private data, untrusted content and outbound access
  from combining without a named control.
- `DOC-SEC-005` requires a recorded basis and route out for personal data.
- `DOC-ARCH-010` puts consequential vendors behind an owned adapter and exit
  route.
- `DREL-AIML-001` records that the hosting choice depends on the applicable
  data and security route. Neither Doctrine claims that hosting is preferable.
- The uncovered domain is `model-execution-locality`.

## Preconditions and engagement triggers

Freeze the feature evaluation set, oracle, model and runtime candidates,
hardware, concurrency, data classes, allowed route, latency and quality
thresholds, cost horizon, offline requirement and provider-loss scenario.
Record prompts, decoding, adapter contract, update and retirement policy,
telemetry, retention and who can diagnose a failed call.

Applicability is `calls_a_model`. Engage when
`model_residency_or_hosting_is_constrained` is true.

## Options

### A. Local inference on supported devices

Run the pinned model and runtime within the venture or user device, keeping
input local and retaining control of availability and update timing. This can
meet residency or offline needs. It is bounded by device memory, throughput,
power, packaging, security updates and variation across supported hardware.

### B. Shared hosted model service

Call a provider's pinned model through an owned adapter. This can offer strong
capability without owning accelerator operations and can scale quickly. It
moves data through a provider boundary, inherits quotas and outages, and
carries a retirement clock controlled elsewhere (EV-0260).

### C. Dedicated or self-hosted remote inference

Operate a pinned model on controlled remote infrastructure or a dedicated
provider boundary. This can meet central control or isolation needs while
serving several clients. It adds model-serving, capacity, patching, scaling and
recovery obligations and still depends on the network.

### D. Hybrid route with an explicit fallback policy

Use one route for the normal case and another for constrained, offline or
degraded cases, selecting by declared data and outcome rules rather than model
self-description. This can preserve a minimum feature during loss and keep
sensitive cases local. It doubles evaluation, prompt compatibility, retirement
and observability surfaces, and divergent outputs can surprise users.

## Failure premises

### Premortem for A. Local inference on supported devices

Assume A failed. Peak memory or first-use latency failed on the lowest supported
device, packaging left a vulnerable runtime unpatched, or a smaller model met a
benchmark but failed the private task-specific oracle.

### Premortem for B. Shared hosted model service

Assume B failed. A provider outage removed the feature, a data route violated
the recorded purpose or residency, or a model retirement forced migration
before the replacement passed the frozen suite.

### Premortem for C. Dedicated or self-hosted remote inference

Assume C failed. Capacity planning and patching became an unowned service,
latency still depended on the network, or nominal isolation did not provide the
incident evidence and data control expected.

### Premortem for D. Hybrid route with an explicit fallback policy

Assume D failed. Routes produced materially different outcomes, a sensitive
request fell through to hosted execution, or the rarely used fallback had
rotted and failed during the provider outage it was meant to cover.

## Decision rule

Choose A when the representative suite passes on the lowest supported device,
data must remain local or offline service is required, and runtime maintenance
is owned. Choose B when the data route is permitted, capability or elastic
capacity matters, and provider loss has an acceptable fallback. Choose C when
central inference is required but shared-provider data or control is
unacceptable, and the venture can meet the serving SLO and restoration drill.
Choose D only when two routes each pass their own acceptance threshold and a
deterministic policy prevents restricted data from taking the wrong route.

Public leaderboards shortlist candidates but do not decide the outcome
(EV-0258). Every selected model remains pinned and evaluated on the product's
own harness.

## Safe default

There is no universal safe hosting default once this high-consequence pressure
is true. Use the route that satisfies the strictest data constraint and the
frozen feature oracle with the fewest operating surfaces. If facts remain
unknown, keep the feature non-consequential or disabled and retain an offline
recorded evaluation path.

## Cheapest discriminating test

Run the same frozen evaluation set locally and through the leading hosted or
remote route. Record quality, first and steady latency, peak memory or remote
capacity, cost, complete data route and operational steps. Then remove network
or provider access and test the named minimum journey, recovery and routing of
a restricted-data canary.

## Fallback, exit and revisit

**Fallback `recorded-minimum-route`:** route only requests permitted for the
last proved local or alternate model, or disable model output and retain a
deterministic or human path. Never silently send restricted data to a different
host.

**Exit condition:** leave the route when the frozen oracle, data policy,
supported-device target, latency or availability objective fails, when a
restricted canary crosses the wrong boundary, or when retirement removes the
pinned model.

**Revisit trigger:** repeat on a model, runtime, provider, hardware, price,
data-purpose, residency, retention, capacity or feature-consequence change,
and before every retirement migration.

## Counter-evidence and transfer limits

Provider lifecycle documentation proves that hosted models can retire, not
that local hosting is preferable (EV-0260). Behaviour drift evidence concerns
two snapshots of one historical provider and includes a contested measurement
(EV-0259). Local execution does not automatically provide privacy if the
runtime logs, updates or tools have egress, while hosted processing can be
permitted under an appropriate recorded basis and controls. Results transfer
only to the tested model, runtime, hardware, provider route, dataset, budget and
oracle.
