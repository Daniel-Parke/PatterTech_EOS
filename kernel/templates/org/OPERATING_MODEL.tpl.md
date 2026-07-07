---
summary: Operating model template, work types, risk tiers and gates, knowledge lifecycle, cadences, humans
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
---

# The Operating Model

How the organisation runs. One document, deliberately: a solo operator
should be able to hold the whole machine in their head. Sections: work,
risk and verification, prioritisation, parallel execution, knowledge,
cadences, metrics, humans.

## 1 · Work

### 1.1 Work types

Every work order declares exactly one type; the type sets its Definition
of Done emphasis.

| Type | Goal | Success looks like |
| --- | --- | --- |
| FEAT | New capability | Acceptance tests pass; docs updated |
| FIX | Defect removal | Failing repro test written first, now green; root cause logged |
| REFACTOR | Structure improvement | Behaviour identical (tests unchanged and green); measurable simplification |
| PERF | Speed or efficiency | Baseline measured, target met, regression guard added |
| MAINT | Hygiene (deps, cleanup, rot) | Sweep checklist complete; nothing behavioural changed |
| HARDEN | Security or resilience | Named threat mitigated; control verified; registry updated |
| COMPLY | Regulatory obligation | Registry obligation moves gap to met, with evidence |
| RESEARCH | Answer a question | Research note with sources, confidence, recommendation |
| DOCS | Knowledge and documentation | Accurate, linked, lifecycle front-matter present |
| OPS | Operational or infra action | Runbook followed or updated; system state verified |
| SPIKE | Timeboxed experiment | Question answered; code discarded or converted to orders |

<!-- scale: L -->
Default playbooks per type live in `org/playbooks/CATALOGUE.md`: FEAT
PB-010, FIX PB-011, REFACTOR and PERF PB-012, MAINT and DOCS PB-013,
RESEARCH and SPIKE PB-020, COMPLY PB-021, HARDEN PB-010 with PB-022,
OPS PB-031 and PB-032.
<!-- scale: end -->

### 1.2 The work order

<!-- scale: M -->
A work order is a row in `org/QUEUE.md`: id, title, type, risk tier,
status, acceptance checks and a done-when line, per the formats in
`org/TEMPLATES.md`. The queue is ordered; the top unblocked item is
next.
<!-- scale: end -->
<!-- scale: L -->
One Markdown file per unit of work, `org/work/items/WO-####-<slug>.md`,
front-matter per `org/TEMPLATES.md` (id, type, practice, priority, risk
tier, status, claims, depends_on, links). Body: context, scope in and
out, acceptance criteria as checkboxes, test specification,
verification requirements, notes log.

Lifecycle: draft, ready, in_progress, in_verification, done; terminal
alternatives blocked and cancelled. Status lives in front-matter; files
are not moved between directories while active. Done and cancelled
items are archived to `org/work/archive/` by the maintenance cadence.
<!-- scale: end -->

Intake, the only four doors:

1. **Human intent**: the operator asks for something; PLAN drafts the
   orders.
2. **Cadence findings**: audits, reviews and registry gaps become
   orders.
3. **Verification failures and incidents**: CI, VERIFY findings and
   production alerts become FIX or OPS orders.
4. **Worker suggestions**: any session may file a suggestion; triage
   promotes, merges or declines with reasons. This is the sanctioned
   outlet for "while I was in there I noticed"; acting on it directly
   is scope creep and forbidden.

### 1.3 Definition of Done (universal baseline)

All acceptance boxes checked. Required tests written first where the
type demands, all green locally and in CI. Lint and types clean.
Migrations additive and reversible with schema docs updated. Security
checklist for the change addressed. Affected docs and knowledge updated
in the same order. Gates for the tier passed. Merged to a green `main`.
`org/STATE.md` and the session log updated.

## 2 · Risk and verification

### 2.1 Risk tiers

<!-- scale: M -->
| Tier | Meaning | Examples | Gates |
| --- | --- | --- | --- |
| T1 | Trivial, reversible | copy, comments, internal docs | G1 |
| T2 | Standard change | typical feature or fix in one surface | G1 + G2 |
| T3 | Sensitive or irreversible | schema, auth, money, personal data, public surfaces, infra, the protected set, data deletion | G1 + G2 + G3, ADR where the constitution demands one |
<!-- scale: end -->
<!-- scale: L -->
| Tier | Meaning | Examples | Gates |
| --- | --- | --- | --- |
| T1 | Trivial, reversible | copy, comments, internal docs, log tweaks | G1 |
| T2 | Standard change | typical feature or fix in one surface | G1 + G2 |
| T3 | Sensitive | schema, auth, money, public surfaces, personal-data paths, infra, dependencies with install scripts | G1 + G2 + G3 |
| T4 | Constitutional or irreversible | constitution, roles, ADR reversals, data deletion, production data migration, key rotation | G1 + G2 + G3 + written ADR |
<!-- scale: end -->

PLAN assigns the tier at triage; VERIFY may raise it, never lower it.
When in doubt, the higher tier applies.

### 2.2 Gates

- **G1, automated.** The CI pipeline the stack profile defines: lint,
  typecheck, unit and integration suites against real services,
  contract-drift checks, build, secret scan, dependency audit. G1 is
  the floor for everything, including docs.
- **G2, independent review.** A separate VERIFY session (never the
  authoring session) reviews the diff against the order, the spec, the
  constitution and the relevant standards; verdict recorded on the
  order.
- **G3, human approval.** The operator approves in writing before merge
  or execution.
<!-- scale: L -->
- **G4, post-release verification.** Smoke checks, monitors and error
  rates after deploy; failures open FIX orders.
- **G5, periodic audit.** Practice audits on cadence sample merged work
  and system state; findings become orders. G5 keeps G1 to G4 honest
  over years.
<!-- scale: end -->

Iron rules: no session merges its own T2-or-above work. Gate results
are recorded on the order. A red gate is never bypassed (Part II
Article 6), and the three-strikes rule in `org/START.md` stops the line
after three distinct failed fix attempts on the same check.

## 3 · Prioritisation

Simple by design: P0 (drop everything: broken main, live harm, legal
deadline), P1 (current milestone critical path), P2 (valuable, not
blocking), P3 (someday). Within a priority the order is explicit in the
queue, set by PLAN at triage; WORK sessions take from the top unless
their launcher names an item. Tie-breaking heuristic, judgement not
formula: compliance deadlines and risk burn-down beat features;
unblocking beats everything of equal value; smallest first among
equals.

<!-- scale: L -->
## 4 · Parallel execution

Scale is limited by verification bandwidth and merge throughput, not by
how many agents can be spawned. Defaults, raised deliberately or never:

- **WIP limit:** at most 2 concurrent WORK sessions; natural partitions
  are the venture's surfaces.
- **Isolation:** every WORK session runs in its own git worktree on
  branch `work/WO-####`. Never two sessions in one working directory.
- **Claims:** each in-progress order declares the path globs it will
  touch. Triage must not mark two orders ready-and-parallel with
  overlapping claims. One owner per file-scope at a time.
- **Merging:** squash-merge to `main` through the tier's gates, same
  session where possible; branch deleted after merge. If a session ends
  un-merged: a `wip:` commit plus a precise handoff on the order and in
  `org/STATE.md`.
- **Logs are conflict-free by construction:** every session writes its
  own file under `org/logs/YYYY-MM/`; shared files touched at close are
  only `org/STATE.md` and the order. Keep both edits minimal.
<!-- scale: end -->
<!-- scale: M -->
## 4 · One session at a time

WIP is 1. Each session works on a short-lived branch off `main` and
merges through its gates before the next session starts. The
`active_session` line in `org/STATE.md` is the claim: check it at
session start, clear it at close, treat a stale claim older than a day
as abandoned.
<!-- scale: end -->

## 5 · Knowledge

<!-- scale: L -->
### 5.1 Layout

`org/knowledge/registry/` holds requirement registries (`REG-*`): the
obligation, control, verification tables per practice. The registry
pattern is the universal mechanism for "what must be true and how we
prove it". `org/knowledge/research/` holds L0 research notes, dated,
sourced, confidence-marked. `org/knowledge/guidance/` holds L1
synthesised guidance. `org/standards/` holds L2 binding standards,
referenced by gates and playbooks. `org/decisions/` holds ADRs.
`org/playbooks/` holds procedures.

### 5.2 The promotion pipeline (Part II Article 7 in practice)

L0 research becomes L1 guidance, L1 becomes L2 standard, L2 becomes L3
automated check. Promotion is explicit work: a PLAN session reviews L0
and L1 items, promotes what has proven out, marks sources, sets
`review_by`, and, the end-state, files orders to encode L2 standards as
L3 automation (lint rules, CI gates, tests, monitors) so compliance
stops costing attention. Every item's front-matter carries id, status,
maturity, owner practice, sources, created, review_by and supersession
links. Expiry generates review work, not silent trust.

### 5.3 Where a fact lives

Business intent in the venture brief and product docs. Law and
obligation in the registry. Decision in an ADR. Binding rule in a
standard. Procedure in a playbook. Current state in `org/STATE.md` and
order front-matter. History in logs, archives and git. If a fact could
live in two places, it lives in the more upstream one and is linked
from the other.
<!-- scale: end -->
<!-- scale: M -->
Knowledge lives small at this scale: decisions in `org/decisions/`
(ADRs), rulings and contracts in the lock-book, everything else in the
venture brief or the queue. Research conclusions carry sources and a
`review_by` date wherever they land; expired items are suspect (Part II
Article 7). If recurring instructions or thresholds start accumulating,
that is the rescale trigger talking.
<!-- scale: end -->

## 6 · Cadences (the heartbeat)

Continuous improvement is mechanised as recurring sessions defined in
`org/CADENCE.md` (schedule, procedure, role, last_run, next_due). The
operator launches whatever is due. Every cadence, whatever the
discipline, runs the same loop: review current state, compare against
registry and standards, identify gaps, file and prioritise orders,
implement separately, verify, update the registry and knowledge, adjust
the checks.

## 7 · Metrics

<!-- scale: L -->
`org/metrics/SCOREBOARD.md` is a small honest table updated by
cadences, not a dashboard fetish. Track only what changes decisions:
releasable-main rate, escaped defects, open audit findings by severity,
registry gap counts, knowledge items expired, agent spend against
budget, cycle time from ready to done. Anything worth graphing later
can be derived from logs and git.
<!-- scale: end -->
<!-- scale: M -->
No scoreboard at this scale. The retrospective cadence reads the queue,
the logs and git directly; if a number starts mattering enough to
track, note it in `org/STATE.md` or rescale.
<!-- scale: end -->

## 8 · Humans

The operator's contract, expanded in the operators guide: launch due
sessions, answer `org/QUESTIONS.md`, approve top-tier gates and
releases, review VERIFY verdicts on sampled work, own accounts, spend
and legal signatures. Everything else is the organisation's job. Budget
guardrail: agent spend is logged per session (estimates acceptable);
triage pauses P2 and P3 work if monthly spend exceeds the figure set in
`org/STATE.md`.

*Anti-patterns this model exists to prevent:* persona proliferation
(specialists as chat characters instead of practices), orchestration
theatre (frameworks before verification bandwidth exists), memory
sprawl (knowledge in chats and vendor tools instead of the repo),
silent scope creep, self-approval, prompt-rot (detail in prompts
instead of procedures), derived-state drift (generated indexes treated
as truth), and big-bang documentation written once and trusted forever.
