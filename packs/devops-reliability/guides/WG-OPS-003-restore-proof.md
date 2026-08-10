---
summary: Trusted snapshots, a restore test with a tick, an evidenced restore drill, or full estate rehearsal?
type: guide
tags: [ops, data, infra]
kind: guide
scope: estate
applies_when: [stores_persistent_data]
authority: binding
basis: standard
evidence_grade: observational
review: 2028-06
sources: [EV-0201, EV-0203]
---

# WG-OPS-003: What proves the backups work?

Carried forward from the v1 devops module wargame of the same id and
re-graded against new evidence. The v1 ruling (a scheduled restore test
from the first production deploy) survives; what changes is that a tick
in a cadence row is no longer accepted as evidence. This version
governs. The v1 file it replaces is at
`archive/v1-final:doctrine/devops/wargames/WG-OPS-003-backups-and-restore.md`,
kept for provenance and not for guidance.

## The question

Every managed database advertises backups; almost nobody has met theirs.
The fork is the strength of proof the venture demands that its data can
come back, and it is ruled before the first production write, because
afterwards every answer is retrofitted.

## It depends on

- Whether production data exists at all yet.
- The data's legal weight. Audit trails and attestations raise the bar,
  because evidence of restore capability may itself be an obligation.
- Recovery objectives anyone actually holds: how much loss and how much
  downtime the operator would truly accept.
- Whether the estate itself (infrastructure as code, DNS, secrets) is
  now the thing that must survive, rather than one database.

## Options

### A. Provider snapshots, trusted

*What it is.* Automated backups and point-in-time recovery switched on,
never exercised.

*Buys.* Nothing beyond the configuration. It is free.

*Costs.* It is a hope, not a capability. The named anti-patterns land
here in a row: assuming a backup exists, assuming it is uncorrupted,
assuming restore fits the recovery time objective (EV-0201).

### B. Restore test with a tick

*What it is.* A cadence row that says a restore was performed, marked
done by whoever performed it.

*Buys.* Someone has actually run a restore at least once, which puts it
a long way ahead of A.

*Costs.* The remaining anti-pattern is intact: restoring a snapshot
without querying the data back out (EV-0201). A tick records that
something happened, not what it proved, and nobody can tell later
whether the restore fitted the RTO.

### C. Evidenced restore drill

*What it is.* B, plus a machine-readable evidence record per run. The
drill states a steady-state hypothesis before it starts (EV-0203),
restores into a fresh location, runs a named validation query against
the restored data, records rows validated, records elapsed time against
the RTO and data loss against the RPO, and alerts when either is missed
(EV-0201). A failed drill files work.

*Buys.* The claim becomes checkable by a script rather than by asking
someone. A regression in restore time shows up as a number moving, not
as a surprise during an outage.

*Costs.* Someone has to define the validation criteria per data source
and keep the drill script working. The hypothesis discipline feels like
ceremony until the first drill falsifies one.

### D. Full estate rehearsal

*What it is.* Rebuild the estate from nothing on a cadence:
infrastructure from code, data from backups, DNS and secrets included.

*Buys.* The only honest answer where an estate outage is existential,
and the only one that catches the dependencies nobody wrote down.

*Costs.* Expensive in time and in cloud spend, and it needs the estate
to be reproducible from code before it can run at all.

## Decision rule

No production data yet: A, with C scheduled against the first production
deploy. Production data exists: C, from the first production deploy, as
a standing cadence with an evidence record per run. Regulated or
attestation-grade data: C with the evidence linked from the compliance
registry row that demands it. The estate, rather than one database, has
become the thing that must survive, typically alongside the first
customers who would sue: D on a slower cadence with C continuing
underneath.

B is not a resting place. It is what C looks like before someone wrote
down what the restore proved.

## Default

C. A backup that has never restored is a rumour, and a restore that was
never validated is an anecdote.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C re-graded to binding on
  EV-0201, whose anti-pattern list is the argument. The evidence record
  shape is fixed in
  `packs/devops-reliability/refs/RESTORE_DRILL_EVIDENCE.md` so a checker
  can read it, and the pack drill treats a passing record with a
  measured elapsed time inside the RTO as a fatal criterion.
- **AutoWatt (2026-07, argued)**: B as a seeded cadence row, monthly
  from first production deploy, with managed automated backups and
  point-in-time recovery beneath it, and audit trail integrity raising
  the evidential bar. Under this re-grade that ruling moves to C, and
  the cadence row now owes an evidence record.
- **WiseWattage (2026, inherited)**: A in practice, managed backups
  unexercised. Counted as the gap that argued this wargame into
  existence, not as evidence for A.
