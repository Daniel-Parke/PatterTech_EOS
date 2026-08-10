---
summary: What the PatterTech EOS is, where it stands against its own gates, how the repo is laid out, how a venture consumes it, and the principles that hold
type: root
tags: [eos]
---

# PatterTech EOS

The PatterTech Engineering Operating System. A documentation and process
repository, no build, that seeds and governs our ventures so a capable
agent can take a project from idea to operated software to the standard
of an experienced senior engineer, with Daniel supplying judgement at a
few named gates rather than repeating himself venture after venture.

It does that by putting engineering judgement in files: packs of argued
knowledge per domain, a kernel that decides how much ceremony a piece of
work deserves, registries of what is true today, and a governance layer
that lets all of it improve without rotting. The architecture of record
is `org/decisions/ADR-0002-eos-v2-adaptive-agentic-development.md`.

New here? Read `TOUR.md`. It teaches the system, says what changed from
v1 and why, and points at the canonical files as it goes. To start a
venture, run `inception/INCEPTION.md`. To see one task run start to
finish first, read `examples/v2-worked-lean.md`.

## Where this stands

v2 is merged and unreleased. Read this before trusting a number.

You need Python 3.11 or newer and two libraries:

```
python -m pip install --require-hashes -r tools/requirements-dev.txt
```

Then run `python -m tools.eos check` and `python -m pytest -q`. Both
should be clean. If they are not, that is the finding, not the code you
were about to read.

The benchmark ran 103 sessions on the encoded harness, 53 under v1 and
50 under v2. This table is reproducible:

```
python benchmark/gates.py --baseline v1-2026-08-08 --candidate v2-2026-08-08
```

| Gate | Threshold | Result | |
| --- | --- | --- | --- |
| Ceremony lines | 60% fewer | 77.3% fewer | pass |
| Aggregate pass rate | no regression | 73.6% to 100% | pass |
| Completeness | 3 trials a slot | 12 slots, none short | pass |
| Context tokens | 30% fewer | 9.1% fewer | **fail** |
| Wall clock | 25% faster | 4.6% faster | **fail** |

Run bare, `gates.py` compares older variants and prints different
figures. Three of five computable gates pass. The two efficiency gates
miss on a mixed picture rather than a uniformly bad one: on context
tokens v2 is cheaper on seven of the twelve tasks and dearer on five.
The protocol sets eight gates; the three missing here are uncomputed
rather than failed, for the reasons below. Rows dated 2026-08-03
measured a variant that never reached the tree and are kept as history,
not as evidence. `org/reports/V2_FINAL_REPORT.md` holds the method and
the per-task split.

What is not proven, and is not pretended otherwise:

- **The sealed suite has never been opened.** It needs Daniel's key and
  runs once. Two of the eight gates depend on it, so they are uncomputed
  rather than passed.
- **No drill reports a verdict.** All twenty-two have a scenario and
  graders, and graders make a verdict possible without being one. That
  needs twenty-two cold-agent sessions, and it is the third uncomputed
  gate.
- **The graders live in the tree a drill drops an agent into**, with no
  holdout exclusion of the kind `benchmark/fixtures` has. A harness
  decision, deliberately left open rather than settled quietly.
- **Three policy ablations never ran** (`v2-wip1`, `v2-mandatory-logs`,
  `v2-no-sampled-review`). They are the designed instrument for
  isolating residual ceremony overhead.
- **Four descriptions in protected files are known wrong.** ADR-0005
  records them and is proposed, not accepted, so the wrong text stands.
  Two of the four compile into every ORG seed.

No licence is declared, at the root or in `tools/pyproject.toml`, which
this repository's own `packs/legal-licensing/PACK.md` B1 requires of
every repository.

`org/STATE.md` carries the live claims and operator flags, `org/TASKS.md`
the task table. Both are derived: fix the record under `org/tasks/` and
regenerate, never hand-edit the view. Writing anything here needs a
claim; `OPERATORS_GUIDE.md` says how one is made.

## Map

| Path | What lives there |
| --- | --- |
| `AGENTS.md` / `CLAUDE.md` | The router: entry modes and the never-list, byte identical |
| `TOUR.md` | The teaching surface, rewritten by hand each release |
| `GOVERNANCE.md` | The graded change path, precedence, promotion, the protected set |
| `OPERATORS_GUIDE.md` | The operator's manual: launchers, approval duties, the guard, cadences |
| `packs/` | The knowledge. `packs/INDEX.md` is the always-loaded surface |
| `kernel/` | Policy, guard and metadata law, schemas, and the templates a seed compiles from |
| `inception/` | Session 0: interview, scale, walk order, compile |
| `examples/` | One task run end to end, lean and high-assurance |
| `org/` | The EOS's own state: task records, claims, decisions, playbooks, logs |
| `registry/` | Projects, capabilities, evidence, vendors, lessons, stack profiles |
| `estate/` | Which repo owns what, and which repos the EOS governs |
| `benchmark/` | The frozen v1-against-v2 protocol, fixtures, drills and results |
| `tools/` | The one executable, `python -m tools.eos` |
| `archive/` | A pointer to the `archive/v1-final` tag, where the whole v1 tree lives |
| `INDEX.md` | Derived index of every file, grep the tag column |

## How a venture consumes the EOS

A venture never reads this repo at random. Session 0 compiles it a seed
pack: a thin router, a lock-book of its rulings, the distilled standards
it needs and, at ORG scale, an org kernel. The seed is stamped with the
EOS commit it came from. The venture pins that commit and never
auto-upgrades; an upgrade is a deliberate run of the upgrade playbook.
`GOVERNANCE.md` sets what a pin must resolve to.

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
  Promotion has numbers and demotion exists (`GOVERNANCE.md`).
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
- **Every venture feeds back.** Rulings and lessons are harvested,
  repeated argued rulings become defaults, and defaults become binding
  only with an ADR.
- **Lean.** Capture the decision structure, not restatements of common
  knowledge. If removing a line would not cause a mistake, cut it.
