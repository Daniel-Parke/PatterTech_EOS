---
summary: What the PatterTech EOS is, how the repo is laid out, how a venture consumes it, and the principles that hold
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
v1 and why, and points at the canonical files as it goes.

## Map

| Path | What lives there |
| --- | --- |
| `AGENTS.md` / `CLAUDE.md` | The router: entry modes and the never-list, byte identical |
| `TOUR.md` | The teaching surface, rewritten by hand each release |
| `GOVERNANCE.md` | The graded change path, precedence, promotion, the protected set |
| `OPERATORS_GUIDE.md` | Daniel's manual for running the EOS |
| `packs/` | The knowledge. `packs/INDEX.md` is the always-loaded surface |
| `kernel/` | Policy, guard and metadata law, schemas, and the templates a seed compiles from |
| `inception/` | Session 0: interview, scale, walk order, compile |
| `org/` | The EOS's own state: task records, claims, decisions, playbooks, logs |
| `registry/` | Projects, capabilities, evidence, vendors, lessons, stack profiles |
| `estate/` | Which repo owns what, and which repos the EOS governs |
| `benchmark/` | The frozen v1-against-v2 protocol, fixtures, drills and results |
| `tools/` | The one executable, `python -m tools.eos` |
| `archive/` | v1 material kept in place and marked archived, never deleted |
| `INDEX.md` | Derived index of every file, grep the tag column |

## How a venture consumes the EOS

A venture never reads this repo at random. Session 0 compiles it a seed
pack: a thin router, a lock-book of its rulings, the distilled standards
it needs and, at ORG scale, an org kernel. The seed is stamped with the
EOS commit it came from. The venture pins that commit and never
auto-upgrades; an upgrade is a deliberate run of the upgrade playbook. A
pin must resolve to a pushed tag or a commit reachable from origin, and
the checker enforces it.

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
