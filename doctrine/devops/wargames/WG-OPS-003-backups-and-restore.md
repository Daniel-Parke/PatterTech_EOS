---
summary: Trusted snapshots, scheduled restore tests, or full disaster rehearsal?
type: wargame
tags: [ops, data, infra]
status: active
review_by: 2027-07
---

# WG-OPS-003: What proves the backups work?

## The question

Every managed database advertises backups; almost nobody has met
theirs. The fork is the strength of proof the venture demands that its
data can come back, and it is ruled before the first production write,
because afterwards every answer is retrofitted.

## It depends on

- Whether production data exists at all yet.
- The data's legal weight: audit trails and attestations raise the bar
  (evidence of restore capability may itself be an obligation).
- Recovery objectives anyone actually holds: how much loss and how
  much downtime the operator would truly accept.

## Options

### A. Provider snapshots, trusted
Automated backups and point-in-time recovery switched on, never
exercised. Free, and it is a hope, not a capability.

### B. Snapshots plus a scheduled restore test
The cadence restores a real backup to a scratch instance, proves the
application reads it, records the evidence, and files an order for
anything that failed. Prove, don't assume, monthly from the first
production deploy.

### C. Full disaster rehearsal
Rebuild the estate from nothing on a cadence: infrastructure from
code, data from backups, DNS and secrets included. The only honest
answer at the scale where an estate outage is existential.

## Decision rule

Production data exists: B, from the first deploy, as a standing
cadence row with recorded evidence. Regulated or attestation-grade
data: B with the evidence linked from the compliance registry row that
demands it. C when the venture's estate (IaC, multiple services)
becomes the thing that must survive, typically alongside the first
paying customers who would sue. A is acceptable only before production
data exists.

## Default

B. A backup that has never restored is a rumour.

## Worked rulings

- **Venture A (2026-07, argued)**: B as a seeded cadence row ("backup
  restore test: prove, don't assume", monthly from first production
  deploy) with RDS automated backups and PITR beneath it, and audit
  trail integrity (its OBL-041) raising the evidential bar.
- **WiseWattage (2026, inherited)**: A in practice (Railway managed
  backups, unexercised); counted as the gap that argued this wargame
  into existence, not as evidence for A.
