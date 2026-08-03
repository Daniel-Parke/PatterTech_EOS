---
summary: Where data rests, whether one shared database, private tables with distinct credentials, one store per deployable, or a records core with a separate readings store
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0162, EV-0151, EV-0152, EV-0157, EV-0159]
review: 2027-06
type: guide
tags: [arch, data, infra]
review_by: 2027-06
---

# WG-ARCH-008: one database, private tables, one per service, or records plus readings?

Carried forward from the v1 wargame of the same id, re-graded from
binding to default (D8 and D9 of `packs/architecture/PACK.md`). The
supporting evidence is hyperscale case reports and one pattern
catalogue, none of it observed at venture scale, so the ruling is a
default that must be argued away in writing rather than an invariant.

## The question

Where data rests decides blast radius, cost, and what the law can ask
of you. The fork recurs at every scale step, and the v1 framing missed
an option: ownership and physical separation are different decisions
with different prices (EV-0162).

## It depends on

- Volume asymmetry: does one class of data grow orders of magnitude
  faster than the rest?
- Regulatory asymmetry: does one class carry legal weight the rest
  does not?
- Ownership: how many deployables genuinely own data, as opposed to
  could in principle?
- Cost tier cliffs, which arrive suddenly.
- Whether cross-store writes would need sagas, and whether anyone is
  willing to operate them.

## Options

### A. One shared database, shared access

**What it is.** Everything in one store, every component holding the
same credentials.

**Buys.** The simplest operations, one backup story, real transactions
and real joins.

**Costs.** Uncontrolled access. Every consumer shares every failure
and every migration, and nothing records who owns which table. This is
what EV-0162 actually names as the anti-pattern.

### B. One database, private tables, distinct credentials

**What it is.** One physical store, but each module owns its tables
and holds credentials that reach nothing else. Optionally a schema per
module.

**Buys.** Enforced ownership at the cheapest price on EV-0162's
escalating ladder, while keeping joins and single-transaction
consistency.

**Costs.** Credential and migration discipline that has to be written
down, and a boundary that is invisible in the application code unless
a check enforces it too.

### C. One database per deployable

**What it is.** Each deployable owns its store; sharing happens over
APIs.

**Buys.** Genuinely independent lifecycles, which is the only thing
that answers DORA's independent-deployability signal (EV-0151) at the
data layer.

**Costs.** Distributed joins, sagas for cross-store writes, API
composition or CQRS for reads, and N backup stories. EV-0162 lists
these as the pattern's drawbacks, which makes it as much a warning
label as a recommendation.

### D. Records core plus separate readings store

**What it is.** Legal-weight records in a small transactional core;
high-volume telemetry or events behind their own ingestion boundary
and store. The stores never mingle, and readings never mutate records.

**Buys.** A small core that stays cheap to back up, audit and reason
about, while volume goes somewhere sized for volume.

**Costs.** Two stores to operate from the day it lands, and a seam
that has to be designed before the feed exists rather than after.

## Decision rule

A high-volume feed with different retention or legal weight from the
core: **D**, and design the boundary before the feed exists.
Deployables with real lifecycle independence, evidenced by a DORA
signal rather than an org chart: **C**, one store each, shared through
contracts. Otherwise **B**: it buys the ownership that people reach
for C to get, at a fraction of the price. **A** is never the ruling,
even at one module, because private tables cost nothing to set up on
day one. Where a state change must also produce a message, use an
outbox in the same transaction and make consumers idempotent
(EV-0157).

## Default

**B**, moving to the matching option when a second real owner or a
volume-asymmetric feed appears, with the migration written down.

## Worked rulings

- **Venture A (2026-07, argued)**: D as constitutional law, records
  never mingling with readings, with a single core serving until
  telemetry existed.
- **PatterTech_Business (2026-07, argued)**: C as the target, one
  database per service with a shared database library and pgvector as
  the only mandatory extension, reached from a single store
  deliberately.
- **WiseWattage (2026, argued)**: one Postgres with D's seam in mind.
  A dropped audit hypertable taught the consumer-and-retention rule
  that is now D9.

## Counter-evidence

EV-0162 is a pattern catalogue written for multi-team microservice
estates by a single author, with no measurement. The costs it lists
for C are precisely the costs a single-store venture does not pay,
which is why B exists as an option here and does not appear in the v1
wargame. Shopify (EV-0159) held boundaries without splitting stores at
all. Nothing in the ledger measures topology outcomes at one or two
people, so D9, the rule that every persisted table names its consumer
and retention, rests on local observation across three ventures and
nothing else.
