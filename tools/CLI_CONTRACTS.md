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
- **2**: cannot run (absent file, malformed input). A missing
  `jsonschema` is not one of these. Schema validation degrades instead:
  S013, S017, S019 on the repo path and D007 and D009 on the seed path
  each emit an error-severity finding naming what went unvalidated, so
  the run finishes and exits 1 with the rest of its findings. A library
  that stopped the run would throw away everything already collected,
  which is the failure that shape avoids.
- **3**: protected-touch-unacknowledged: `route` ruled the factor
  `protected-set-contact` and no `--adr` was given. That factor is
  activated by a changed path matching a glob in the policy's
  `path_patterns.protected` list, which is the only thing that raises
  this exit code. The command checks only that a value was passed;
  nothing yet reads the id or confirms the ADR is accepted, so the
  operator carries that check. A policy's `protected_pointers` list is a
  declaration, validated against `kernel/schemas/policy.schema.json` by
  the seed check D007; no command reads it to rule a touch, so a change
  that reaches a pointer target without also matching a protected path
  does not raise this code.

## check

Inputs: `--repo` (the default; passing it with `--seed` exits 2 because
they are different runs), `--seed PATH`, `--write-index`, `--series E|S|F|B`
to run one series, `--strict-semantic` and `--relax-semantic` to pin or
drop the S-series severity, `--offline` to skip checks needing git remotes,
and `--json`. Output: a findings list `[{check, path, message, severity}]`.
`--write-index` regenerates every derived index to a fixpoint and is the
only sanctioned way to update them; the set is `INDEX.md`,
`packs/INDEX.md`, `packs/GUIDE_INDEX.md`, `registry/CAPABILITIES.md` and,
once `registry/lessons.json` exists, `registry/LESSONS.md`. Exit 1 on any
error-severity finding.

`--seed PATH` exits 2 rather than 1 when the run could not happen at
all: the seed path does not exist, or `kernel/SCALE_MATRIX.md` is
missing so nothing can say what the seed should contain. Those two
findings are named in `tools/eos/checks/seed.py` (`cannot_run`) so the
exit code follows the finding rather than a phrase in its message.
Everything else about a seed is a rubric failure and exits 1.

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
for adapter use, plus `--adapter-validated` to assert the host adapter
hook. Without that flag the caller is treated as having no adapter.
Output: one document per
`guard-action.schema.json`. Without a validated adapter every guarded
class rules manual-only (fail closed). Exit 0 for allow, 1 for any
blocking verdict, 2 when evaluation itself cannot run.

## context

Inputs: `--diff RANGE`, and optionally `--task T-####`, whose record
supplies the declared `applies_when` predicates that gate pack
activation. An unknown task id exits 2. Output: the changed-surface context packet as
JSON on stdout, truncated to 300 lines: `{changed, summaries,
referencing_files, activated_packs, routed}`. Unchanged context is never
re-supplied within a run.

## study

Inputs: `--out DIR` and optional `--name NNNN`. Copies
`kernel/templates/LENS.tpl.md` into `DIR/LENS.md`, or `DIR/LENS-<name>.md`
with a name, so two studies can share a directory; the venture convention
is `docs/lenses/`. The id form is `LENS-NNNN`, four digits, which is what
`kernel/schemas/lesson.schema.json` enforces on the `lens` field a study
lesson carries, so pass the number and `--name 0002` writes
`LENS-0002.md`. The command does not check the form: whatever `--name`
carries lands in the filename, so a slug there produces a contract no
lesson row can cite. The copy drops `template: true`, because a scaffolded
contract is a working file and has to stay under the unfilled-slot check.
Nothing is filled in and nothing is fetched: the lens contract is agreed
with the operator before the source is read (PB-E11).

Output: `{created, template, slots}`, where `slots` lists any `{{SLOT}}`
still to fill. Exit 0 on write, 1 when the target file already exists,
which is refused rather than overwritten, and 2 when the kernel template
is absent.

## task

Record ops: `new --record FILE`, `show --id T-####` and
`update --id T-#### --patch JSON`, each reading and writing
`org/tasks/T-####.json` (`task-record.schema.json`) via
write-temp-then-rename. `--patch` is a JSON object shallow-merged into
the record, except `timestamps`, which merges one level deeper. A record
is closed by `update` setting its status; there is no separate `close`
op. `new` routes the record as it writes it and prints the ruled tier
and its reasons, so no session needs a second routing command.

Claim ops: `claims-verify --lane ID --paths ...` compares a lane's diff
against its assigned claims and exits 1 on any file outside them.
`org/claims.json` is written by the integrator by hand and committed
before dispatch; there is no `claims assign`, `renew` or `recover`
command. Recovery of an expired claim needs liveness evidence and the
operator, and a timestamp alone never authorises it.

View op: `views` (integrator only) regenerates the derived
`org/TASKS.md` and `org/STATE.md` from the task records, claims,
cadence rows and git facts; hand-edits to those views are checker
errors. Check E011 is what makes that true: it rebuilds both views and
compares, byte for byte up to the state view's machine-facts block. The
block itself is S007's, which tests the recorded commit by ancestry
because a generated view always names a commit behind HEAD.

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
[--no-dry-run]`: dry run is the default, so `--dry-run` is accepted and
changes nothing about the behaviour; without `--no-dry-run` it reports
what it would do and writes nothing, and with it the steps execute and
advance their statuses.
This build runs on fixture seeds inside this repo only, and exits 2 if
pointed at a sibling repo. Exit 1 when any step ends blocked.

## benchmark

`benchmark prepare --task DIR --variant v1|v2 --run-id ID --dest DIR`:
materialises the task's fixture, places that variant's process surface
on it, writes the run metadata beside the scratch tree as
`<dest>.run.json` rather than inside it, and prints the task
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
A failed criterion does not change the exit code. The row is written
with the failure recorded in it and the command still exits 0, so read
the verdicts off the ledger row rather than off the exit status.

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
criterion. Both directories now exist, one per pack for all twenty-two
drills, so a criterion with a grader reports `pass` or `fail` and
`manual` is left for the criteria no grader covers. `--attempt DIR` grades the tree a cold agent delivered
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
coordination files. The indexes and `registry/LESSONS.md` are
regenerated by `check --write-index`, the views org/TASKS.md and
org/STATE.md by `task views`, and by the release playbook; hand-edits
are checker errors, caught by E001 and E011.
