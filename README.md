---
summary: What the PatterTech EOS is, who it is for, where it stands against its own gates, how the repo is laid out, and how a venture consumes it
type: root
tags: [eos]
---

# PatterTech EOS

The PatterTech Engineering Operating System. A documentation and process
repository, no build, that seeds our ventures and learns from them.

The point of it is that a capable agent can take a project from idea to
operated software to the standard of an experienced senior engineer,
with the operator supplying judgement at a few named gates rather than
repeating himself venture after venture.

It does that by putting engineering judgement in files: packs of argued
knowledge per domain, a kernel that decides how much ceremony a piece of
work deserves, registries of what is true today, and a governance layer
that lets all of it improve without rotting.

## At a glance

| Item | Where it stands |
| --- | --- |
| Version | 0.4.0. Nothing has been released from this line and no tag is cut |
| What 1.0 would mean | Walk-away ready, against the eight-item gate in ADR-0009 |
| Architecture of record | ADR-0002, extended by ADR-0006 and loosened by ADR-0008 |
| Knowledge | Atomic Doctrine in `packs/DOCTRINE_INDEX.md`, unified Wargames in `packs/WARGAME_INDEX.md`, and honest gaps in `registry/CAPABILITIES.md` |
| Evidence | `registry/evidence.json` is canonical and every live row must be cited |
| Ventures seeded | 3, listed in `registry/PROJECTS.md` |
| Checks | `python -m tools.eos check --repo` is the current answer; no copied total is treated as live state |
| Tests | The full pytest suite is the gate; the final programme receipt records the run |
| Licence | Apache-2.0 |

## Who this is for, and where to start

| You are | Start here |
| --- | --- |
| New to the system | `TOUR.md`. It teaches the system once, defines the words this repository uses in a particular way, and points at the canonical files as it goes |
| Running it | `OPERATORS_GUIDE.md`: what to launch, what to approve, and what to do when something looks wrong |
| After one worked example | `examples/v2-worked-lean.md`, a single task run start to finish |
| Starting a venture | The four steps under "From a clone to a seeded venture" |
| Already on a venture | That venture's lock-book first, then only the packs it cites |
| Working on the EOS itself | `org/STATE.md` for claims and flags, `org/TASKS.md` for the task table |

Two things to know before you read further.

**Ventures appear under placeholders.** Most ventures cited here appear
as Venture A, Venture B and so on, one placeholder per repository and
never two ventures folded into one. This repository and the public
website keep their real names. A worked ruling therefore still claims
what it always claimed, that a real venture argued a real fork on a real
date, and `registry/PROJECTS.md` carries the fuller note.

**It is Apache-2.0.** `LICENSE` at the root carries the terms and
`NOTICE` the attributions. `registry/LICENCE_RESIDUALS.md` is the honest
gap list behind that choice.

## Where this stands

### The version number

Nothing has been released from this line. v2 was merged and never
released and v2.1 folded into it (ADR-0007), and ADR-0009 renumbers the
result.

| Number | What it covers |
| --- | --- |
| 0.2.0 | the v2 overhaul |
| 0.3.0 | v2.1 |
| 0.4.0 | the tree you are reading |

The `v1.0.0` tag stays where it is, because it released the architecture
this one replaced, archived at `archive/v1-final`. 1.0 is reserved for
the eight-item gate in ADR-0009, which is what walking away from this
safely would take. Read this before trusting a number.

### The release gate

The release gate is now this, and nothing else:

- the checker green, with the semantic and freshness series
- the full test suite green
- the CHANGELOG written
- no false statement about the tree surviving the final review
- The operator's explicit approval under PB-E05

No benchmark gate is on it.

### What the benchmark showed

The evidence offered for the release is delivery quality. The benchmark
ran 103 sessions on 2026-08-08, 53 under v1 and 50 under v2.
**Fifty-three v1 runs produced fully passing work thirty-nine times.
Fifty v2 runs produced it fifty times.** Ceremony fell 77.3 per cent.

| Gate | Threshold | Result | |
| --- | --- | --- | --- |
| Ceremony lines | 60% fewer | 77.3% fewer | pass |
| Aggregate pass rate | no regression | 73.6% to 100% | pass |
| Completeness | 3 trials a slot | 12 slots, none short | pass |
| Context tokens | 30% fewer | 9.1% fewer | struck |
| Wall clock | 25% faster | 4.6% faster | struck |

The table is reproducible:

```
python benchmark/gates.py --baseline v1-2026-08-08 --candidate v2-2026-08-08
```

That is five of the eight gates in `benchmark/PROTOCOL.md`. Run bare,
`benchmark/gates.py` compares older variants and prints different
figures. Rows dated 2026-08-03 measured a variant that never reached the
tree and are kept as history, not as evidence.
`org/reports/V2_FINAL_REPORT.md` holds the method and the per-task
split.

### What the numbers do not cover

Efficiency is offered as unmeasured, and here is exactly what that
means.

**The two efficiency gates are struck, not met.** They were written to
compare two kernels under a frozen harness. The system they were meant
to judge has changed shape since, and the instrument that would re-judge
it is not being run, so ADR-0007 strikes them with that reason recorded.
A struck gate is not a met gate and no file here may call it one. The
9.1 and 4.6 per cent figures are recorded as achieved, not as passed.

**No measurement of the current system exists.** No benchmark run was
made during the v2.1 work, so every figure above measures the v2 tree as
it stood on 2026-08-08 and none of them measures what you are reading.
Amending the thresholds to match the figures already achieved would be
tuning the target to the result, so it was not done.

**The sealed suite is retired unopened.** `SEALED-BENCH-2026-08` runs
once, needs the operator's private key, and was authored for a comparison this
release supersedes. It stays in the tree with its hashes, the key stays
with the operator, and a future sealed evaluation is written fresh against
whatever it is meant to judge. Two of the protocol's eight gates
depended on it and are therefore uncomputed. That is a real reduction in
assurance against the plan ADR-0002 approved, accepted knowingly.

**Three policy ablations never ran** (`v2-wip1`, `v2-mandatory-logs`,
`v2-no-sampled-review`). They are the designed instrument for isolating
residual ceremony overhead, and they move to the optional post-release
list.

### What the drills and the guard do not yet prove

**No drill has returned a pack verdict.** Twenty-seven specs are
frozen. Twenty-two carry a scenario and graders, and fifteen of those
have a grader for every criterion, which makes a verdict possible
without being one. On 2026-08-15 those twenty-two ran against their
untouched fixtures and every one failed, so the append-only ledger no
longer holds only nulls. The other five were frozen the same day before
their packs existed and have no scenario yet, so they cannot be run at
all, which their ledger rows say rather than reporting a failure. Those rows are marked
`graded: scenario-baseline`, which says they are the criteria proving
they discriminate and not a judgement on any pack. The fourth
ingredient, a cold-agent session, is still a spend decision, deferred,
and not a release blocker.

**The graders live in the tree a drill drops an agent into**, with no
holdout exclusion of the kind `benchmark/fixtures` has. A harness
decision, deliberately left open rather than settled quietly.

**The action-time guard grants nothing autonomous.** Its one shipped
host adapter was validated at mapping level, offline, on 2026-08-03.
That run proved the mapping, not that a live session's hooks fire.
Three of the ten guarded classes are covered and all three rule
require-approval, so even those resolve only on a recorded operator
decision. `TOUR.md` explains the two layers and `OPERATORS_GUIDE.md`
says what it means at the keyboard.

### Live state

`org/STATE.md` carries the live claims and operator flags, `org/TASKS.md`
the task table. Both are derived: fix the record under `org/tasks/` and
regenerate, never hand-edit the view.

A claim is needed when more than one session may write at once; a
session working alone is implicitly claimed (ADR-0008).
`OPERATORS_GUIDE.md` says how a claim is made and what the empty claim
file in this repository does to `task new`.

## Installing and running the checks

You need Python 3.11 or newer and two libraries.

```
python -m pip install --require-hashes -r tools/requirements-dev.txt
python -m tools.eos check --repo
python -m pytest -q
```

Run both commands. A copied test count or checker summary would become a
second, stale source of truth, so this file does not carry one.

If yours reports errors, that is the finding, not the code you were
about to read. The common one is a derived file left stale by an edit to
its source, which `python -m tools.eos check --write-index` fixes.

Nothing here runs at commit time. There is no pre-commit hook in this
repository, so a voice slip or a stale index is caught by the checker
when you run it and by CI when you push.

### What CI runs

CI runs the same checks on Ubuntu and Windows against Python 3.11 and
3.14, from `.github/workflows/checks.yml`, on every push and pull
request, and installs from the same hash-locked file the command above
names.

### Which platforms the lock covers

The lock carries every wheel hash for linux-x86_64, windows-amd64 and
macos-arm64 on CPython 3.11 and 3.14. Intel macOS is not covered,
because rpds-py publishes no wheel for it and asking for one walks pip
back to a six-year-old release. On a platform outside that set the
install fails the hash check, which is the intended answer rather than
a quiet unpinned install.

### The commands worth knowing

Each of these is `python -m tools.eos` followed by the arguments below.

| Arguments | What it answers |
| --- | --- |
| `check --repo` | is the tree self-consistent |
| `check --write-index` | regenerate the derived indexes after editing a source |
| `route --facts FILE` | what tier a piece of work rules, and on which facts |
| `activate --brief PATH` | which packs a venture's declared facts activate, and which they do not |
| `doctrine list`, `show ID`, `match --facts FILE` | which standing rules exist, what one says, and which apply to the declared facts |
| `wargame list`, `show ID`, `match --facts FILE` | which decision procedures exist and which pressures make them required or worth considering |
| `id resolve ID --commit REF` | where an immutable live, aliased, retired or historically pinned identity resolves; `--rulings FILE` resolves a venture-local RUL record |
| `migrate plan/apply` | plan a lossless legacy Ruling migration, then apply an inspected state explicitly; dry-run is the default |
| `drills` | list the frozen drills, their hashes, and which were frozen before their pack was authored |

`activate` also takes `--facts FILE` or a repeatable `--predicate NAME`,
and the names it accepts are the controlled vocabulary in
`kernel/PREDICATES.md`. `tools/CLI_CONTRACTS.md` is the contract for
every command and its exit codes, and three tests hold it there.

### From a clone to a seeded venture

Four steps, and no other document collects them:

1. Clone this repository and run the three commands above.
2. Read `TOUR.md`.
3. Run launcher L2 in `OPERATORS_GUIDE.md` from the new venture's own
   repository. That is Session 0, and it ends with a compiled seed you
   sign.
4. Run L3 for Genesis if you want the build blueprint.

Everything after that happens in the venture's repository, not this one.

## Map

| Path | What lives there |
| --- | --- |
| `AGENTS.md` / `CLAUDE.md` | The router: entry modes and the never-list, byte identical, capped at forty lines |
| `TOUR.md` | The teaching surface, rewritten by hand each release |
| `GOVERNANCE.md` | The graded change path, precedence, promotion, the protected set |
| `OPERATORS_GUIDE.md` | The operator's manual: launchers, approval duties, the guard, the monthly pass |
| `packs/` | The knowledge: pack maps, atomic Doctrine, Wargames and their supporting material. `packs/INDEX.md` is the always-loaded surface |
| `packs/DOCTRINE_INDEX.md` | Generated catalogue of every atomic Doctrine and its authority grade |
| `packs/WARGAME_INDEX.md` | Generated public index of every Wargame, including immutable `GD-*` identities |
| `packs/GUIDE_INDEX.md` | Compatibility pointer for the retired Guide name |
| `packs/PACK_SHAPE.md` | The contract a pack keeps, including the eleven-point definition of done |
| `kernel/` | Policy, guard and metadata law, the scale matrix, the seed rubric, schemas, and the templates a seed compiles from |
| `kernel/PREDICATES.md` | The controlled vocabulary of activation predicates, one name per fact (ADR-0010) |
| `inception/` | Session 0 and Genesis: interview, scale, walk order, compile, blueprint |
| `examples/` | Worked task runs, historical reseeds, and `current-head-seed`, which proves the current structured Ruling path |
| `org/` | The EOS's own state: task records, claims, cadence, decision records, playbooks and historical logs |
| `registry/` | Projects, capabilities, evidence, lessons, vendors, stack profiles |
| `registry/coverage.json` | The canonical domain coverage matrix, so an omission is a row rather than silence |
| `registry/evidence.json` | The canonical source ledger; the checker refuses uncited live rows |
| `registry/lessons.json` | What we studied, what was decided, and what was rejected and why |
| `registry/DOCTRINE_PRESSURE_MATRIX.md` | Generated view of typed Doctrine relations and the accepted pressure backlog |
| `estate/` | Which repos exist, which the EOS governs, and which were left out on whose ruling |
| `benchmark/` | The frozen v1-against-v2 protocol, fixtures, drills and results |
| `tools/` | The one executable, `python -m tools.eos`, version 0.4.0 |
| `archive/` | A pointer to the `archive/v1-final` tag, where the whole v1 tree lives |
| `LICENSE`, `NOTICE` | Apache-2.0, and the attributions behind it |
| `INDEX.md` | Derived index of every live file, one row each, grep the tag column |

## How a venture consumes the EOS

### Session 0 compiles a seed

A venture never reads this repo at random. Session 0 activates packs,
inherits applicable Doctrine and runs only the always-walk or
pressure-matched Wargames. Unknown high-consequence facts are asked or
included, not quietly treated as false. The resulting selections,
omissions and argued outcomes live in `docs/RULINGS.json`.

Session 0 then compiles the seed: a thin router, a lock-book pointing at
that Ruling record, the distilled standards it needs and, at ORG scale,
an org kernel. `kernel/SCALE_MATRIX.md` is the law of what that contains,
and the seed is stamped with the EOS commit it came from. Inherited
defaults do not create hundreds of empty Ruling rows.

Genesis then turns that seed into a build blueprint inside the venture's
own repository: research packets, a product map with a dependency graph,
work packages, and a failing acceptance spine.

### Then the EOS lets go

It compiles a seed and a blueprint and stops. There is no standing
obligation on a venture to stay in line with this repository, and no
standing obligation on this repository to keep it there.

Ventures diverge freely, for their own good reasons, and the guidance
they were born with is advice they may discard. The EOS never initiates
contact.

### Check-ins and upgrades are the venture's call

A check-in happens only when a venture asks for one. It reviews the
venture against current guidance, returns findings and candidate
lessons, and applies nothing.

Pulling a newer version of the EOS is the same kind of thing. The
venture pins the commit it compiled from and never auto-upgrades, and an
upgrade is a deliberate run of the upgrade playbook that the venture
chooses to start. `GOVERNANCE.md` sets what a pin must resolve to.

### Reading the venture directory

`registry/PROJECTS.md` is the venture directory, three rows today. Read
its standing note before reading a status line: it records what was true
when a venture was born and when somebody last looked, not what is true
now. A stale status line there is a stale reading, not a venture in
breach.

Working agents read the venture's own files first and follow citations
back here. Nothing in this repo is read by a venture at runtime.

## Principles

What must stay true as the EOS grows.

- **Agnostic core, locked-in ventures.** EOS files never assume one
  brand, stack or client. Each venture freezes its choices in its own
  lock-book. A rule that only makes sense for one venture belongs in a
  privacy-reviewed Ruling summary or an exemplar, not in estate Doctrine.
- **Evidence before authority.** A rule earns its place by surviving
  argument and citing sources, not by being written confidently.
  Promotion has numbers and demotion exists (`GOVERNANCE.md`). A
  rejected lesson keeps its reason, so nobody can propose it forever.
- **Never describe a control you have not built.** Sixty-six false
  statements about this tree got into it once. An honest gap is cheaper
  than a confident sentence, and the standing section above is what that
  costs in prose.
- **The venture is sovereign.** The EOS is a library and a midwife, not
  a landlord. It compiles a seed and a blueprint at birth and then
  stops. Guidance a venture was born with is advice it may discard.
- **Files over memory.** Everything an agent needs is in the repos.
  Session memory is a convenience, never the source of truth.
- **Doctrine stands; registries date.** Atomic Doctrine carries standing
  propositions and authority. Named tools, tested versions and other
  time-sensitive facts belong in dated stack or evidence records.
- **Ceremony is proportional to risk.** The router rules a tier from
  semantic facts, and the tier decides the paperwork. A doc fix does not
  pay for a schema migration's assurance.
- **Compiled, never composed.** Ventures are seeded by slot-filling
  hand-written templates, with a compile report proving ancestry.
- **Ventures feed back when they choose to.** Only privacy-reviewed
  summaries are harvested from ventures that share them. Repeated argued
  Rulings may support promotion; defaults become binding only with an ADR.
- **Lean.** Capture the decision structure, not restatements of common
  knowledge. If removing a line would not cause a mistake, cut it.
