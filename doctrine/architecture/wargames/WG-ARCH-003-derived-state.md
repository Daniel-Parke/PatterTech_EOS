---
summary: Derived values: always computed, cached, or stored as immutable snapshots?
type: wargame
tags: [arch, data, state]
status: active
review_by: 2027-07
---

# WG-ARCH-003: Where does derived state live?

## The question

Scores, grades, statuses, rollups, "current" anything: derived values
want to be stored the moment they get expensive, and stored derivations
drift from their sources silently. The fork is where a derived value is
allowed to rest.

## It depends on

- Whether the value carries legal or attestation weight at a point in
  time (what was true when we signed?).
- The cost and frequency of recomputation against the read rate.
- Whether an owner exists for invalidation; a cache without an owner is
  a slow bug.

## Options

### A. Always computed
Derive on read, every time. Never stale, never audited wrongly; costs
compute and latency.

### B. Cache-aside with an owner
Computed, cached with an explicit invalidation owner, TTL as the
backstop. Buys the hot path; costs an invalidation discipline that
must be written down.

### C. Immutable snapshot
The derivation is captured once, with its inputs digest and versions,
and never updated: a historical fact, not a cache. Corrections are new
snapshots.

## Decision rule

Point-in-time legal or attestation weight: C, and the snapshot records
its inputs so it can be re-derived and audited. Hot-path cost with a
nameable invalidation owner: B. Otherwise A; latency is cheaper than
drift. Never store a derived value that is neither snapshot nor owned
cache.

## Default

A, computed. Storage is where derived values go to rot.

## Worked rulings

- **AutoWatt (2026-07, argued)**: A with the C exception, in its
  constitution Part I Article 3: everything derived is computed, and
  the sole sanctioned store is the attestation snapshot a Verification
  issues (score, grade, inputs digest, profile versions).
- **WiseWattage (2026, argued)**: B for the weather grid and SAT
  results (its ADR-002): shared Postgres grid plus Redis cache-aside,
  invalidation owned by the grid keys, after per-process SQLite proved
  unshareable across replicas.
