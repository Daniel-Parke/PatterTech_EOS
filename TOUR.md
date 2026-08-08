---
summary: The teaching surface for EOS v2, what changed from v1 and why, the kernel, the packs and where to look
type: guide
tags: [eos]
review_by: 2027-01
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
ceremony: of the six commits after the v1.0.0 tag, **four were
unrecorded**, none was logged, and one was a doctrine edit with no
wargame behind it. A repo can be checker-green and still hold false
statements about itself, and this one did.

The benchmark measured the same thing from the other end. On the
R2-and-above tasks, the median v1 run spent **between 177 and 301
ceremony lines**, and it ended behind an operator gate that never
arrives on its own: `human_gates_pending`
finished at one or more on every migration and auth run, and on three
of the four bug-fix runs. Ceremony was not buying safety there. It was
buying a queue of things waiting for Daniel.

So v2 keeps the parts that earned their place and makes the rest
proportional. It also fills the knowledge gaps: v1 had one deep web
aesthetic and four thin modules, with nothing on product, coding, data,
agents, security or delivery.

## The five execution modes

Ceremony now attaches to the task, not to the calendar.

- **Express** (tier R0): reversible local work in one run. The commit
  message is the whole record. Targeted checks, self-merge, no files.
- **Standard** (R1, the default): one owner plans, implements and
  tests, with a task record under `org/tasks/`. Independent review when
  the router asks for it, otherwise a sampled review pool.
- **Exploration**: a sandboxed spike on a `spike/` branch the checker
  refuses to merge. Timeboxed. It exits discarded or hardened.
- **High-assurance** (R2 and R3): explicit invariants, a rollback plan,
  an acceptance oracle written independently before implementation and
  frozen, independent review, and a person for anything irreversible.
- **Parallel**: a wrapper, not a mode of its own. Each lane carries its
  own mode and its own claim.

PLAN, WORK and VERIFY are retired. The one separation kept is oracle
authorship, because it is the one with controlled evidence behind it.

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

## The decision budget

"Never invent" is replaced by three bands. **Free**: naming,
decomposition, test structure, patterns already in the tree, file
placement. Decide it, record it in the commit message. **Durable**: a
new dependency, a schema element, a public contract, a precedent. Decide
it, write a short ADR before merge. **Escalation**: money, legal,
personal-data ambiguity, the protected set, weakening a check, conflict
with stated intent. Never alone.

Express lives in the free band only. A durable decision converts the run
to Standard.

## Oracle independence

Whoever writes the gate tests for a change must not be holding its
implementation in context. Tests written after seeing faulty code catch
roughly half as many faults. At High-assurance the oracle is authored
first, hashed and frozen; amendments are append-only, authored by
someone other than the implementer, and the amendment rate is itself a
quality signal reviewed at retro.

## Claims and derived views

There is exactly one concurrency mechanism: claims assigned by the
integrator and committed to the integration branch before any lane is
dispatched. Lanes never acquire or mutate a claim. A session not named
in `org/claims.json` may not create task records or modify product
files; its work is quarantined for the integrator to adopt or discard.
Liveness comes from harness state or a recorded process id, and a
timestamp alone never authorises taking someone's claim.

Records are canonical, views are generated. Task records under
`org/tasks/`, the evidence ledger, the coverage matrix and the estate
manifest hold the truth. `org/TASKS.md`, `org/STATE.md`, `INDEX.md` and
`registry/CAPABILITIES.md` are views, regenerated by the integrator and
never hand-edited.

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
| Which knowledge applies to this task? | `packs/INDEX.md` |
| What does the EOS know, and what does it not? | `registry/CAPABILITIES.md` |
| How is risk decided? | `kernel/POLICY_SPEC.md`, `kernel/GUARD_SPEC.md` |
| What metadata does this file need? | `kernel/METADATA_SPEC.md` |
| What is in flight, and who holds what? | `org/TASKS.md`, `org/STATE.md` |
| Why is it like this? | `org/decisions/`, newest first |
| Which repos exist and which are governed? | `estate/ESTATE_MAP.md` |
| Where did that claim come from? | `registry/evidence.json` |
| What did v1 say? | the `archive/v1-final` tag, `archive/README.md` says how |
