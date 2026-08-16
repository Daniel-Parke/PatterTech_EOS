---
id: WG-DEVOPS-007
summary: What telemetry is sufficient to diagnose user harm without collecting secrets, personal data or cross-tenant context unnecessarily?
kind: wargame
type: wargame
tags: [data, eos, ops, security, wargame]
scenario_modes: [conflict, gap]
applicable_doctrines: [DOC-DEVOPS-004, DOC-DEVOPS-007, DOC-SEC-004, DOC-SEC-005, DOC-SEC-017]
gap_domain: privacy-safe-observability
applies_when: [deploys_to_environment, handles_personal_data, holds_credentials]
engages_when: [observability_collects_sensitive_data]
consequence: high
relations: [DREL-OPS-002, DREL-OPS-003]
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0020, EV-0041, EV-0198, EV-0220, EV-0225, EV-0578]
review: 2027-08
review_cohort: T-0026-pressure-wargames
lifecycle: active
---

# WG-DEVOPS-007: How much telemetry is enough and safe?

## Decision question and stakes

Choose the smallest telemetry design that can detect and diagnose a named
user-journey failure without turning logs, traces or metrics into a second
store of secrets, personal data or cross-tenant context. Under-collection
extends incidents. Over-collection creates its own breach, retention and access
surface.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-004` requires at least one user-facing SLI and SLO.
- `DOC-DEVOPS-007` allows long-term dependency only on stable observability
  signals.
- `DOC-SEC-004` protects secrets and `DOC-SEC-005` controls personal data.
- `DOC-SEC-017` scores security and utility on the same runs.
- `DREL-OPS-002` and `DREL-OPS-003` record the tensions between diagnostic
  visibility, secret protection and personal-data minimisation.
- The uncovered domain is `privacy-safe-observability`.

## Preconditions and engagement triggers

Name the user journey and incident question. Build a field inventory before
instrumentation: purpose, source, sensitivity, tenant scope, cardinality,
retention, access, export, deletion and whether the value is required to answer
that question. Define the redaction point and prove it sits before every sink.
Use synthetic identifiers and secrets for the drill.

Applicability is any of `deploys_to_environment`, `handles_personal_data` or
`holds_credentials`. Engage when `observability_collects_sensitive_data` is
true.

## Options

### A. Aggregate journey metrics only

Record counts, rates, durations and bounded error classes with no request
payload or stable user identity. This is low risk and can govern an SLO. It may
show that users are failing without exposing which stage or dependency caused
the failure.

### B. Structured minimised events and traces

Emit allowlisted fields, short-lived correlation identifiers and bounded
attributes at named journey stages. This can diagnose causality while keeping
content out. Schema drift, high-cardinality values and accidental string fields
can still leak sensitive data.

### C. Pseudonymised or tokenised diagnostic linkage

Use a controlled mapping or keyed transform to join events without exposing a
direct identifier to ordinary telemetry readers. This supports per-journey
reconstruction but remains personal data where linkage is possible and adds a
key, access and deletion obligation.

### D. Time-bounded diagnostic capture under incident approval

Enable a narrow, sampled, encrypted capture for a named incident, with operator
approval, access logging, automatic expiry and post-capture review. This may
answer a question unavailable from ordinary telemetry. It carries the highest
privacy and secret risk and must never capture authentication material or
cross-tenant content by convenience.

## Failure premises

### Premortem for A. Aggregate journey metrics only

Assume A failed. The SLO detected harm but responders could not distinguish
dependency, release, tenant or stage, so recovery depended on guesswork and
took longer than the objective allowed.

### Premortem for B. Structured minimised events and traces

Assume B failed. A free-text error or URL field carried a token or personal
value, schema evolution bypassed the allowlist, or correlation broke at the
one boundary needed during the incident.

### Premortem for C. Pseudonymised or tokenised diagnostic linkage

Assume C failed. Readers could re-identify a person from auxiliary data, the
mapping outlived its purpose, or deletion removed the source record but left a
complete behavioural history in telemetry.

### Premortem for D. Time-bounded diagnostic capture under incident approval

Assume D failed. The switch stayed on, sensitive payloads reached a vendor
sink, access was broader than the incident team, or the capture lacked the one
field needed despite assuming much greater risk.

## Decision rule

Start with A and add B fields only when each field answers a named detection or
diagnosis question. Select C only when cross-event linkage is necessary and
purpose, key control, retention and deletion are recorded. Select D only for a
high-impact unresolved incident when A to C cannot discriminate the cause, the
capture has explicit approval and automatic expiry, and secret and tenant
isolation tests pass before enablement.

No raw credential, authentication token or unrestricted request or response
body is a valid telemetry option. If diagnosis appears to require one, redesign
the probe at the boundary or reproduce with synthetic data.

## Safe default

Aggregate journey measures plus structured allowlisted events with short-lived
random correlation, no free text, payloads, secrets or direct personal
identifiers. Retention and access are no broader than the named operational
purpose.

## Cheapest discriminating test

Seed one representative incident and diagnose it from the proposed redacted
telemetry. On the exact same records, seed a credential, personal identifier
and another tenant's marker at likely ingress points. The design passes only if
the incident cause is recoverable and every sensitive marker is absent from
all sinks, exports and error paths.

## Fallback, exit and revisit

**Fallback `aggregate-only`:** disable diagnostic attributes at the collector
or source, retain only bounded aggregate journey measures and reproduce the
fault with synthetic data in a controlled environment.

**Exit condition:** stop the selected telemetry when a deny-list canary reaches
a sink, purpose or retention expires, access cannot be audited, cardinality
becomes unsafe, or the signal no longer answers its named question.

**Revisit trigger:** repeat for a new sink, field, tenant boundary, identifier,
vendor, retention rule, user journey or incident question, and when a signal's
stability changes.

## Counter-evidence and transfer limits

User-led SLO guidance supports a small representative signal set but does not
settle its privacy design (EV-0578). OpenTelemetry stability applies per signal
and says nothing about whether an attribute is safe or useful (EV-0198).
Pseudonymisation reduces exposure but does not necessarily remove personal-data
duties. A seeded incident demonstrates one diagnostic question and leakage
surface, not all future errors. Utility and data minimisation must be re-tested
together as the schema changes.
