---
summary: Background jobs: in-process, a durable database queue, or an external broker?
type: wargame
tags: [arch, state, infra]
status: archived
review_by: 2027-07
---

# WG-ARCH-004: In-process jobs, a durable database queue, or a broker?

## The question

The first background job arrives innocently (send an email, refresh a
forecast) and the execution substrate it lands on is suddenly load-
bearing: deploys orphan it, retries duplicate it, scale queues behind
it. The fork is the substrate.

## It depends on

- Must jobs survive a deploy or crash?
- Do workers need to scale independently of the API?
- Is there already a database everyone trusts?
- Fan-out across services, or one service's own work?

## Options

### A. In-process executor
A thread pool in the service. Zero infrastructure; jobs die with the
process and nobody is told.

### B. Durable database claim queue
A jobs table claimed with `FOR UPDATE SKIP LOCKED`, idempotency keys,
stale-claim reaping, and a unit-builder registry (closures do not
serialise; persist context, rebuild work from it). One store, exactly
the database's guarantees, deploy-safe.

### C. External broker
Redis, SQS, or kin. Buys fan-out, rate shaping and multi-service
consumers; costs a second stateful system with its own failure modes.

## Decision rule

Jobs may vanish on deploy without harm: A. Jobs must survive deploys
or scale on separate workers, and one database serves the system: B,
and keep A as the default path behind a flag so the cutover is a
deploy, not a rewrite. Multi-service fan-out or throughput beyond one
database's comfort: C, and only then.

## Default

A with B's seam designed in (idempotency keys and rebuildable units
from day one); promote to B when the first job that must not vanish
appears.

## Worked rulings

- **WiseWattage (2026, argued)**: B behind the `WW_DURABLE_JOBS` flag
  (its ADR-006), in-process the default, after deploys orphaned
  forecast jobs. The unit-builder registry exists precisely because
  closures could not be picked up by a fresh worker.
