---
id: WG-DEVOPS-005
summary: Trusted snapshots, a restore test with a tick, an evidenced restore drill, or full estate rehearsal?
kind: wargame
type: wargame
tags: [data, eos, infra, ops, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DEVOPS-005]
applies_when: [deploys_to_environment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: binding
basis: standard
evidence_grade: observational
sources: [EV-0201, EV-0203]
review: 2028-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DEVOPS-005: What proves the backups work?

Carried forward from the v1 devops module wargame of the same id and
re-graded against new evidence. The v1 ruling (a scheduled restore test
from the first production deploy) survives; what changes is that a tick
in a cadence row is no longer accepted as evidence. This version
governs. The v1 file it replaces is at
`archive/v1-final:doctrine/devops/wargames/WG-DEVOPS-005-backups-and-restore.md`,
kept for provenance and not for guidance.

## Decision question and stakes

Every managed database advertises backups; almost nobody has met theirs.
The fork is the strength of proof the venture demands that its data can
come back, and it is ruled before the first production write, because
afterwards every answer is retrofitted.

## Doctrines or coverage gap under pressure

- `DOC-DEVOPS-005` (binding): A restore drill runs on cadence and produces a dated evidence record with a measured elapsed time, a validation query and a result.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether production data exists at all yet.
- The data's legal weight. Audit trails and attestations raise the bar,
  because evidence of restore capability may itself be an obligation.
- Recovery objectives anyone actually holds: how much loss and how much
  downtime the operator would truly accept.
- Whether the estate itself (infrastructure as code, DNS, secrets) is
  now the thing that must survive, rather than one database.

Applicability is `deploys_to_environment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Provider snapshots, trusted

Assume `A. Provider snapshots, trusted` was selected and the outcome failed. Test this option's stated failure mechanism first: * It is a hope, not a capability. The named anti-patterns land here in a row: assuming a backup exists, assuming it is uncorrupted, assuming restore fits the recovery time objective (EV-0201).

### Premortem for B. Restore test with a tick

Assume `B. Restore test with a tick` was selected and the outcome failed. Test this option's stated failure mechanism first: * The remaining anti-pattern is intact: restoring a snapshot without querying the data back out (EV-0201). A tick records that something happened, not what it proved, and nobody can tell later whether the restore fitted the RTO.

### Premortem for C. Evidenced restore drill

Assume `C. Evidenced restore drill` was selected and the outcome failed. Test this option's stated failure mechanism first: * Someone has to define the validation criteria per data source and keep the drill script working. The hypothesis discipline feels like ceremony until the first drill falsifies one.

### Premortem for D. Full estate rehearsal

Assume `D. Full estate rehearsal` was selected and the outcome failed. Test this option's stated failure mechanism first: * Expensive in time and in cloud spend, and it needs the estate to be reproducible from code before it can run at all.

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

## Safe default

C. A backup that has never restored is a rumour, and a restore that was
never validated is an anecdote.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether production data exists at all yet.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. A backup that has never restored is a rumour, and a restore that was never validated is an anecdote.

**Exit condition:** Stop or roll back the selected branch when * It is a hope, not a capability. The named anti-patterns land here in a row: assuming a backup exists, assuming it is uncorrupted, assuming restore fits the recovery time objective (EV-0201), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether production data exists at all yet.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test **Whether production data exists at all yet.** and **The data's legal weight. Audit trails and attestations raise the bar, because evidence of restore capability may itself be an obligation.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
