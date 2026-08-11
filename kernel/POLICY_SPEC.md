---
summary: The risk model law, the semantic factor table, tier routing, exceptions and recomputation
type: kernel
tags: [eos]
---

# POLICY_SPEC

This file is in the protected set, together with every policy's `risk`
and `approvals` blocks. Changing any of them requires an accepted ADR
and Daniel. One command enforces that: `python -m tools.eos route` exits
3 when the diff matches a protected path pattern and no `--adr` was
given. No other command reads the protected set, so an unacknowledged
touch that never runs `route` is caught by review (`tools/CLI_CONTRACTS.md`).

This is the law behind layer 1 of risk control: the task router that
assigns a workflow tier before work starts. Layer 2, the action-time
guard, is specified in `kernel/GUARD_SPEC.md`. A venture instantiates
this law in its policy file, validated by
`kernel/schemas/policy.schema.json`.

## The model

Risk classification is semantic, deterministic and auditable. The
router takes the union of two input sets and rules the minimum tier
consistent with the active factors:

- **Declared facts**: the side effects the owner states on the task
  record (sends-external, writes-production-data, migrates-schema,
  touches-auth, handles-pii, financial-impact, irreversible-action,
  rollback-cost). Every one of them reaches a factor. The record's
  `capabilities` list is free text for the reviewer and activates
  nothing.
- **Derived signals**: touched paths, DDL and DML detection, public API
  surface contact, CI and infrastructure files, install hooks in a
  dependency manifest, secret patterns, personal-data fields and diff
  size. They are derived at the gate, against a diff, and never at
  record creation, which has no diff to read. Two of them reach no
  factor and so move no ruling: a dependency manifest that merely moved,
  and a sensitive-path match. `DIAGNOSTIC_SIGNALS` in
  `tools/eos/router.py` says why for each. The detector returns both for
  a caller that wants them, and nothing prints them today.

Given the same facts and the same policy version, the ruling is always
the same, and it always comes with machine-readable reasons, one per
active factor: `{factor, tier_floor, source: declared|derived,
evidence}`.

Paths and diff size are signals that instantiate semantic factors. No
rule maps a path alone to a tier, and a pattern match carries no floor
of its own: it sets a signal, and the factor citing that signal carries
the floor. The router reads two of the policy's three `path_patterns`
lists. A `protected` match sets paths:protected, which is the only path
signal a venture's own list can raise; paths:auth and paths:payment come
from directory and filename sets fixed in the router. A `sensitive`
match sets a signal that reaches no factor, so it moves nothing. The
`reversible` list is read by nothing at all; it is a reading aid, and
editing it changes no ruling.

## The factor table

This table is `FACTOR_TABLE` in `tools/eos/router.py`, and that copy is
the one that rules. A venture's policy file carries a `risk.factors`
block of its own, validated at seed time by
`kernel/schemas/policy.schema.json`; the router never reads it, so
adding or removing a row there moves no ruling. What a venture really
tunes is the two inputs the router does read: the express thresholds,
and the protected pattern list behind paths:protected (ADR-0006). The
schema's `express.denied_by_factors` is not a third: which factors deny
Express is fixed in the table below.

Sources are exactly the names the router matches. Declared ones come
off the task record's `side_effects`; the rest are detector ids.

| Factor | Floor | Sources |
| --- | --- | --- |
| protected-set-contact | R3 | paths:protected |
| irreversible-action | R3 | declared irreversible-action, declared rollback-cost |
| destructive-migration | R3 | ddl-drop, destructive-dml |
| key-material | R3 | secret-pattern |
| data-deletion | R3 | declared writes-production-data, data-deletion |
| auth-surface | R2 | declared touches-auth, paths:auth |
| money | R2 | declared financial-impact, paths:payment |
| schema-change | R2 | declared migrates-schema, ddl-change, migration-path |
| public-contract | R2 | public-api-delta |
| ci-stateful-infra | R2 | ci-config, install-script |
| pii-handling | R2 | declared handles-pii, pii-fields |
| boundary-contact | R1, denies Express | declared sends-external |
| size-threshold | R1, denies Express | diff-size |

A floor is a minimum, never a ceiling: multiple active factors resolve
to the highest floor. The last two rows raise nothing on their own; they
only bar Express, so a task with nothing else active lands at Standard.

Three source names sit in the router's table with no detector behind
them, and it lists them rather than pretending otherwise: `no-rollback`
on irreversible-action, `egress` on boundary-contact and `infra-state`
on ci-stateful-infra. Nothing in a diff says a change cannot be undone
or that a call goes out, and the ci-config detector already matches the
files infra-state would. `RESERVED_SOURCES` in `tools/eos/router.py`
carries the reason per name. They are named so nobody reads a source
list as a control that exists.

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

Exploration is orthogonal: a sandboxed spike on `spike/T-####` that
never merges, held by the exploration playbook rather than by a check;
hardening its result re-enters through the router like any other task.

## Agent proposes, the router rules

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
keep it: the router re-rules against the diff the session actually
produced, a fact the declaration missed comes back as a discrepancy,
and the ruling only ever rises. The stored ruling decides the ceremony a
session works under; the gate ruling decides what merges.

The gate is somebody running `python -m tools.eos route --task T-####
--diff RANGE`, which exits 1 on a discrepancy. CI runs the checker and
the tests and does not run the router, so this recomputation binds
through the merge playbook rather than through a pipeline.

## Exceptions

Upward-only recomputation would inflate tiers permanently without a
sanctioned way back down. That way is the audited exception:

- A **one-off exception** lowers the ruling for a single task. It must
  cite concrete evidence (for example: DDL detected, but the hunk is
  comment-only, shown inline) and be authorised by a REVIEWER who does
  not own the task.
- A **standing exception** covers a recurring pattern. It is an accepted
  ADR in `org/decisions/`, authorised by the operator, carrying an
  expiry date (ADR-0004). An expired standing exception is caught by the
  monthly governance review, which samples recorded exceptions. No check
  reads expiry dates.
- One-off exceptions are recorded on the task record they apply to,
  beside the ruling they lower, with evidence, authoriser and date.
  There is no separate ledger; ADR-0004 withdrew the one that was
  specified and never built.
- Retro samples both: exceptions are re-examined for evidence quality,
  and an exception pattern that keeps recurring is a signal to fix the
  factor table by ADR, not to keep excepting.

No exception, standing or one-off, can cross the guard's non-waivable
floors in `kernel/GUARD_SPEC.md`.

## Capability profiles never move floors

A capability profile (`kernel/schemas/capability-profile.schema.json`)
records evidence-earned trust: benchmark runs, sampled-review pass
rates, escaped defects. Its level tunes Express thresholds, the free
decision band and the review sampling rate. No code loads it: the
tuning is a person reading the record and editing the policy, so the
profile is an argument for a change rather than the change. It never
moves a tier floor, never touches the factor table and never affects a
non-waivable floor. Trust earned on ordinary work buys speed on
ordinary work; it buys nothing where harm is possible.

## What this file is not

This file does not evaluate individual tool actions; that is the
guard's job, and it applies regardless of tier. It does not define
metadata axes (`kernel/METADATA_SPEC.md`) or command behaviour
(`tools/CLI_CONTRACTS.md`).
