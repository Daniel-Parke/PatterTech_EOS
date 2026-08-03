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

Inputs: `--repo` (default), `--seed PATH`, `--write-index`, optional
`--json`. Runs the E (structural), S (semantic), D (seed) and F
(freshness) series. Output: a findings list `[{check, path, message,
severity}]`. `--write-index` regenerates the derived indexes and is the
only sanctioned way to update them. Exit 1 on any error-severity
finding, 3 if regeneration would touch protected content unacknowledged.

## route

Inputs: `--task T-####` or `--facts FILE` (declared facts JSON), plus
optional `--diff RANGE` for gate-time recomputation. Output: `{tier_ruled,
reasons, discrepancies}` where `reasons` rows follow
`task-record.schema.json` and `discrepancies` lists derived facts the
declaration missed. Deterministic given the same inputs and policy
version. Gate-time recomputation only ever raises the ruling. Exit 1
when discrepancies are found at the gate.

## guard eval

Inputs: `--class CLASS --payload SUMMARY`, or `--tool NAME --input FILE`
for adapter use. Output: one document per
`guard-action.schema.json`. Without a validated adapter every guarded
class rules manual-only (fail closed). Exit 0 for allow, 1 for any
blocking verdict, 2 when evaluation itself cannot run.

## context

Inputs: `--task T-####` or `--diff RANGE`. Output: the changed-surface
context packet as Markdown on stdout, at most 300 lines: touched files,
owning packs, applicable rules, affected tests from the test map.
Unchanged context is never re-supplied within a run.

## task

Record ops: `new`, `show`, `update`, `close`, each reading and writing
`org/tasks/T-####.json` (`task-record.schema.json`) via
write-temp-then-rename. Claim ops: `claims assign` (integrator only:
writes `org/claims.json` per `claims.schema.json` for commit before
dispatch), `claims verify` (compares a lane's actual diff against its
assigned claims; exit 1 on any file outside them), `claims renew`
(only within the renewal window), `claims recover` (requires liveness
evidence: harness state or a dead PID on the recorded host; a
timestamp alone is refused and the command directs to operator
recovery).

View op: `views` (integrator only) regenerates the derived
`org/TASKS.md` and `org/STATE.md` from the task records, claims,
cadence rows and git facts; hand-edits to those views are checker
errors.

Refusal semantics: when the invoking session is not named in the
committed unexpired claim set, `new`, `update` and `close` refuse with
exit 1 and output `{refused: true, reason, claim_set_ref}`. Unscheduled
work stays quarantined on its branch for the integrator to adopt or
discard; it is never deleted without operator authority.

## migrate

`migrate plan --venture NAME`: read-only against the venture; writes
only a committed plan report in this repo and outputs
`migration-state.schema.json`. `migrate apply --state FILE`: executes
the steps and advances their statuses; this build it runs on fixture
seeds only, and it exits 2 if pointed at a sibling repo. Exit 1 when
any step ends blocked.

## benchmark

`benchmark run --task DIR --variant v1|v2`: executes one session
against the task's fixture under its frozen budgets
(`benchmark-task.schema.json`), recording the transcript.
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
criterion. `--attempt DIR` grades the tree a cold agent delivered
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
