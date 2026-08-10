---
summary: Subcommand contracts for python -m tools.eos, inputs, JSON outputs, exit codes
type: kernel
tags: [eos]
---

# CLI_CONTRACTS

Every command is invoked as `python -m tools.eos <cmd>` from the repo
root. Machine output is JSON on stdout, validating the named schema in
`kernel/schemas/`. Human-readable findings go to stderr.

Exit codes, uniform across commands:

- **0**: clean, or warnings only.
- **1**: findings (errors, refusals, blocking verdicts, failed criteria).
- **2**: cannot run (missing dependency, absent file, malformed input).
  Missing jsonschema exits 2 and prints the install command.
- **3**: protected-touch-unacknowledged: the requested change reaches a
  protected-set file or a policy `protected_pointers` target without
  `--adr ADR-####` naming an accepted ADR that authorises it.

## check

Inputs: `--repo` (the default; passing it with `--seed` exits 2 because
they are different runs), `--seed PATH`, `--write-index`, `--series E|S|D|F`
to run one series, `--strict-semantic` and `--relax-semantic` to pin or
drop the S-series severity, `--offline` to skip checks needing git remotes,
and `--json`. Output: a findings list `[{check, path, message, severity}]`.
`--write-index` regenerates every derived index to a fixpoint and is the
only sanctioned way to update them. Exit 1 on any error-severity finding.

## route

Inputs: `--task T-####` or `--facts FILE` (declared facts JSON), plus
optional `--diff RANGE` for gate-time recomputation and `--adr ADR-####`
to acknowledge a protected-set touch. Output: `{tier, reasons,
discrepancies}` where `reasons` rows follow `task-record.schema.json` and
`discrepancies` lists derived facts the declaration missed. Deterministic
given the same inputs and policy version. Gate-time recomputation only
ever raises the ruling. Exit 1 when discrepancies are found at the gate.
Exit 3 when a reason carries the factor `protected-set-contact` and no
`--adr` was given; the message names the file that matched.

## guard eval

Inputs: `--class CLASS --payload SUMMARY`, or `--tool NAME --input FILE`
for adapter use. Output: one document per
`guard-action.schema.json`. Without a validated adapter every guarded
class rules manual-only (fail closed). Exit 0 for allow, 1 for any
blocking verdict, 2 when evaluation itself cannot run.

## context

Inputs: `--diff RANGE`. Output: the changed-surface context packet as
JSON on stdout, truncated to 300 lines: `{changed, summaries,
referencing_files, activated_packs, routed}`. Unchanged context is never
re-supplied within a run.

## task

Record ops: `new`, `show`, `update`, each reading and writing
`org/tasks/T-####.json` (`task-record.schema.json`) via
write-temp-then-rename. A record is closed by `update` setting its
status; there is no separate `close` op.

Claim ops: `claims-verify --lane ID --paths ...` compares a lane's diff
against its assigned claims and exits 1 on any file outside them.
`org/claims.json` is written by the integrator by hand and committed
before dispatch; there is no `claims assign`, `renew` or `recover`
command. Recovery of an expired claim needs liveness evidence and the
operator, and a timestamp alone never authorises it.

View op: `views` (integrator only) regenerates the derived
`org/TASKS.md` and `org/STATE.md` from the task records, claims,
cadence rows and git facts; hand-edits to those views are checker
errors.

Refusal semantics: `new` and `update` refuse with exit 1 and output
`{refused: true, reason, claim_set_ref}` when the writing session is not
named in the committed claim set, or when the lane holds no claim
covering the record's path. The session is `--session ID`, else
`EOS_SESSION_ID`, else the record's `owner_session`. A repository with no
`org/claims.json` is not running the assigned-claims model and the
control does not apply. Unscheduled work stays quarantined on its branch
for the integrator to adopt or discard; it is never deleted without
operator authority.

## migrate

`migrate plan --seed PATH`: read-only against the seed; outputs
`migration-state.schema.json`. `migrate apply --state FILE
[--no-dry-run]`: without `--no-dry-run` it reports what it would do and
changes nothing; with it, the steps execute and advance their statuses.
This build runs on fixture seeds inside this repo only, and exits 2 if
pointed at a sibling repo. Exit 1 when any step ends blocked.

## benchmark

`benchmark prepare --task DIR --variant v1|v2 --run-id ID --dest DIR`:
materialises the task's fixture, places that variant's process surface
on it, writes `run.json` into the scratch tree and prints the task
prompt as JSON. It prepares a session; it does not run one. Running the
session and capturing its transcript is the operator's or the
orchestrator's job, and `benchmark/README.md` says so. This entry
previously claimed the command "executes one session ... recording the
transcript"; it did neither, and in fact could not run at all, because
`--variant` was passed into the fixture slot.
`benchmark score --task DIR --scratch DIR --transcript FILE --variant
V --run-id ID`: runs the task's criteria scripts and appends exactly
one row to `benchmark/results/ledger.json`
(`benchmark-result.schema.json`). The ledger is append-only: a
duplicate run_id is refused (exit 1) and nothing is ever rewritten.
Exit 1 also when any criterion fails.

## drills

Inputs: `--pack NAME` or `--all` to run, neither to list, plus optional
`--attempt DIR`, `--scratch DIR` and `--record`.

Listing outputs one row per drill: pack, spec path, recorded sha256,
whether the file still matches it, the criteria count, how many graders
exist, and `frozen_before_authoring`. That last flag is load-bearing. A
drill frozen before its pack was authored could not have been written
to; one frozen afterwards could, and a reader must be able to tell the
two apart without reading commit history.

Running materialises the drill's frozen scenario
(`benchmark/drills/scenarios/<pack>/`) into a scratch directory and
runs one grader (`benchmark/drills/graders/<pack>/cN.py`) per numbered
criterion. Neither directory exists yet, so every criterion currently
reports `manual` and every drill reports `pass: null`. `--attempt DIR` grades the tree a cold agent delivered
instead; without it the untouched fixture is graded, which proves the
criteria discriminate and proves nothing about a pack. The command
never runs the agent: that is the harness's job.

Output: `{pack, drill, pass, criteria}` with a `verdict` per criterion,
one of `pass`, `fail` or `manual`. `manual` means no grader exists for
that criterion, or the scenario could not be materialised, so the
criterion is prose a human must judge. A manual criterion is never
counted as a pass. It follows that `pass` is `false` when any criterion
failed, `true` only when every criterion was machine-evaluated and
passed, and `null` with a stated reason otherwise. A drill whose
criteria are all manual reports `null`, never a green.

`--record` appends one entry per drill to `benchmark/drills/RESULTS.json`,
which is append-only: rows are never rewritten or removed.

Exit 0 only when every requested drill passed outright. Exit 1 on any
failed criterion and on any drill left without a verdict, because a
drill that did not run is not a drill that passed. Exit 2 when the
command cannot run: no manifest, unknown pack, missing spec, or a spec
whose hash no longer matches the freeze.

A failed drill routes to fixing the pack and re-running; the spec
itself never changes without an ADR amendment.

## Shared behaviour

Commands never weaken, skip or delete a failing check. Commands that
write state use write-temp-then-rename and never hold live mutable
coordination files. Derived views (TASKS, STATE, indexes) are
regenerated only by `check --write-index` or the release playbook;
hand-edits are checker errors.
