---
summary: Subcommand contracts for python -m tools.eos, inputs, JSON outputs, exit codes
type: kernel
tags: [eos]
---

# CLI_CONTRACTS

Every command is invoked as `python -m tools.eos <cmd>` from the repo
root. Machine output is JSON on stdout and human-readable findings go
to stderr. Where a schema in `kernel/schemas/` governs the output, the
command's own section below names it; the rest is JSON with the shape
its section describes and no schema behind it.

Exit codes, uniform across commands, with one stated exception:
`benchmark` hands back the exit code of the frozen script it invokes,
so a missing task directory there reports 1 rather than 2.

- **0**: clean, or warnings only.
- **1**: findings (errors, refusals, blocking verdicts, failed criteria).
- **2**: cannot run (absent file, malformed input). Absent covers a file
  the caller named that is not there and a `--diff` range git cannot
  resolve; malformed covers a JSON input that will not parse and a task
  record the schema rejects. The message names the input and no
  traceback is printed, because a caller reads a traceback's exit 1 as
  findings. A missing
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
to run one series, `--relax-semantic` to drop the S-series to warnings
(error is the default, so `--strict-semantic` changes nothing except
overriding `--relax-semantic` where both are passed),
`--offline` to skip checks needing git remotes,
and `--json`. Output: a findings list `[{check, path, message, severity}]`.
`--series` filters on the id prefix, so `--series E` runs E001 upward
and nothing else; the seed D-series is not in that registry and runs
only under `--seed`. Any value outside that set is refused with exit 2:
a prefix match on an unknown letter selects no checks at all, so a typo
reported a clean tree.

`--write-index` regenerates every derived index to a fixpoint and is the
only sanctioned way to update them. Three are always written:
`INDEX.md`, `packs/INDEX.md` and the compatibility pointer
`packs/GUIDE_INDEX.md`. Where atomic Doctrine exists it also writes
`packs/DOCTRINE_INDEX.md`, `packs/WARGAME_INDEX.md` and
`registry/DOCTRINE_PRESSURE_MATRIX.md`; the alias view additionally needs
`registry/identifier-aliases.json`. `registry/CAPABILITIES.md` needs
`registry/coverage.json` and `registry/LESSONS.md` needs
`registry/lessons.json`. Exit 1 on any error-severity finding.

`--seed PATH` exits 2 rather than 1 when the run could not happen at
all: the seed path does not exist, or `kernel/SCALE_MATRIX.md` is
missing so nothing can say what the seed should contain. Those two
findings are named in `tools/eos/checks/seed.py` (`cannot_run`) so the
exit code follows the finding rather than a phrase in its message.
Everything else about a seed is a rubric failure and exits 1.

## route

Inputs: `--task T-####` or `--facts FILE` (declared facts JSON), plus
optional `--diff RANGE` for gate-time recomputation and `--adr ADR-####`
to acknowledge a protected-set touch. An unknown task id exits 2. With
neither `--task` nor `--facts` the command routes an empty fact set and
rules R0, which is the only answer available to a question with no facts
in it. R0 from an empty fact set is not R0 from facts that fired
nothing, and `task new` now prints which of the two it did, because on
21 of the first 25 task records it was the first and every reader of
those records had to infer it. Output: `{tier, reasons, discrepancies}` where `reasons`
rows follow `task-record.schema.json` and `discrepancies` lists derived
facts the declaration missed. Deterministic given the same inputs and
policy version. Gate-time recomputation only ever raises the ruling.
Exit 1 when discrepancies are found at the gate. Exit 3 when a reason
carries the factor `protected-set-contact` and no `--adr` was given;
the message names the file that matched.

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

## activate

Inputs: `--brief PATH`, a venture brief whose ```facts block carries the
declared venture facts; `--facts FILE`, a JSON list of predicates or an
object with a `predicates` key; and `--predicate NAME`, repeatable. Any
of the three may be given together and they union. None of them exits 2,
and so does a missing brief, a brief declaring no facts, or a facts file
that is not a list.

Output on stdout: `{declared, unknown_predicates, activated,
not_activated}`. An `activated` row carries the pack, its body path, the
predicates that matched and the ones still to confirm. A `not_activated`
row carries the pack and every predicate that would have activated it.

This is the half of pack activation `context` cannot compute. Path
triggers need a diff, and at Session 0 the venture has no history, which
is why `inception/WALK_ORDER.md` builds the walk by matching triggers
against the interview by hand. The same match from declared facts is
reproducible and testable.

`not_activated` is the pack-level record of what was considered and left
out. A compiled seed records what came in through the compile report's
ancestry, and D003 refuses a file with no reason to be there, but
nothing recorded the packs nobody loaded, so a reader could not tell a
pack ruled irrelevant from a pack nobody thought of.

Exit 1 when a declared predicate is owned by no pack. A misspelled fact
activates nothing and reads exactly like a fact that is false, so the
pack it should have loaded stays out and the seed ships without the
ruling. That is the expensive direction, so it fails rather than warns.

## doctrine

Operations are `list`, `show ID` and `match`. `--commit REF` reads the
same contracts from a pinned Git tree rather than the worktree. `list`
returns a compact catalogue with id, path, statement, authority,
applicability, challenge triggers and review; it deliberately omits bodies
and full metadata. `show` returns the complete metadata and body for one live
or aliased Doctrine identity. An unknown or wrong-kind identity exits 1.

`match` needs `--facts FILE` or at least one repeatable
`--fact NAME=true|false|unknown`. A facts file is an object, optionally under
a `facts` key. It returns applicable Doctrine summaries, required, candidate
and omitted Wargames, unresolved facts, uncovered pressures, the reason for
each selection and dependency-ordered packs. It never chooses the outcome.
Required and candidate rows are summaries. False omissions are compact
`{id, reason}` rows; use `show ID` when their full metadata is needed. This
keeps a selective result smaller than loading every Wargame it chose not to
run.
`--include WG-ID=reason` and `--omit WG-ID=reason` record an operator override;
the reason is required. Exit 1 when the resolver has an integrity problem or
a true or unknown declared pressure has no covering Wargame.

## wargame

The operations and flags are the same as `doctrine`: `list`, `show ID`,
`match`, `--commit`, `--facts`, repeatable `--fact`, `--include` and
`--omit`. `list` is a compact catalogue of both immutable `GD-*` and `WG-*`
identities, which are one semantic Wargame type. `show` returns one full
procedure. `match` returns the shared Doctrine and Wargame selection result,
because selective Session 0 needs both halves of the same decision surface.
New identities use `WG-*`; an existing `GD-*` remains valid and is never
renamed merely to change its type.

Pressure matching is tri-state. True engages the procedure. False records an
omission. Unknown high-consequence pressure engages or asks; unknown routine
pressure remains a candidate. An operator include or omission is preserved in
`selection_reasons`. A binding Doctrine is never waived by a Wargame result.

## id

`id resolve ID [--commit REF] [--rulings FILE]` resolves a canonical estate
identity, a compatibility alias or a retired definition through the same
commit-aware resolver used by checks, Session 0 and migration. Output is
`{id, resolved, canonical, kind, state, path, commit}`. Retired history
resolves with `state: retired` so provenance remains readable, but the
Rulings validator refuses it as a live selection. An unknown identity returns
`{id, resolved: false}` and exits 1.

`RUL-*` identity is document-scoped because ventures may use the same local
identifier without creating an estate collision. For a RUL identity the
command reads `docs/RULINGS.json` below the current directory, or the explicit
`--rulings FILE`, validates the whole document against its `eos_commit`, and
returns `scope: venture-document`. `--commit`, when supplied, must resolve to
that same EOS pin. Raw venture Rulings are not added to an EOS registry.

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
contract is a working file rather than a template: that flag exempts a
file from the semantic series, the freshness series and E008 alike, so a
contract still carrying it is one no checker ever reads.
Nothing is filled in and nothing is fetched: the lens contract is agreed
with the operator before the source is read (PB-E11).

Output: `{created, template, slots}`, where `slots` lists any `{{SLOT}}`
markers the copied template carries. `kernel/templates/LENS.tpl.md`
carries none: it prompts with prose blanks such as `- Agreed by:`
instead, so `slots` comes back empty for it and E008 has nothing to fire
on. Exit 0 on write, 1 when the target file already exists,
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
and its reasons, so no session needs a second routing command. An
unknown id exits 2 on `show` and on `update`.

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
because a generated view always names a commit behind HEAD. S020 covers
the case where there is no block at all: the generator writes a sentence
saying git facts were unavailable, and a view carrying that sentence in
a working copy where git resolves HEAD is stale output that E011 cannot
see, because it blanks the block and the sentence to the same token.

Refusal semantics: `new` and `update` refuse with exit 1 and output
`{refused: true, reason, claim_set_ref}` when the writing session is not
named in the committed claim set, or when the lane holds no claim
covering the record's path. The session is `--session ID`, else
`EOS_SESSION_ID`, else the record's `owner_session`. Two shapes mean the
assigned-claims model is not in force and the control does not apply: no
`org/claims.json` at all, and one holding no lanes. The second is
ADR-0008 decision 1, that a claim is required only where more than one
session may write at once and a session working alone is implicitly
claimed. A released claim set is committed with an empty lanes list
rather than deleted, and a compiled ORG seed ships one that way, so the
lone operator and a venture's first `task new` both pass. Where lanes are
present nothing is loosened. Unscheduled work stays quarantined on its branch
for the integrator to adopt or discard; it is never deleted without
operator authority.

## migrate

`migrate plan --seed PATH`: read-only against the seed; outputs
`migration-state.schema.json`.

`migrate apply --seed PATH --state FILE [--no-dry-run]`: both flags are
required. The state document cannot name its own seed, because
`migration-state.schema.json` fixes the key set and has no seed path in
it, so apply is told which seed to work on rather than guessing; without
`--seed` it exits 2 and says so. Dry run is the default, so `--dry-run`
is accepted and changes nothing about the behaviour; without
`--no-dry-run` apply reports what it would do and writes nothing, and
with it the steps execute and advance their statuses. This build runs on
fixture seeds inside this repo only, and exits 2 if pointed anywhere
else. The test is path containment, so a sibling directory whose name
merely extends this repository's is outside it too. Exit 1 when any step
ends blocked.

## benchmark

Both ops are subprocess wrappers over frozen scripts, and the frozen
script's exit code is what the caller gets. Missing flags are caught
here and exit 2; anything the script itself refuses carries the
script's own code, which for a task directory that is not there is 1.

`benchmark prepare --task DIR --variant v1|v2 --run-id ID --dest DIR`
drives `benchmark/harness.py`: it materialises the task's fixture,
places that variant's process surface on it, writes the run metadata
beside the scratch tree as `<dest>.run.json` rather than inside it, and
prints the task prompt as JSON. It prepares a session; it does not run
one. Running the session and capturing its transcript is the operator's
or the orchestrator's job, and `benchmark/README.md` says so.

`benchmark score --task DIR --scratch DIR --transcript FILE --variant
V --run-id ID` drives `benchmark/score.py`: it runs the task's criteria
scripts and appends exactly one row to `benchmark/results/ledger.json`
(`benchmark-result.schema.json`). The ledger is append-only: a
duplicate run_id is refused (exit 1) and nothing is ever rewritten.
A failed criterion does not change the exit code. The row is written
with the failure recorded in it and the command still exits 0, so read
the verdicts off the ledger row rather than off the exit status.

## drills

Inputs: `--pack NAME` or `--all` to run, neither to list, plus optional
`--attempt DIR`, `--scratch DIR` and `--record`.

Listing outputs one row per drill: pack, spec path, recorded sha256,
whether the file still matches it, the drill title, the criteria count,
how many graders exist, whether a scenario is on disk, whether the
drill is runnable (hash intact, scenario present, a grader for every
criterion), the freeze wave, and `frozen_before_authoring`. That last
flag is load-bearing. A drill frozen before its pack was authored could
not have been written to; one frozen afterwards could, and a reader
must be able to tell the two apart without reading commit history.
Listing exits 0, or 2 when any spec no longer matches its recorded
hash.

Running materialises the drill's frozen scenario
(`benchmark/drills/scenarios/<pack>/`) into a scratch directory and
runs one grader (`benchmark/drills/graders/<pack>/cN.py`) per numbered
criterion. Every pack has a scenario directory and a grader directory,
but not every criterion has a grader: where one is missing the
criterion reports `manual`, which is prose a human must judge and never
a pass. `--attempt DIR` grades the tree a cold agent delivered instead;
without it the untouched fixture is graded, which proves the criteria
discriminate and proves nothing about a pack. The command never runs
the agent: that is the harness's job.

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

A run exits 0 only when every requested drill passed outright. Exit 1
on any failed criterion and on any drill left without a verdict,
because a drill that did not run is not a drill that passed. Exit 2
when the command cannot run: no manifest, unknown pack, missing spec,
or a spec whose hash no longer matches the freeze.

A failed drill routes to fixing the pack and re-running; the spec
itself never changes without an ADR amendment.

## Shared behaviour

Commands never weaken, skip or delete a failing check. Commands that
write state use write-temp-then-rename and never hold live mutable
coordination files. The indexes and `registry/LESSONS.md` are
regenerated by `check --write-index` and the views `org/TASKS.md` and
`org/STATE.md` by `task views`; hand-edits to either set are checker
errors, caught by E001 and E011.
