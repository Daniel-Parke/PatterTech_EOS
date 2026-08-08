---
summary: The risk model law, the semantic factor table, tier routing, exceptions and recomputation
type: kernel
tags: [eos]
---

# POLICY_SPEC

This file is in the protected set, together with every policy's `risk`
and `approvals` blocks. Changing any of them requires an accepted ADR
and Daniel. The checker refuses an unacknowledged touch (exit 3, see
`tools/CLI_CONTRACTS.md`).

This is the law behind layer 1 of risk control: the task router that
assigns a workflow tier before work starts. Layer 2, the action-time
guard, is specified in `kernel/GUARD_SPEC.md`. A venture instantiates
this law in its policy file, validated by
`kernel/schemas/policy.schema.json`.

## The model

Risk classification is semantic, deterministic and auditable. The
router takes the union of two input sets and rules the minimum tier
consistent with the active factors:

- **Declared facts**: capabilities and side effects the owner states on
  the task record (sends-external, writes-production-data,
  migrates-schema, touches-auth, handles-pii, financial-impact,
  irreversible-action, rollback-cost).
- **Derived signals**: touched paths, DDL and DML detection, dependency
  manifest deltas, public API surface contact, CI and infra files,
  secret patterns, diff size.

Given the same facts and the same policy version, the ruling is always
the same, and it always comes with machine-readable reasons, one per
active factor: `{factor, tier_floor, source: declared|derived,
evidence}`.

Paths and diff size are signals that instantiate semantic factors. No
rule maps a path alone to a tier. The policy's `path_patterns` lists
(reversible, sensitive, protected) exist only as signal sources that
the factor table cites; a pattern match activates a factor, and the
factor carries the floor.

## The factor table

Every policy binds at least these factors. A venture may add stricter
factors; it may not remove or weaken these.

| Factor | Effect | Typical sources |
| --- | --- | --- |
| protected-set contact | floor R3 | paths:protected match in the diff |
| irreversible action | floor R3 | declared irreversible-action; derived no-rollback detection |
| destructive migration | floor R3 | DDL drops, destructive DML, migrates-schema with data loss |
| key material | floor R3 | secret patterns in the diff or environment |
| data deletion | floor R3 | deletion beyond the working tree, declared or derived |
| auth surface | floor R2 | touches-auth; authn or authz paths |
| money | floor R2 | financial-impact; payment and billing paths |
| schema change | floor R2 | migrates-schema; DDL detection |
| public contract | floor R2 | public API surface contact; exported interface deltas |
| CI and stateful infra | floor R2 | CI config and infrastructure-with-state files |
| PII handling | floor R2 | handles-pii; personal-data field detection |
| boundary contact | denies R0 | sends-external; any egress beyond the repo |
| size threshold | denies R0 | diff lines or file count over the express limits |

A floor is a minimum, never a ceiling: multiple active factors resolve
to the highest floor. "Denies R0" raises nothing by itself; it only
bars Express, so the task routes Standard or higher on whatever else is
active.

## Tiers and routing

- **R0** routes to Express: reversible local work, commit message as
  the whole record, targeted checks, self-merge.
- **R1** routes to Standard, the default: one owner, a task record,
  sampled review unless the reasons or the capability profile demand an
  independent one.
- **R2** routes to High-assurance: independent oracle authored before
  implementation and frozen, explicit invariants, rollback plan,
  independent review at acceptance.
- **R3** is High-assurance plus a human: operator approval for anything
  irreversible or externally consequential, always.

Exploration is orthogonal: a sandboxed spike on `spike/T-####` that the
checker refuses to merge; hardening its result re-enters through the
router like any other task.

## Agent proposes, checker decides

The owning agent proposes declared facts and a proposed tier. The
router, not the agent, rules the tier. A fact the derived signals
expose but the declaration missed is a gate-time discrepancy finding:
the work does not merge until the declaration is corrected and the task
re-routed. Honest declaration costs nothing; omission is visible.

## Routing is paid once

The ruling is computed when the task record is created and stored on
the record: `tier_ruled` with the machine-readable reasons beside it. A
session reads its tier and its reasons from the record, which is a
plain file read, and does not run the router again to learn what the
record already carries. A record created without declared facts routes
from an empty fact set and rules a clean R0; its reasons list is empty,
and an empty reasons list is how a record says no factor is active.

Express work below the record threshold is unchanged. It has no record
because the commit message is the whole record, and the record is
created at the moment the work converts to Standard or above, which is
where the ruling is stored.

Two recomputations remain, and neither is a per-session round trip. The
owner re-routes when the declared facts themselves change mid-run. The
gate recomputes at merge, next.

## Gate-time recomputation, upward only

At the merge gate the router recomputes the tier against the actual
diff, not the declared intent. The recomputed tier can only raise the
ruling, never lower it. Work that arrived as R1 and turns out to touch
an R2 surface is re-routed and re-verified at R2. The only path down is
an exception, below.

This recomputation is what makes routing once safe rather than a
loophole. A session cannot under-declare its way to a lower tier and
keep it: the checker re-rules against the diff the session actually
produced, a fact the declaration missed is a discrepancy finding that
blocks the merge until the record is corrected and re-routed, and the
ruling only ever rises. The stored ruling decides the ceremony a
session works under; the gate ruling decides what merges.

## Exceptions

Upward-only recomputation would inflate tiers permanently without a
sanctioned way back down. That way is the audited exception:

- A **one-off exception** lowers the ruling for a single task. It must
  cite concrete evidence (for example: DDL detected, but the hunk is
  comment-only, shown inline) and be authorised by a REVIEWER who does
  not own the task.
- A **standing exception** covers a recurring pattern. It is an accepted
  ADR in `org/decisions/`, authorised by the operator, carrying an
  expiry date (ADR-0004). An expired standing exception is a checker
  finding.
- One-off exceptions are recorded on the task record they apply to,
  beside the ruling they lower, with evidence, authoriser and date.
  There is no separate ledger: `org/exceptions.jsonl` was specified,
  never implemented and never read, so the one sanctioned route back
  down from an upward-only ruling was a document. An exception now
  lives where the decision lives.
- Retro samples both: exceptions are re-examined for evidence quality,
  and an exception pattern that keeps recurring is a signal to fix the
  factor table by ADR, not to keep excepting.

No exception, standing or one-off, can cross the guard's non-waivable
floors in `kernel/GUARD_SPEC.md`.

## Capability profiles never move floors

A capability profile (`kernel/schemas/capability-profile.schema.json`)
records evidence-earned trust: benchmark runs, sampled-review pass
rates, escaped defects. Its level tunes Express thresholds, the free
decision band and the review sampling rate. It never changes a tier
floor, never touches the factor table and never affects a non-waivable
floor. Trust earned on ordinary work buys speed on ordinary work; it
buys nothing where harm is possible.

## What this file is not

This file does not evaluate individual tool actions; that is the
guard's job, and it applies regardless of tier. It does not define
metadata axes (`kernel/METADATA_SPEC.md`) or command behaviour
(`tools/CLI_CONTRACTS.md`).
