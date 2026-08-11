---
summary: The teaching surface for EOS v2.1, what changed from v1 and why, the modes, the risk layers, Genesis, study, graph builds, staged verification and where to look
type: guide
tags: [eos]
review: 2027-08
supersedes: archive/v1-final:GUIDE.md
---

# TOUR

The one document that teaches the system. It replaces `GUIDE.md`, which
taught v1 and is at `archive/v1-final:GUIDE.md`. TOUR is rewritten by
hand at every release rather than patched, because a teaching file
edited in place drifts away from the system it describes and nobody
notices until it misleads someone. There is no generator: this is a
discipline, not a build step, and calling it regenerated would imply a
machine keeps it true when a person does.

Read this once. After that, work from the router, `packs/INDEX.md` and
the canonical files it points at.

## What this repository is

A pile of files that carry engineering judgement, so that an agent
building a product does not have to work it all out again. There is no
build here and nothing in this repository runs while a venture runs.
Four things live in it:

- **Packs**: argued knowledge, one per domain, with sources.
- **The kernel**: how much ceremony a piece of work deserves, what a
  consequential action may do, and the templates a venture is compiled
  from.
- **Registries**: what is true today, with dates on it.
- **Governance**: how all of the above changes without rotting.

## What changed from v1, and why

v1 imported the AutoWatt machinery unchanged: PLAN, WORK and VERIFY
separated on every task, a session log and a Resume Packet at every
close, one item in flight, test-first everywhere, a wargame before any
doctrine change, and a checker that validated metadata but no meaning.

The 2026-08 audit measured what that cost across all twenty v1
sessions. **20.1 per cent of every line ever written was ceremony.**
Mandated boot reading ran **475 to 900 lines** before any work started.
**Three of the twenty sessions were one hundred per cent paperwork.**
Worst of all, the discipline collapsed the moment work left session
ceremony: of the six commits after the v1.0.0 tag, **four left no
record but the commit message**, and one of those four was a doctrine
edit with no wargame behind it. The other two did commit their session
logs. A repository can be checker-green and still hold false statements
about itself, and this one did.

The benchmark measured the same thing from the other end. Under v2,
ceremony fell on every task it scored: 136 lines to 43 on the feature,
142 to 19 on the UI fix, 119 to 0 on the injection probe, 17 to 0 on
the doc fix. Delivery went the same way, and that is the number that
matters most: **fifty-three v1 runs produced fully passing work
thirty-nine times, and fifty v2 runs produced it fifty times.**
`org/reports/V2_FINAL_REPORT.md` holds the method and the per-task
split, including the two efficiency gates v2 did not reach, which
ADR-0007 has since struck rather than met. README says why.

So v2 keeps the parts that earned their place and makes the rest
proportional. It also filled the knowledge gaps: v1 had one deep web
aesthetic and four thin modules, with nothing on product, coding, data,
agents, security or delivery.

v2.1, this release, adds back the one step v2 dropped (Genesis), gives
the system a way to learn from things that are not documents (the study
workflow), writes down how we actually build (the swarm pack), stages
verification by risk instead of by ordering, and takes a pass at the
rules to leave fewer of them, better kept.

## The five execution modes

Ceremony attaches to the task, not to the calendar. Every task is given
a risk tier, R0 to R3. R0 is reversible local work; R3 is work a person
has to approve because it cannot be undone. The tier picks the mode.

- **Express** (tier R0): reversible local work in one run. The commit
  message is the whole record. Targeted checks, self-merge, no files.
- **Standard** (R1, the default): one owner plans, implements and
  tests, with a task record under `org/tasks/`. Independent review when
  the router asks for it, otherwise a sampled review pool.
- **Exploration**: a sandboxed spike on a `spike/` branch that never
  merges. Timeboxed. It exits discarded or hardened.
- **High-assurance** (R2 and R3): explicit invariants, a rollback plan,
  an acceptance oracle written independently before implementation and
  frozen, independent review, and a person for anything irreversible.
- **Parallel**: a wrapper, not a mode of its own. Each lane carries its
  own mode and its own claim.

PLAN, WORK and VERIFY are retired. The one separation kept is who
writes the thing that decides whether the work is correct, because that
is the one with controlled evidence behind it.

## Two layers of risk control

**Layer one, the router.** It reads declared facts (does this send
externally, touch money, migrate a schema, handle personal data) and
derived signals (touched paths, DDL detection, dependency deltas, diff
size), and rules the minimum tier with machine-readable reasons. No rule
maps a path alone to a tier. Downward adjustments need a recorded,
expiring exception citing evidence. The law is `kernel/POLICY_SPEC.md`.

**Layer two, the action-time guard.** Every consequential action is
judged immediately before it runs, whatever the tier: allow,
require-approval, manual-only, or deny. Money movement, production data
deletion, secret emission, force-pushing main, publishing to a new
destination and accepting legal terms have floors nothing can lower.
The guard **fails closed**: without a validated host enforcement
adapter, every guarded class is manual-only. The law is
`kernel/GUARD_SPEC.md`.

Neither layer moved in v2.1. The de-restriction pass in ADR-0008 goes
nowhere near them.

## The decision budget

"Never invent" is replaced by three bands. **Free**: naming,
decomposition, test structure, patterns already in the tree, file
placement. Decide it, record it in the commit message. **Durable**: a
new dependency, a schema element, a public contract, a precedent. Decide
it, write a short ADR before merge. **Escalation**: money, legal,
personal-data ambiguity, the protected set (the handful of files and
subjects that need an accepted decision record and Daniel before they
change), weakening a check, conflict with stated intent. Never alone.

Express lives in the free band only. A durable decision converts the run
to Standard.

## Genesis: what a venture gets at birth

Session 0 (`inception/INCEPTION.md`) interviews the operator, rules the
scale, and compiles a seed: a thin router, a lock-book for the
venture's own rulings, the standards it needs and, at ORG scale, an org
kernel. The seed is stamped with the EOS commit it came from.

Under v1 there was a second step after that, and v2 lost it. A venture
went from a signed seed straight into ad-hoc tasks, with the whole
product still un-designed. **Genesis** is that step, restored and
redefined by ADR-0006. From now on the word means this and only this;
where the v1 sense is cited, the citation is glossed.

Genesis runs in the venture's own repository, after the seed gate, and
produces the build blueprint:

1. **Research packets**, one per material workstream. Each is bounded:
   sourced facts and decisions only, a stated stopping condition, a line
   cap, and a rule that research which changes no decision says so in
   one line and stops.
2. **A product map** (`docs/PRODUCT_MAP.md`): the domain model, the
   components and what runs where, the contracts between them, the
   dependency graph, acceptance conditions per user journey, the risks,
   and the open decisions with owners. Every section carries a lifecycle
   state: draft, settled or stale.
3. **Work packages** (`docs/packages/WP-NN.md`): one per lane, each
   naming its objective, the interfaces it consumes and provides, the
   files it owns, the exact context it needs, its acceptance conditions
   written from the map rather than from code, and what done means.
4. **An acceptance spine**: the journey walk-through written as a real
   but failing test suite. It goes green journey by journey, and because
   it is written before any implementation exists, it is the independent
   oracle the build lanes inherit.

Genesis is scale-graded. Its templates compile into every seed; whether
to run it, and in the full or the lite form, is the operator's decision
at launch. ORG runs the full form by default, S the lite form. It ends
with one human gate, the same one the operator already holds: read the
map and the packages, and say go.

Then the EOS lets go. It compiles a seed and a blueprint and stops.
Ventures diverge freely, for their own good reasons, and nothing here
chases them. A check-in happens only when the venture asks for one, and
a check-in returns findings and candidate lessons and changes nothing.

## Building wide: graphs, lanes and one integrator

`packs/agentic-swarm/` is the twenty-first pack and it describes how we
build substantial work: fan out over a measured dependency graph, with
one integrator and a verifier that predates the lanes. Anything else is
either a single agent or an expensive mistake. The integrator is the
one session that commits the claims, adopts or discards what the lanes
return and regenerates the derived views. `OPERATORS_GUIDE.md` gives
those duties to the operator, and here the operator is Daniel.

What that means in practice:

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
- Agreement between lanes is never evidence of correctness. Agent
  attempts at the same specification fail together far more often than
  chance, so a vote proves nothing.

The pack carries its own counter-evidence, and it is strong: in the one
study that normalised tool access and accounting across ten benchmarks,
five of six multi-agent systems scored below a single-agent baseline
while costing more, one of them 286 per cent more tokens. The sixth
came out above the baseline by a margin inside the uncertainty band, at
24 per cent more tokens. Coordination cost grows faster than the work
does. No public benchmark measures the shape we use, so our own runs
are the best evidence we have, and the pack says that plainly rather
than claiming swarms are faster.

`kernel/templates/org/GRAPH_BUILD.tpl.md` compiles the usable half of
this into every ORG seed, so a venture gets the method too.

## How work is verified

Verification is staged by risk and by measured stability, never by a
percentage of completeness. There is no coverage gate.

- **From day one**: the risk floors, which never move; cheap executable
  checks (build, types, lint, schema, smoke) wired before the first
  feature lane opens; and the failing acceptance spine from Genesis.
- **Per change**: reproduce a bug before fixing it, write the oracle
  before gate-bearing work, pin behaviour before refactoring. Changes
  touching personal data or anything irreversible take the strict path.
- **At interface stability**: when a package declares its contract
  stable, contract tests on that boundary start blocking its neighbours.
- **At stabilisation**: only when the stability signals fire is the
  broad harness assembled. `packs/delivery-testing/PACK.md` states
  them, and states that they are starting values a venture overrides in
  its lock-book rather than measured thresholds. The harness is derived
  from the map and the specifications rather than from the code,
  authored or reviewed independently of the model that wrote the
  implementation, and mutation-checked before it is allowed to block
  anything.

**Test-first is no longer doctrine.** The rule in `packs/coding` that
required it is now a default: do it unless you record why not. Two
measurements moved it, and neither of them tests ordering head to
head. Prompting a frontier model for more tests across the five hundred
tasks of SWE-bench Verified changed test-writing behaviour on most
tasks and left the number of tasks resolved statistically unchanged.
And prompting a model with the buggy implementation in front of it cut
bug-revealing tests by about two thirds against giving it the correct
implementation, and by about 44 per cent against giving it the
specification. `packs/coding/PACK.md` carries both rows by evidence id.

Read those two together and the binding rule is narrower and better
evidenced than the one it replaces: **the artefact that decides whether
a change is correct must not be written by the agent holding that
implementation in context.** Ordering is ceremony. Independence is not.
Acceptance conditions authored at Genesis satisfy this by construction,
which is why a lane never has to stop for it.

## Studying something, and what happens to what you learn

Before v2.1 the EOS could only learn from published documents. It can
now be pointed at a product, a repository, a game, a design system or a
postmortem, and the procedure is PB-E11.

It only ever starts because Daniel points at something. It is never
scheduled.

1. **A lens contract first.** One page: what the source is and its exact
   version, how it was lawfully obtained, its licence and the
   jurisdiction that matters, the aspects being studied, the aspects
   deliberately excluded, how far the study may escalate (observe, docs,
   tests, source), and where the findings land. Daniel approves it in
   the room. Never carried: verbatim code, assets, expressive text, or
   anything that would make the result look like the source.
2. **One session reads the raw source, and only that session.** If the
   source is fetched live, the copy is frozen first and the frozen copy
   is what gets read.
3. **Findings keep their kinds apart**: direct observation, sourced
   fact, interpretation, inference, recommendation. Each is marked as
   something the source does well, does badly, or merely does
   differently, or as unknown, with the conditions that made it work.
4. **Conflicts are found before Daniel sees anything.** The findings are
   mapped against the packs, the registries, the policies, governance
   and prior lessons, and anything that contradicts a live rule names
   that rule.
5. **Then a bounded interview**, and his decisions become rows in
   `registry/lessons.json`. `registry/LESSONS.md` is the derived view of
   that file and is never hand-edited.

A lesson row carries where it came from, the lesson itself, its evidence
class, its disposition, its scope, when it applies, what it informs,
what it contradicts and what it replaces, the decision date and Daniel's
reasoning in a line.

The disposition is the useful part. A lesson can be reference only, a
dated registry fact, a ruling for one venture, a worked exemplar, an
implementation reference, experimental guidance with an expiry, a
decision guide, an estate default, or a candidate for binding. It can
also be **rejected, and the rejection stays in the ledger with its
reason**, which is the gap this fixes: a declined lesson used to vanish
and could be proposed again forever. Or **deferred**, which needs a
named trigger rather than a date alone.

Nothing here can make a rule binding. The workflow can propose it; the
promotion ladder in `GOVERNANCE.md` is unchanged and binding still needs
an accepted ADR and Daniel.

## Claims and derived views

Claims stop two sessions writing the same file. When more than one
session may write at once, the integrator assigns claims and commits
them before any lane is dispatched, and lanes never acquire or mutate
one. Once a claim set is committed it is exclusive: a session it does
not name may not create task records or modify product files, and its
work is quarantined for the integrator to adopt or discard. Liveness
comes from harness state or a recorded process id, and a timestamp alone
never authorises taking someone's claim.

A single session working alone does not hand-write a claim file first.
It is implicitly claimed, because there is nobody to collide with, and
git history plus the checker is what catches it going wrong (ADR-0008).

Records are canonical, views are generated. Task records under
`org/tasks/`, the evidence ledger, the lessons ledger, the coverage
matrix and the estate manifest hold the truth. `org/TASKS.md`,
`org/STATE.md`, `INDEX.md`, `registry/CAPABILITIES.md` and
`registry/LESSONS.md` are views, regenerated by the integrator and never
hand-edited.

## Less law, better kept

ADR-0008 went through the rules and asked one question of each: does it
prevent a real failure that is serious or hard to undo, and is it based
on law, on a standard, on measurement, or is it a safety floor? A rule
that answers yes stays **binding**. Everything else becomes a
**default**, which means do it unless you record why not. A default is
not a suggestion, and the monthly pass samples the recorded reasons.

What ADR-0008 loosens: claims are needed when work runs in parallel, not
when a lone session writes; a lane may open its own task record; task
records are for gate-bearing work and ordinary work records itself in
the commit message; four monthly cadences became one pass with four
sections and the two quarterly ones became on-demand; most line budgets
warn instead of failing; the tag list became the known set rather than
the permitted set; and the metadata minima shrank to the axes that
actually change what an agent does.

What did not change, and the ADR says why: the safety floors, the rule
that a derived file is never hand-edited, append-only decision records,
supersession stated in both directions, the promotion ladder, and the
decision budget. The honest counter-argument is recorded too, because
loose governance is how sixty-six false statements got into this tree in
the first place. So every loosened rule names what catches the failure
instead.

## The pack system

Knowledge is packs, disclosed in three levels: a first paragraph always
in context, a `PACK.md` body on activation, and guides, refs, exemplars
and recipes on demand. The contract is `packs/PACK_SHAPE.md`, including
the eleven-point definition of done. A domain that cannot meet that bar
stays a row in `registry/coverage.json` and is never described as
implemented.

`START.md` is retired and archived at `archive/v1-final:START.md`. Its job,
telling you what to read for your entry mode, is done by two things
now: the mode you are routed into by `python -m tools.eos route`, and
the activation rows in `packs/INDEX.md`. You no longer read a fixed
list before starting; the work decides what loads.

## Where to look for what

| Question | File |
| --- | --- |
| What am I allowed to do here? | `AGENTS.md`, then `GOVERNANCE.md` |
| How do I start a venture? | `inception/INCEPTION.md` |
| How does a venture get a build plan? | `inception/GENESIS.md` |
| How do I run a wide build? | `packs/agentic-swarm/PACK.md` |
| What does one task look like end to end? | `examples/v2-worked-lean.md`, `examples/v2-worked-high-assurance.md` |
| Which knowledge applies to this task? | `packs/INDEX.md` |
| What does the EOS know, and what does it not? | `registry/CAPABILITIES.md` |
| How is risk decided? | `kernel/POLICY_SPEC.md`, `kernel/GUARD_SPEC.md` |
| What metadata does this file need? | `kernel/METADATA_SPEC.md` |
| What is in flight, and who holds what? | `org/TASKS.md`, `org/STATE.md` |
| What have we studied, and what did we decide? | `registry/LESSONS.md` |
| Why is it like this? | `org/decisions/`, newest first |
| Which repos exist and which are governed? | `estate/ESTATE_MAP.md` |
| Where did that claim come from? | `registry/evidence.json` |
| What did v1 say? | the `archive/v1-final` tag, `archive/README.md` says how |
