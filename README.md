---
summary: What the PatterTech EOS is, where it stands against its own gates, how the repo is laid out, how a venture consumes it, and the principles that hold
type: root
tags: [eos]
---

# PatterTech EOS

The PatterTech Engineering Operating System. A documentation and process
repository, no build, that seeds our ventures and learns from them, so a
capable agent can take a project from idea to operated software to the
standard of an experienced senior engineer, with Daniel supplying
judgement at a few named gates rather than repeating himself venture
after venture.

It does that by putting engineering judgement in files: packs of argued
knowledge per domain, a kernel that decides how much ceremony a piece of
work deserves, registries of what is true today, and a governance layer
that lets all of it improve without rotting. The architecture of record
is `org/decisions/ADR-0002-eos-v2-adaptive-agentic-development.md`,
extended by ADR-0006 and loosened by ADR-0008.

New here? Read `TOUR.md`. It teaches the system, says what changed from
v1 and why, and points at the canonical files as it goes. To start a
venture, run `inception/INCEPTION.md`, then `inception/GENESIS.md` for
the build blueprint. To see one task run start to finish first, read
`examples/v2-worked-lean.md`.

Licensed under Apache-2.0. `LICENSE` at the root carries the terms and
`NOTICE` carries the attributions.

## Where this stands

v2 was merged and never released. v2.1 folded into it, and the two ship
as one release (ADR-0007). Read this before trusting a number.

You need Python 3.11 or newer and two libraries:

```
python -m pip install --require-hashes -r tools/requirements-dev.txt
```

Then run `python -m tools.eos check` and `python -m pytest -q`. Both
should be clean. If they are not, that is the finding, not the code you
were about to read.

**The release gate is now this**, and nothing else: the checker green
with the semantic and freshness series, the full test suite green, the
CHANGELOG written, no false statement about the tree surviving the final
review, and Daniel's explicit approval under PB-E05.

The evidence offered for the release is delivery quality. The benchmark
ran 103 sessions on 2026-08-08, 53 under v1 and 50 under v2.
**Fifty-three v1 runs produced fully passing work thirty-nine times.
Fifty v2 runs produced it fifty times.** Ceremony fell 77.3 per cent.
The table below is reproducible:

```
python benchmark/gates.py --baseline v1-2026-08-08 --candidate v2-2026-08-08
```

| Gate | Threshold | Result | |
| --- | --- | --- | --- |
| Ceremony lines | 60% fewer | 77.3% fewer | pass |
| Aggregate pass rate | no regression | 73.6% to 100% | pass |
| Completeness | 3 trials a slot | 12 slots, none short | pass |
| Context tokens | 30% fewer | 9.1% fewer | struck |
| Wall clock | 25% faster | 4.6% faster | struck |

Efficiency is offered as unmeasured, and here is exactly what that
means:

- **The two efficiency gates are struck, not met.** They were written
  to compare two kernels under a frozen harness. The system they were
  meant to judge has changed shape since, and the instrument that would
  re-judge it is not being run, so ADR-0007 strikes them with that
  reason recorded. A struck gate is not a met gate and no file here may
  call it one. The 9.1 and 4.6 per cent figures are recorded as
  achieved, not as passed.
- **No measurement of the evolved system exists.** No benchmark run was
  made as part of the v2.1 work. Amending the thresholds to match the
  figures already achieved would be tuning the target to the result, so
  it was not done.
- **The sealed suite is retired unopened.** `SEALED-BENCH-2026-08` runs
  once, needs Daniel's private key, and was authored for a comparison
  this release supersedes. It stays in the tree with its hashes, the key
  stays with Daniel, and a future sealed evaluation is written fresh
  against whatever it is meant to judge. Two of the protocol's eight
  gates depended on it and are therefore uncomputed. That is a real
  reduction in assurance against the plan ADR-0002 approved, accepted
  knowingly.
- **No drill reports a verdict.** All twenty-two have a scenario and
  graders, and graders make a verdict possible without being one.
  Running them is a spend decision, deferred, and it is not a release
  blocker.
- **The graders live in the tree a drill drops an agent into**, with no
  holdout exclusion of the kind `benchmark/fixtures` has. A harness
  decision, deliberately left open rather than settled quietly.
- **Three policy ablations never ran** (`v2-wip1`, `v2-mandatory-logs`,
  `v2-no-sampled-review`). They are the designed instrument for
  isolating residual ceremony overhead, and they move to the optional
  post-release list.

Run bare, `gates.py` compares older variants and prints different
figures. Rows dated 2026-08-03 measured a variant that never reached the
tree and are kept as history, not as evidence.
`org/reports/V2_FINAL_REPORT.md` holds the method and the per-task
split.

`org/STATE.md` carries the live claims and operator flags, `org/TASKS.md`
the task table. Both are derived: fix the record under `org/tasks/` and
regenerate, never hand-edit the view. A claim is needed when more than
one session may write at once; a session working alone is implicitly
claimed (ADR-0008). `OPERATORS_GUIDE.md` says how a claim is made.

## Map

| Path | What lives there |
| --- | --- |
| `AGENTS.md` / `CLAUDE.md` | The router: entry modes and the never-list, byte identical |
| `TOUR.md` | The teaching surface, rewritten by hand each release |
| `GOVERNANCE.md` | The graded change path, precedence, promotion, the protected set |
| `OPERATORS_GUIDE.md` | The operator's manual: launchers, approval duties, the guard, cadences |
| `packs/` | The knowledge, twenty-one domains. `packs/INDEX.md` is the always-loaded surface |
| `packs/agentic-swarm/` | How we build wide: dependency-graph partitions, lanes, one integrator |
| `kernel/` | Policy, guard and metadata law, schemas, and the templates a seed compiles from |
| `inception/` | Session 0 and Genesis: interview, scale, walk order, compile, blueprint |
| `examples/` | One task run end to end, lean and high-assurance |
| `org/` | The EOS's own state: task records, claims, decisions, playbooks, logs |
| `registry/` | Projects, capabilities, evidence, lessons, vendors, stack profiles |
| `registry/lessons.json` | What we studied, what was decided, and what was rejected and why |
| `estate/` | Which repo owns what, and which repos the EOS governs |
| `benchmark/` | The frozen v1-against-v2 protocol, fixtures, drills and results |
| `tools/` | The one executable, `python -m tools.eos` |
| `archive/` | A pointer to the `archive/v1-final` tag, where the whole v1 tree lives |
| `LICENSE`, `NOTICE` | Apache-2.0, and the attributions behind it |
| `INDEX.md` | Derived index of every file, grep the tag column |

## How a venture consumes the EOS

A venture never reads this repo at random. Session 0 compiles it a seed
pack: a thin router, a lock-book of its rulings, the distilled standards
it needs and, at ORG scale, an org kernel. The seed is stamped with the
EOS commit it came from. Genesis then turns that seed into a build
blueprint inside the venture's own repository: research packets, a
product map with a dependency graph, work packages, and a failing
acceptance spine.

**Then the EOS lets go.** It compiles a seed and a blueprint and stops.
There is no standing obligation on a venture to stay in line with this
repository, and no standing obligation on this repository to keep it
there. Ventures diverge freely, for their own good reasons, and the
guidance they were born with is advice they may discard. The EOS never
initiates contact.

A check-in happens only when a venture asks for one. It reviews the
venture against current guidance, returns findings and candidate
lessons, and applies nothing. Pulling a newer version of the EOS is the
same kind of thing: the venture pins the commit it compiled from and
never auto-upgrades, and an upgrade is a deliberate run of the upgrade
playbook that the venture chooses to start. `GOVERNANCE.md` sets what a
pin must resolve to.

Working agents read the venture's own files first and follow citations
back here. Nothing in this repo is read by a venture at runtime.

## Principles

What must stay true as the EOS grows.

- **Agnostic core, locked-in ventures.** EOS files never assume one
  brand, stack or client. Each venture freezes its choices in its own
  lock-book. A rule that only makes sense for one venture belongs in a
  worked ruling or an exemplar, not in a pack.
- **Evidence before authority.** A rule earns its place by surviving
  argument and citing sources, not by being written confidently.
  Promotion has numbers and demotion exists (`GOVERNANCE.md`). A
  rejected lesson keeps its reason, so nobody can propose it forever.
- **The venture is sovereign.** The EOS is a library and a midwife, not
  a landlord. It compiles a seed and a blueprint at birth and then
  stops. Guidance a venture was born with is advice it may discard.
- **Files over memory.** Everything an agent needs is in the repos.
  Session memory is a convenience, never the source of truth.
- **Packs argue; registries date.** Timeless rules and dated facts never
  share a file. Time-sensitive claims carry a review trigger, and stale
  guidance is a bug.
- **Ceremony is proportional to risk.** The router rules a tier from
  semantic facts, and the tier decides the paperwork. A doc fix does not
  pay for a schema migration's assurance.
- **Compiled, never composed.** Ventures are seeded by slot-filling
  hand-written templates, with a compile report proving ancestry.
- **Ventures feed back when they choose to.** Rulings and lessons are
  harvested from the ventures that share them, repeated argued rulings
  become defaults, and defaults become binding only with an ADR.
- **Lean.** Capture the decision structure, not restatements of common
  knowledge. If removing a line would not cause a mistake, cut it.
