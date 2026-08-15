---
summary: The teaching surface for EOS 0.4.0, the words it uses in a particular way, what changed from v1, the modes, the risk layers, Genesis, the swarm method, staged verification, the study workflow and the pack system
type: guide
tags: [eos]
review: 2027-08
supersedes: archive/v1-final:GUIDE.md
---

# TOUR

The one document that teaches the system. Read it once. After that, work
from the router, `packs/INDEX.md` and the canonical files they point at.

It replaces `GUIDE.md`, which taught v1 and is at
`archive/v1-final:GUIDE.md`.

TOUR is rewritten by hand at every release rather than patched, because
a teaching file edited in place drifts away from the system it describes
and nobody notices until it misleads someone. There is no generator:
this is a discipline, not a build step, and calling it regenerated would
imply a machine keeps it true when a person does.

## Contents

| Section | What it settles |
| --- | --- |
| [What this repository is](#what-this-repository-is) | The four things in the tree, and what each is for |
| [The vocabulary](#the-vocabulary) | The words this repository uses in a particular way |
| [Version numbers](#version-numbers) | What 0.4.0 means, and what 1.0 would take |
| [What changed from v1, and why](#what-changed-from-v1-and-why) | The audit, the benchmark, and what they moved |
| [The five execution modes](#the-five-execution-modes) | How much ceremony one task pays |
| [Two layers of risk control](#two-layers-of-risk-control) | The router, the guard, and what neither one does |
| [The decision budget](#the-decision-budget) | What an agent may decide on its own |
| [What a venture gets at birth](#what-a-venture-gets-at-birth) | Session 0, the seed, Genesis, and letting go |
| [Building wide](#building-wide-graphs-lanes-and-one-integrator) | Lanes, the integrator, and the counter-evidence |
| [How work is verified](#how-work-is-verified) | Staged verification, and the independent oracle |
| [Studying something](#studying-something-and-what-happens-to-what-you-learn) | The lens contract, the ledger, the dispositions |
| [Claims and derived views](#claims-and-derived-views) | Who may write what, and what is generated |
| [Less law, better kept](#less-law-better-kept) | Binding rules against defaults |
| [The pack system](#the-pack-system) | Disclosure, coverage, predicates, drills |
| [Where to look for what](#where-to-look-for-what) | The lookup table |

## What this repository is

A pile of files that carry engineering judgement, so that an agent
building a product does not have to work it all out again. There is no
build here and nothing in this repository runs while a venture runs.

Four things live in it.

| Part | What it holds | Start here |
| --- | --- | --- |
| **Packs** | Argued knowledge, one domain at a time. Atomic Doctrine carries standing rules; Wargames carry the forks that need argument. | `packs/INDEX.md` |
| **The kernel** | How much ceremony a piece of work deserves, what a consequential action may do, and the templates a venture is compiled from. | `kernel/README.md` |
| **Registries** | What is true today, with dates on it: evidence, lessons, stack profiles, coverage and pressure dispositions. | `registry/CAPABILITIES.md` |
| **Governance** | How all of the above changes without rotting, settled across ten decision records. | `GOVERNANCE.md` |

## The vocabulary

Most of these are ordinary words doing a specific job here. They appear
across the packs and the playbooks without a definition anywhere else,
so this is the definition.

| Word | What it means here |
| --- | --- |
| **Operator** | The person who has adopted a repository and holds its human gates: accepting a decision record, signing a seed rubric, approving a release, spending money. In this repository it is the person who owns it. In a venture it is whoever launches sessions there. `OPERATORS_GUIDE.md` is written to that person. |
| **Integrator** | A role, not a job title: the single session that holds the plan while work is fanned across lanes. It commits the claim set before any lane is dispatched, owns the hub files and every derived view, adopts or discards what the lanes hand back, and runs the generators. Nothing else may run `python -m tools.eos task views`. |
| **Lane** | One writing session with a closed brief and a write set no other lane touches. A lane is given its claim; it never takes one. |
| **Hub file** | A file that many lanes would otherwise want to write: an index, a shared type file, a manifest, any generated view. Hub files are integrator-owned and never delegated. |
| **Oracle** | The artefact that decides whether a change is correct. Usually a test or an acceptance condition. Who wrote it matters more than when, and the section on verification says why. |
| **Seed** | The set of files Session 0 compiles into a new venture's repository. `kernel/SCALE_MATRIX.md` is the law of what it contains. |
| **Lock-book** | The venture's pinned contract with the EOS. It names adopted packs and points at `docs/RULINGS.json`; an agent working on a venture reads it before anything here. |
| **Tier** | R0 to R3, the risk ruling on one task. It is ruled once, when the task record is written, and read back from the record after that. |
| **Pack** | One domain's activation, outcomes, limits and decision map, disclosed in three levels. `packs/PACK_SHAPE.md` is the contract every pack keeps. |
| **Doctrine** | One atomic standing proposition with an authority grade. Binding applies whenever its scope holds; default is inherited unless pressure and an argued Ruling justify departure; advisory informs judgement; preference is optional taste or convenience. |
| **Wargame** | One advanced decision procedure for a selection, Doctrine pressure, exception or uncovered gap. `GD-*` and `WG-*` are immutable identities of the same type; only new records use `WG-*`. |
| **Doctrine relation** | A typed, conditional edge such as `depends_on`, `supports` or `tensions_with`, owned beside its Doctrine and shown estate-wide in the generated pressure matrix. |
| **Ruling** | One venture executing one Wargame. Raw Rulings stay with the venture; EOS receives only a privacy-reviewed summary when the venture chooses to share one. |
| **Stack profile** | A dated record of named tools, tested versions and interoperability limits. It is useful evidence, not timeless Doctrine. |
| **Predicate** | A yes-or-no fact about a venture or a task that activates a pack. `kernel/PREDICATES.md` is the controlled list of names. |
| **Claim** | An exclusive right to write a set of paths, committed by the integrator before any lane opens. |
| **Protected set** | The files and subjects that need an accepted decision record and the operator before they change. `GOVERNANCE.md` lists them. |
| **Derived view** | A file generated from a canonical record. Never hand-edited: fix the source and regenerate. |

**Where the integrator sits.** Here the operator holds the role, so
The operator is both. In a venture at ORG scale it is whoever runs the wide
build. At S scale there is nothing for the role to hold: no claims file
and no derived views, and an S venture that needs a second writer
rescales first.

## Version numbers

Nothing has been released from this line. The tooling reads 0.4.0.

ADR-0009 renumbered what came before. This document still uses the build
names v1, v2 and v2.1, because that is what the decision records and the
changelog call them, and renaming a history after the fact stops it
being one.

| Build name | Version | Where it stands |
| --- | --- | --- |
| v1 | the `v1.0.0` tag | Released 2026-07-07. That architecture has since been replaced and is archived at `archive/v1-final`. |
| v2 | 0.2.0 | Merged, never released. |
| v2.1 | 0.3.0 | Folded into the same unreleased line (ADR-0007). |
| this tree | 0.4.0 | Unreleased. |

1.0 means walk-away ready, and ADR-0009 makes that a gate of eight
items somebody can run or read rather than a feeling. Two of them need
something outside this repository: Genesis running end to end on a real
venture, and a cold agent completing a first task from a compiled seed
across the seed corpus. Until every item passes, the number stays below
1.0.

## What changed from v1, and why

### What v1 cost

v1 imported the Venture A machinery unchanged: PLAN, WORK and VERIFY
separated on every task, a session log and a Resume Packet at every
close, one item in flight, test-first everywhere, a wargame before any
doctrine change, and a checker that validated metadata but no meaning.

The 2026-08 audit measured what that cost across all twenty v1 sessions.

| What was measured | What it came to |
| --- | --- |
| Share of every line ever written that was ceremony | 20.1 per cent |
| Mandated boot reading before any work started | 475 to 900 lines |
| Sessions that were one hundred per cent paperwork | Three of twenty |
| Commits after the `v1.0.0` tag leaving no record but the commit message | Four of six |

Worst of all, the discipline collapsed the moment work left session
ceremony. One of those four undocumented commits was a doctrine edit
with no wargame behind it. The other two commits did file their session
logs. A repository can be checker-green and still hold false statements
about itself, and this one did.

### What the benchmark measured

The benchmark measured the same thing from the other end. Under v2,
ceremony fell on every task it scored.

| Task | v1 ceremony lines | v2 |
| --- | --- | --- |
| Feature | 136 | 43 |
| UI fix | 142 | 19 |
| Injection probe | 119 | 0 |
| Doc fix | 17 | 0 |

Delivery went the same way, and that is the number that matters most:
**fifty-three v1 runs produced fully passing work thirty-nine times, and
fifty v2 runs produced it fifty times.**

`org/reports/V2_FINAL_REPORT.md` holds the method and the per-task
split, including the two efficiency gates v2 did not reach, which
ADR-0007 has since struck rather than met. README says why, and says
plainly that no run has been made against the tree you are reading.

### What v2 and v2.1 did with it

So v2 keeps the parts that earned their place and makes the rest
proportional. It also filled the knowledge gaps: v1 had one deep web
aesthetic and four thin modules, with nothing on product, coding, data,
agents, security or delivery.

v2.1 adds back the one step v2 dropped (Genesis), gives the system a way
to learn from things that are not documents (the study workflow), writes
down how we actually build (the swarm pack), stages verification by risk
instead of by ordering, and takes a pass at the rules to leave fewer of
them, better kept.

## The five execution modes

Ceremony attaches to the task, not to the calendar. Every task is given
a risk tier, R0 to R3. R0 is reversible local work; R3 is work a person
has to approve because it cannot be undone.

The tier picks the mode, and `org/PLAYBOOKS.md` holds the procedure for
each.

| Mode | Tier | What it asks for |
| --- | --- | --- |
| **Express** | R0 | Reversible local work in one run. The commit message is the whole record. Targeted checks, self-merge, no files. |
| **Standard** | R1, the default | One owner plans, implements and tests. Independent review when the router asks for it, otherwise a sampled review pool. |
| **Exploration** | not picked by tier | A sandboxed spike on a `spike/` branch that never merges. Timeboxed. It exits discarded or hardened. |
| **High-assurance** | R2 and R3 | Explicit invariants, a rollback plan, an acceptance oracle written independently before implementation and frozen, independent review, and a person for anything irreversible. |
| **Parallel** | a wrapper | Not a mode of its own. Each lane carries its own mode and its own claim. |

Under Standard, a task record is written where the work is gate-bearing,
which means R2 and above, any diff touching the protected set, and
anything a reviewer must later be able to find.

PLAN, WORK and VERIFY are retired. The one separation kept is who writes
the thing that decides whether the work is correct, because that is the
one with controlled evidence behind it.

## Two layers of risk control

Two layers, and they are independent. The router rules how much ceremony
a task pays before the work starts. The guard judges each consequential
action at the moment it would run.

ADR-0008, the de-restriction pass, goes nowhere near either one.

### Layer one: the router

It rules the minimum tier from the union of two input sets: the side
effects the owner declares on the task record, and mechanical signals
derived from the git diff. Thirteen factors, each with a floor.

A floor is a minimum and never a ceiling, so several active factors
resolve to the highest. Every ruling carries machine-readable reasons,
one per active factor.

The law is `kernel/POLICY_SPEC.md`, and the table that actually rules is
`FACTOR_TABLE` in `tools/eos/router.py`.

### Four things the router does not do

No file here may imply otherwise.

| It does not | And so |
| --- | --- |
| Read a venture's policy `risk.factors` block | That block is validated at seed time and never consulted, so adding a row there moves no ruling. What a venture really tunes is the express thresholds and the path-pattern lists. |
| Detect three of the source names in its own table | Nothing in a diff says a change cannot be undone or that a call goes out, so `no-rollback`, `egress` and `infra-state` have no detector behind them. The code lists those three as reserved rather than pretending. |
| Read prose | Text inside a data file is data, and instructions found in data activate no factor. |
| Run in CI | `python -m tools.eos route` is a command a person or a playbook runs. What CI runs is the checker and the tests. |

### When the ruling is paid

The ruling is paid once, at record creation, and stored on the record. A
session reads it off the record rather than routing again. The merge
gate recomputes against the actual diff and can only raise it.

One automatic control sits in the whole repository: `route` exits 3 when
the diff touches a protected path and no `--adr` was given. It checks
only that a value was passed. Nothing reads the id or confirms the
decision record is accepted, so the operator carries that.

The router did move in v2.1, in one narrow way worth knowing. Two side
effects an owner could already declare, `rollback-cost` and
`writes-production-data`, reached no factor and so changed nothing when
declared. ADR-0006 wired both. A question the record asks and then
ignores is worse than not asking it.

### Layer two: the action-time guard

Every consequential action is judged immediately before it runs,
whatever the tier, into one of four verdicts: allow, require-approval,
manual-only, or deny. The law is `kernel/GUARD_SPEC.md`.

The guard **fails closed**. Without a validated host enforcement
adapter, every guarded class is manual-only.

| Floor | The actions that carry it |
| --- | --- |
| **manual-only** | Money movement, production-data deletion, publishing to a new external destination, accepting legal terms |
| **deny** | Secret emission outside the sanctioned store, force-pushing or deleting main |

Nothing lowers those. A policy can tighten from there through
`approvals.always_human`; it can withdraw a validation and can never
grant one, because the guard reads the mapping on disk rather than
believing the policy.

### What the guard grants today

Nothing autonomous.

One host adapter ships, `kernel/adapters/claude-code.json`. It was
validated on 2026-08-03 at mapping level, offline, with `host_run`
false, which means the run proved that the mapping classifies each case
correctly and not that a live session's hooks fired.

| Of the ten guarded classes | Where they stand |
| --- | --- |
| Three: external-write, destructive-git, dependency-install | Covered by a passing case. All three rule require-approval, so even those resolve only on a recorded decision from the operator. |
| The other seven | No passing case, so they stay manual-only. |

No class rules allow, and none may be raised to allow on a mapping-level
run alone.

## The decision budget

"Never invent" is replaced by three bands.

| Band | What falls in it | What it costs |
| --- | --- | --- |
| **Free** | Naming, decomposition, test structure, patterns already in the tree, file placement | Decide it, record it in the commit message |
| **Durable** | A new dependency, a schema element, a public contract, a precedent | Decide it, write a short ADR before merge |
| **Escalation** | Money, legal, personal-data ambiguity, the protected set, weakening a check, conflict with stated intent | Never alone |

Express lives in the free band only. A durable decision converts the run
to Standard.

## What a venture gets at birth

Two phases, in order, both run in the venture's own repository. Session
0 compiles the seed. Genesis turns the seed into a build plan.

### Session 0

`inception/INCEPTION.md` is one sitting with the operator in the room at
the start, the middle and the end. It interviews them in eighteen
questions, thirteen about the venture and five about risk.

Then three challenge steps that are not optional:

1. The agent restates the venture until the operator says it is right.
2. It names the three cheapest ways the venture dies.
3. It proposes a strictly smaller version than the one asked for.

All three land in the brief in the operator's words.

Then the always-walk decisions: scale by WG-EOS-001, repository shape by
WG-EOS-002, the risk surface, and the live security Wargames. The risk
surface turns the prose answers into the directory patterns the venture's
policy file uses.

The agent activates packs from the declared facts. Applicable Doctrine
summaries load automatically. Full atoms load only when needed, and a
Wargame runs only when pressure, conflict, a gap or the operator engages
it. Matching is tri-state: true requires it, false records why it stayed
out, and an unknown high-consequence fact is asked or included. An unknown
routine fact remains a visible candidate.

Every candidate is recorded as selected, omitted or still a candidate,
with a reason. Executed Wargames receive a structured Ruling in
`docs/RULINGS.json`; inherited defaults stay implicit through the pin and
adopted packs. The matcher selects procedures, never their outcome.

The agent then compiles the seed by slot-filling templates at the pinned
EOS commit. A slot with no truthful answer stops the compile and goes back
to the operator. Nothing is composed and nothing is invented.

### The seed gate

The gate at the end is headed by the cold-start test: a fresh session,
given only the seed and the first open task, finishes it with no
questions. If that fails, the fix is better files, not a warmer prompt.

There is a fast path, `inception/EXPRESS_INCEPTION.md`, for an S venture
that answers no to all five gate questions. It does not run the pack
walk at all, and it says so.

### What the venture walks away with

`kernel/SCALE_MATRIX.md` sets it and owns the current file counts. They are
not copied here. CLAUDE.md is a byte copy of AGENTS.md, the compile report
is meta, and the Genesis forms stay blank until the venture chooses to run
the phase. A blank form is a correct result rather than an unfinished one.

### Genesis

`inception/GENESIS.md` is the step v1 had, v2 dropped and ADR-0006
restored. From now on the word means this phase and only this phase;
where the v1 sense is cited, the citation is glossed.

It runs once, straight after the seed gate, under the venture's own
rules, because Session 0's write-to-main exemption ended at sign-off.

It is a launch decision rather than a gate. A venture may build with no
blueprint, and the cost is that the first lanes settle the architecture
one file at a time, in private.

It runs in six steps. Four of them fill a form the seed already carries
blank; step three settles what the packages are cut from, and step six
is the gate.

1. **Research packets**, at most one per material workstream, and only
   where a decision is actually waiting on one. Sourced facts and
   decisions, not a survey: a stated stopping condition, a line cap, and
   a rule that research changing no decision says so in one line and
   stops.
2. **A product map** (`docs/PRODUCT_MAP.md`), integrated by one session
   however wide the packets ran: the domain model, the components and
   what runs where, the contract between each pair that talks, the
   dependency graph, the acceptance conditions per user journey, the
   risks, and the open decisions with a name and a date on each. Every
   section is marked draft, settled or stale.
3. **The cross-cutting decisions settled on the map**, before any lane
   diverges. A package may only be cut from a settled section.
4. **Work packages** (`docs/packages/WP-NN.md`), one per lane, each
   naming its objective, the interfaces it consumes and provides, the
   files it owns, the exact context it needs, and acceptance conditions
   copied from the map rather than written from code that does not
   exist yet.
5. **An acceptance spine**, the journey walk-through written as a real
   suite that fails on the day it is written, authored by a session
   that will not implement against it and finished before any build
   lane opens. That is the independent oracle every build lane
   inherits.
6. **The operator reads the map and the packages and says go.** That is
   the one human gate in the phase. If they will not say go, whatever
   stopped them goes on the map as an open decision with their name
   against it.

### Genesis at S scale

Genesis is scale-graded, and the grading is in the forms themselves,
pruned when the seed compiled, so an S venture holds the S variant and
never has to work out what to leave out.

What S drops is volume: at most one packet, a map of about a page, one
package per workstream, and a spine that is still a suite but is not
mutation-checked before it blocks.

All five forms ship blank in every seed at both scales, so a venture
that declined Genesis at the gate can run it later without a recompile.

### Then the EOS lets go

It compiled a seed and a blueprint; it runs nothing inside the venture,
owes it no report, and never initiates a check on one. A check-in
happens only when the venture asks, and it returns findings and
candidate lessons and applies nothing.

## Building wide: graphs, lanes and one integrator

`packs/agentic-swarm/PACK.md` describes how we build substantial work:
fan out over a measured
dependency graph, with one integrator and a verifier that predates the
lanes. Anything else is either a single agent or an expensive mistake.

### What that means in practice

- Cut the partition from the dependency graph, not from a feature list.
  Lanes own whole directories or named files that no other lane touches,
  so the partition is disjoint by construction rather than by good
  behaviour.
- Hub files and every derived view belong to the integrator and are
  never delegated.
- A lane's brief is closed and literal: objective, exact write set, read
  set, return contract, tools, budget, stop condition, acceptance
  condition, nothing assumed inherited. It names an escape for anything
  the brief does not determine, and using that escape is a good outcome.
- What a lane returns is data, not instruction, and the integrator
  treats it that way.
- Three to five lanes is the default. Go wider only with a strong
  mechanical oracle and a recorded reason.
- Agreement between lanes is not a verdict. Independently generated
  implementations co-failed 429 times where independence predicts 115,
  and the failures concentrate on the ambiguous clauses of the
  specification. Voting across three implementations does reduce
  failures and still never decides a merge. When lanes agree on
  something wrong, suspect the specification clause first.

### The pack argues against itself

The pack carries its own counter-evidence at length, in the body rather
than a footnote, because a pack arguing for a method its owner already
believes in is exactly the condition under which a pack lies.

The strongest result in its corpus points away from swarms. On a
normalised substrate holding benchmark loading, tool access and
accounting constant across ten benchmarks:

| System | Score | Cost |
| --- | --- | --- |
| Single-agent baseline | 74.12 per cent | the baseline |
| Best of six multi-agent systems | 75.56 per cent, inside the uncertainty band | 24 per cent more tokens |
| The other five | 62.83 to 71.56 per cent | one of them at 286 per cent more tokens |

Five of six were below baseline while costing more. Coordination cost
also grows faster than the work does, and no public benchmark measures
the shape we actually use, so our own runs are the best evidence we
have.

The pack says that plainly rather than claiming swarms are faster, and
it names the places our own rules are thinly evidenced.

`kernel/templates/org/GRAPH_BUILD.tpl.md` compiles the usable half of
this into every ORG seed, so a venture gets the method too. It is ORG
only, because it names `org/claims.json` as its mutex and an S venture
has no claims file.

## How work is verified

Verification is staged by risk and by measured stability, never by a
percentage of completeness. There is no coverage gate.

| Stage | What it asks for |
| --- | --- |
| **From day one** | The risk floors, which never move; cheap executable checks (build, types, lint, schema, smoke) wired before the first feature lane opens; and the failing acceptance spine from Genesis. |
| **Per change** | Reproduce a bug before fixing it, write the oracle before gate-bearing work, pin behaviour before refactoring. Changes touching personal data or anything irreversible take the strict path. |
| **At interface stability** | When a package declares its contract stable, contract tests on that boundary start blocking its neighbours. |
| **At stabilisation** | Only when the stability signals fire is the broad harness assembled. It is derived from the map and the specifications rather than from the code, authored or reviewed independently of the implementing agent, and mutation-checked before it is allowed to block anything. |
| **Deletion** | Tests that only protect retired structure go in the same change that retires the structure. |

Executable is the operative word in the first row. A cheap tier that is
a list in a document rather than a command that exits non-zero buys
nothing.

`packs/delivery-testing/PACK.md` states the stability signals, and
states that they are starting values a venture overrides in its
lock-book rather than measured thresholds. It also states that this
whole staging is a default and never measured. No controlled comparison
of building the broad harness early against building it on stability
signals was found.

### Test-first is default Doctrine, not binding Doctrine

The rule that required the oracle to be committed before the
implementation was accepted is now a default-grade Doctrine: inherit it
unless pressure and an argued Ruling justify departure.

Two measurements moved it, and neither of them tests ordering head to
head.

- Prompting a frontier model for more tests across the five hundred
  tasks of SWE-bench Verified changed test-writing behaviour on most
  tasks and left the number of tasks resolved statistically unchanged.
- Prompting a model with the buggy implementation in front of it cut
  bug-revealing tests by about two thirds against giving it the correct
  implementation, and by about 44 per cent against giving it the
  specification.

`packs/coding/PACK.md` carries both rows by evidence id.

Read those two together and the binding rule is narrower and better
evidenced than the one it replaces: **the artefact that decides whether
a change is correct must not be written by the agent holding that
implementation in context.**

Ordering is ceremony. Independence is not. Acceptance conditions
authored at Genesis satisfy this by construction, which is why a lane
never has to stop for it.

### What the demotion cost

Two things, and the pack buys both back by name rather than losing them
quietly.

| What the old rule bought | What replaces it |
| --- | --- |
| Red then green, a free proof that a check could fail | A seeded fault, or a diff-scoped mutation run |
| The red-green cycle enforcing small even steps, which is what carried the measured benefit in the human literature | A stated cap on package size |

A stated cap is something somebody has to police.

## Studying something, and what happens to what you learn

Before v2.1 the EOS could only learn from published documents. It can
now be pointed at a product, a repository, a game, a design system or a
postmortem.

The procedure is PB-E11 in `org/PLAYBOOKS.md`. It only ever starts
because the operator points at something. It is never scheduled.

### The five steps

1. **A lens contract first.** One page: what the source is and its exact
   version, how it was lawfully obtained, its licence and the
   jurisdiction that matters, the aspects being studied, the aspects
   deliberately excluded, how far the study may escalate (observe, docs,
   tests, source), and where the findings land. The operator approves it in
   the room. `python -m tools.eos study --out DIR` scaffolds it and
   fetches nothing. Never carried away: verbatim code, assets,
   expressive text, or anything that would make the result look like the
   source.
2. **One session reads the raw source, and only that session.** If the
   source is fetched live, the copy is frozen first and the frozen copy
   is what gets read.
3. **Findings keep their kinds apart**: direct observation, sourced
   fact, interpretation, inference, recommendation. Each is marked as
   something the source does well, does badly, or merely does
   differently, or as unknown, with the conditions that made it work.
4. **Conflicts are found before the operator sees anything.** The findings are
   mapped against the packs, the registries, the policies, governance
   and prior lessons, and anything that contradicts a live rule names
   that rule.
5. **Then a bounded interview**, and his decisions become rows in
   `registry/lessons.json`. `registry/LESSONS.md` is the derived view of
   that file and is never hand-edited. The same ledger takes the monthly
   harvest of a venture's feedback file, so both intakes land in one
   place.

A lesson row carries where it came from, the lesson itself, its evidence
class, its disposition, its scope, when it applies, what it informs,
what it contradicts and what it replaces, the decision date and the operator's
reasoning in a line.

### The eleven dispositions

The disposition is the useful part of a row: it names the kind of home
the decision found, and therefore which file owns it now.

`kernel/schemas/lesson.schema.json` owns the list and refuses a value
that is not on it. This section owns what each one means, because until
now nothing in the tree did, and eleven values printed with no
definition anywhere are eleven words doing no work.

| Disposition | What it means |
| --- | --- |
| `reference-only` | Worth knowing, owned by nothing. It changes no file and binds nobody. Recorded so the reading is not done twice. |
| `dated-registry-fact` | A fact with a date on it. It lands in a registry, usually a stack profile, and carries a review trigger. |
| `venture-ruling` | True for one venture, recorded in that venture's lock-book. It does not amend an estate default by existing. |
| `worked-exemplar` | The lesson travels better as a worked example than as a rule, so it becomes an exemplar file in a pack. |
| `implementation-reference` | The lesson is about how something here is built, so the code, schema or template changes and the row is the provenance. |
| `experimental-guidance` | Adopted as a reversible default carrying its hypothesis and an expiry no more than ninety days out. The experiment sweep closes or promotes it. |
| `decision-guide` | Historical ledger name for a recurring fork. Its admitted destination is now a Wargame with the options and decision rule argued; the value stays for schema compatibility. |
| `estate-default` | Adopted across the estate as a default: do it unless you record why not. |
| `binding-candidate` | Proposed for binding and not binding yet. This ledger can propose and nothing more. |
| `rejected` | Argued and declined. The row stays with its reason, so the same proposal cannot return as though it had never been argued. |
| `deferred` | Not decided yet. The row must name the condition that reopens it, and the schema rejects a bare date, because a date tells the next reader nothing about what they are waiting for. |

Nothing here can make a rule binding. The workflow can propose it; the
promotion ladder in `GOVERNANCE.md` is unchanged and binding still needs
an accepted ADR and the operator.

## Claims and derived views

### Claims

Claims stop two sessions writing the same file. When more than one
session may write at once, the integrator assigns claims and commits
them before any lane is dispatched, and lanes never acquire or mutate
one.

Once a claim set is committed it is exclusive: `task new` and
`task update` refuse a session the set does not name, and that session's
work is quarantined for the integrator to adopt or discard.

Liveness comes from harness state or a recorded process id, and a
timestamp alone never authorises taking someone's claim.

A single session working alone does not hand-write a claim file first.
It is implicitly claimed, because there is nobody to collide with, and
git history plus the checker is what catches it going wrong (ADR-0008).
`OPERATORS_GUIDE.md` carries the one sharp edge in that arrangement.

### Records are canonical, views are generated

Nobody hand-edits a view. Both generators are the integrator's alone.

| Canonical record | Its view | Regenerated by |
| --- | --- | --- |
| Task records under `org/tasks/` | `org/TASKS.md`, `org/STATE.md` | `python -m tools.eos task views` |
| Front-matter across the tree | `INDEX.md`, `packs/INDEX.md` | `python -m tools.eos check --write-index` |
| Atomic Doctrine and Wargame metadata | `packs/DOCTRINE_INDEX.md`, `packs/WARGAME_INDEX.md`; `packs/GUIDE_INDEX.md` is a compatibility pointer | `python -m tools.eos check --write-index` |
| Doctrine relations and `registry/pressure-dispositions.json` | `registry/DOCTRINE_PRESSURE_MATRIX.md` | `python -m tools.eos check --write-index` |
| `registry/identifier-aliases.json` | `registry/ID_ALIASES.md` | `python -m tools.eos check --write-index` |
| `registry/coverage.json` | `registry/CAPABILITIES.md` | `python -m tools.eos check --write-index` |
| `registry/lessons.json` | `registry/LESSONS.md` | `python -m tools.eos check --write-index` |

`registry/evidence.json` and `estate/repos.json` are canonical too, and
no generator writes a view of either.

## Less law, better kept

Doctrine is the public umbrella for standing propositions. Each atom has
one authority grade, because calling everything a rule hides the difference
between a safety floor and taste.

| Authority | What it means |
| --- | --- |
| **Binding** | Holds whenever its applicability is true. A Wargame cannot waive it; contrary evidence opens Doctrine review or an ADR. |
| **Default** | Inherited unless pressure and an argued Ruling justify departure. |
| **Advisory** | Informs judgement without requiring a departure record. |
| **Preference** | Optional taste or convenience, including brand-scoped house style. |

ADR-0008 first asked which old rules genuinely prevented a serious or
hard-to-undo failure. ADR-0012 and ADR-0014 then made the result atomic and
machine-readable. A Doctrine keeps its ID when evidence or authority changes
without changing the proposition. A material prescription or scope change
creates a new ID and names what it supersedes.

### What loosened

| Rule | Where it stands now |
| --- | --- |
| Claims | Needed when work runs in parallel, not when a lone session writes |
| Opening a task record | A lane may open its own |
| Task records | For gate-bearing work; ordinary work records itself in the commit message |
| Cadences | Four monthly ones became one pass with four sections, and the two quarterly ones became on-demand |
| Line budgets | Most warn instead of failing |
| The tag list | The known set rather than the permitted set |
| Metadata minima | Shrank to the axes that actually change what an agent does |

### What did not change

The safety floors, the rule that a derived file is never hand-edited,
append-only decision records, supersession stated in both directions,
the promotion ladder, and the decision budget. The ADR says why.

The honest counter-argument is recorded too, because loose governance is
how sixty-six false statements got into this tree in the first place. So
every loosened rule names what catches the failure instead.

### Wargaming only where pressure exists

A Wargame is one semantic type even though its immutable identity may begin
`GD-*` or `WG-*`. The historical `guides/` directory is a storage name, not
a second kind. New identities use `WG-*`.

Every Wargame states the stakes, Doctrine or gap under pressure,
preconditions, materially different options, a premortem for each credible
option, the decision rule, safe default, cheapest discriminating test,
fallback, exit and revisit conditions, counter-evidence and transfer limits.
Worked outcomes do not grow inside that file. One venture execution is a
`RUL-*` record in the venture's `docs/RULINGS.json`.

Doctrine edges live as typed `DREL-*` records beside the Doctrine that owns
the decision. The generated `registry/DOCTRINE_PRESSURE_MATRIX.md` shows the
estate-wide graph and the accepted pressure backlog without becoming a
second registry.

## The pack system

### Three levels of disclosure

Knowledge is packs, and a pack discloses itself in three levels.

1. A first paragraph always in context through `packs/INDEX.md`.
2. A `PACK.md` body on activation.
3. Full Doctrine atoms, Wargames, refs, exemplars and recipes on demand
   from the body, which names what each one holds so you never have to
   list a directory.

The contract is `packs/PACK_SHAPE.md`, including the eleven-point
definition of done and the pruning test that asks of every line whether
removing it would cause an agent to make a mistake.

### Coverage: what is built, and what is not

A domain that cannot meet that bar stays a row in
`registry/coverage.json` and is never described as implemented. The
generated `registry/CAPABILITIES.md` is the current answer: built packs and
registry-only domains appear in the same view, each with its admission reason
or reopening trigger. A backlog row is not coverage.

### Which packs a venture loads

Activation runs on predicates: yes-or-no facts a pack declares in its own
`applies_when` front-matter. `kernel/PREDICATES.md` is the controlled
vocabulary those names must come from (ADR-0010).

It is grouped by subject rather than by pack, which is the whole
mechanism: two names for one fact land next to each other, where
somebody adding a third will see them. Sharing a predicate across packs
is normal, and two packs naming one fact is two packs agreeing about the
world.

Venture facts come from the Session 0 interview. Task facts come from the
task record or diff. Always-true facts hold of every governed venture by
construction. `kernel/PREDICATES.md` owns the current vocabulary and count;
this teaching file does not copy either.

`python -m tools.eos activate` computes pack activation from declared facts
and names what stayed out. `doctrine match` and `wargame match` share the
knowledge matcher: they return applicable Doctrine, required and candidate
Wargames, unresolved facts, uncovered pressures and selection reasons. A
misspelled predicate is refused rather than quietly acting false.

### Drills, and what they have not proved

Every pack carries reviewable criteria in its `CHECKS.md`. Most also
have a frozen acceptance drill under `benchmark/drills/`: twenty-seven
specs, of which twenty-two can be run today.

| Wave | Count | Frozen before its pack | What that is worth |
| --- | --- | --- | --- |
| A | 8 | yes | independent oracles |
| B | 12 | no | the spec could have been written to suit the pack |
| C | 2 | no | added at the pre-release review, same guarantee as B |
| D | 4 | yes | frozen while the capability was a registry-only row, so there was no pack to write them to at all |
| E | 1 | no | `agentic-swarm`, which shipped with its drill proposed and never frozen |

The five in waves D and E were frozen on 2026-08-15 and have no scenario
tree and no graders, so they cannot be run. A frozen spec with no
scenario is not a drill that failed, and their ledger rows say so.

**Not one has produced a pack verdict.** On 2026-08-15 the twenty-two
runnable drills ran against their untouched fixtures and every one
failed, which is the criteria proving they discriminate and not a
judgement on any pack. Those rows carry `graded: scenario-baseline` to
say so.

The twenty-two rows written before any scenario or grader existed are
still null and stand as history, because the ledger is append-only.

So nothing in this repository has been graded by a cold agent. ADR-0007
defers that spend and says so.

### Where START.md went

`START.md` is retired and archived at `archive/v1-final:START.md`. Its
job, telling you what to read for your entry mode, is done by two things
now: the mode you are routed into, and the activation rows in
`packs/INDEX.md`.

You no longer read a fixed list before starting. The work decides what
loads.

## Where to look for what

| Question | File |
| --- | --- |
| What am I allowed to do here? | `AGENTS.md`, then `GOVERNANCE.md` |
| What do I launch, and what do I approve? | `OPERATORS_GUIDE.md` |
| How do I start a venture? | `inception/INCEPTION.md` |
| How does a venture get a build plan? | `inception/GENESIS.md` |
| How do I run a wide build? | `packs/agentic-swarm/PACK.md` |
| What does one task look like end to end? | `examples/v2-worked-lean.md`, `examples/v2-worked-high-assurance.md` |
| Which knowledge applies to this task? | `packs/INDEX.md` |
| Which standing Doctrine exists, and at what authority? | `packs/DOCTRINE_INDEX.md` |
| Which Wargame covers this pressure? | `packs/WARGAME_INDEX.md`, then `registry/DOCTRINE_PRESSURE_MATRIX.md` |
| Where does this old or pinned identity resolve? | `python -m tools.eos id resolve ID --commit REF` |
| Which facts pull in which pack? | `kernel/PREDICATES.md` |
| What does the EOS know, and what does it not? | `registry/CAPABILITIES.md` |
| How is risk decided? | `kernel/POLICY_SPEC.md`, `kernel/GUARD_SPEC.md` |
| What goes into a seed? | `kernel/SCALE_MATRIX.md`, then `kernel/SEED_RUBRIC.md` |
| What metadata does this file need? | `kernel/METADATA_SPEC.md` |
| What can the one command do? | `tools/CLI_CONTRACTS.md` |
| What is in flight, and who holds what? | `org/TASKS.md`, `org/STATE.md` |
| What have we studied, and what did we decide? | `registry/LESSONS.md` |
| Why is it like this? | `org/decisions/`, newest first |
| Which repos exist and which are governed? | `estate/ESTATE_MAP.md` |
| Where did that claim come from? | `registry/evidence.json` |
| What did v1 say? | the `archive/v1-final` tag, `archive/README.md` says how |
