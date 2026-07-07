---
summary: One shared database, one per service, or a records core with a separate high-volume store?
type: wargame
tags: [arch, data, infra]
status: active
review_by: 2027-07
---

# WG-ARCH-008: One database, one per service, or records plus readings?

## The question

Where data rests decides blast radius, cost and what the law can ask
of you. The fork recurs at every scale step: one shared database, a
database per service, or a legal-weight core with high-volume material
behind its own boundary.

## It depends on

- Volume asymmetry: does one class of data grow orders of magnitude
  faster than the rest?
- Regulatory asymmetry: does one class carry legal weight the rest
  does not?
- Service topology: how many deployables genuinely own data?
- Cost tier cliffs (storage limits that arrive suddenly).

## Options

### A. One shared database
Everything in one Postgres. Simplest operations, one backup story;
every consumer shares every failure and every migration.

### B. One database per service
Each deployable owns its store; sharing happens over APIs. Buys
independent lifecycles; costs distributed joins and N backup stories.

### C. Records core plus separate ingestion store
Legal-weight records in a small OLTP core; high-volume telemetry or
events behind their own ingestion boundary and store. The stores never
mingle; readings never mutate records.

## Decision rule

A high-volume feed with different retention or legal weight than the
core: C, and design the boundary before the feed exists. Multiple
services each owning data with real lifecycle independence: B, one
database each, shared through contracts. Otherwise A; a second
database before a second real owner is ceremony.

## Default

A until a genuine second owner or a volume-asymmetric feed appears;
then the matching option, deliberately, with the migration written.

## Worked rulings

- **Venture A (2026-07, argued)**: C as constitutional law (Part I
  Article 6, records never mingle with readings), with A serving until
  telemetry exists.
- **PatterTech_Business (2026-07, argued)**: B as the target (its
  ADR-0011: one database per service, one shared db library, pgvector
  the only mandatory extension), reached from A deliberately.
- **WiseWattage (2026, argued)**: A with C's seam: one Postgres, and a
  dropped audit hypertable (ADR-003) that taught the
  consumer-and-retention rule now in the stack profile.
