---
summary: The machine-readable SLO object, the error budget policy shape, and the aggregate metrics this estate refuses
type: implementation
tags: [ops, delivery]
kind: recipe
scope: estate
review: 2028-02
sources: [EV-0020, EV-0096, EV-0199, EV-0211]
---

# SLO objects and the error budget policy

Level-3 reference for binding requirement 4 and for
`packs/devops-reliability/guides/GD-DEVOPS-003-error-budget-dial.md`.

## The SLO object

Reliability targets are declarative, vendor-neutral and machine-readable
(EV-0020). Prose in a wiki is not an SLO, because nothing can read it,
nothing can alert on it, and nobody can tell later what the target was
when the argument happened.

The minimum a service carries:

```yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: api-availability
spec:
  service: api
  indicator:
    metadata:
      name: successful-requests
    spec:
      ratioMetric:
        good: { metricSource: { type: Prometheus } }
        total: { metricSource: { type: Prometheus } }
  objectives:
    - displayName: 99.5 percent of requests succeed
      target: 0.995
  timeWindow:
    - duration: 28d
      isRolling: true
```

The specification also covers error budget and alert policy objects. A
venture starts with one SLI per service and adds only when an argument
needs one. EV-0020 is a specification and not evidence that SLO-driven
governance works, so the binding claim is narrow: the target exists and
is machine-readable. What is done with it is the guide's business.

## The error budget policy

Paraphrased from EV-0096, which is CC BY-NC-ND and is therefore never
quoted here. The shape:

- The budget is what the objective permits over the window. A 99.5
  percent target over 28 days permits roughly 3 hours 22 minutes of
  failure.
- While budget remains, changes ship with low ceremony.
- Once the budget is spent, changes halt except P0 fixes and security
  work, until the service is back inside the objective.
- The policy is written and agreed before it first fires, and it names
  what counts as P0 in this venture.

That evidence is one organisation's practice with no controlled
comparison behind it, which is why the policy is a default in this pack
and not a binding requirement.

## Delivery numbers

Where they are kept, keep both axes. Throughput is deployment frequency
and change lead time; instability is change fail rate, failed deployment
recovery time and deployment rework rate (EV-0199, CC BY 4.0, Google
LLC). Reporting a throughput number without an instability number is the
failure mode the set exists to prevent. The published benchmark bands
are derived from self-reported survey data clustered into performance
groups and do not transfer to a one or two person venture, so use the
numbers as a trend against yourself and never as a grade against the
industry.

## What this estate refuses

- **A fleet-wide mean time to recovery target.** Incident duration is
  positively skewed and low fidelity, and across the VOID corpus it did
  not correlate with severity (EV-0211). Record recovery time per event.
  Do not average it, do not target the average, and do not put the
  average on a dashboard where someone will target it anyway.
- **Delivery numbers presented as individual productivity.** They
  describe the delivery system (EV-0199, EV-0210). Attaching them to a
  person converts a measure into a target and destroys both.
- **Action-item counts from postmortems as a metric.** Counting them
  rewards filing tickets, which is not the same as learning anything.

## Cheaper signals worth more

EV-0211 offers substitutes that a small venture can actually run:
customer impact per incident, the cost of coordination during it, and
near-miss reports. Near-miss reporting only works while it stays
lightweight, so a near miss does not automatically trigger an
investigation. The moment it does, the reports stop.
