---
summary: Venture playbook catalogue template, PB-001 to PB-051, one versioned procedure per session category
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
---

# Playbook catalogue

A playbook is a versioned procedure for a category of session. Launcher
prompts stay tiny and stable ("run PB-021"); the evolving detail lives
here, so improving a procedure means editing one file, never hunting
through prompt collections. When a playbook outgrows a page, split it
to `org/playbooks/PB-###-<slug>.md` and leave a one-line pointer in
this catalogue. Playbooks are owned by PLAN; improvements arrive via
suggestions and the monthly retrospective (PB-050).

Every playbook implicitly begins with the START bootstrap and ends with
the START close-out. The steps below are the middle.

## PB-001 · Genesis (PLAN, one-off)

Purpose: turn the Session 0 seed into a complete, buildable
organisation.

1. Read the entire `org/` tree, the venture brief and every compliance
   registry.
2. Produce the product design set under `org/product/`: the domain
   model (entities, invariants, event registry, any scoring model with
   worked examples), the architecture (context and container views,
   auth and data flows, environments), the roadmap (the version-one
   fence and the layer map), the brand and voice references the
   lock-book cites, and, where the venture has a database, the schema
   documentation with seams for later layers.
3. Produce the initial standards set under `org/standards/`, each with
   front-matter and `review_by`.
4. Write the ADR set for every judgement call taken, flagging each in
   `org/STATE.md` for the human.
5. Write the full version-one specs under `org/product/specs/` with
   test specifications (Given/When/Then at the levels each surface
   needs).
6. Convert the registries' gap rows and the specs into a complete,
   ordered backlog, foundation tasks first (scaffolds, CI, the failing
   acceptance suite).

## PB-010 · Feature development (WORK)

1. From the order's test specification, write failing tests first;
   acceptance-level skips are lifted only when green end to end.
2. Implement minimally to green; refactor with tests green.
3. Honour the constitution's Part I articles the spec names (choke
   points, audited events, append-only rules); add empty, error and
   loading states for UI surfaces.
4. Update docs, contracts and schema in the same order; small commits;
   gates per tier.

## PB-011 · Bug fix (WORK)

1. Reproduce with a failing test before reading for a fix. No repro:
   downgrade to a research note on the order and escalate.
2. Fix the root cause, not the symptom; the repro test stays forever.
3. Write a three-line root-cause note on the order; if the class of bug
   could recur, file a suggestion for a standard or automated check.

## PB-012 · Refactor and performance (WORK)

1. Baseline first: behaviour pinned by existing tests (add
   characterisation tests if thin); for PERF, measure and record the
   number being improved.
2. Change structure or behaviour, never both in one order.
3. Prove it: tests unchanged and green; the PERF target met and a
   regression guard added; the complexity delta noted on the order.

## PB-013 · Maintenance sweep (WORK, cadence)

Checklist run: dependency updates within policy (lockfile refresh,
audit clean) · expired `review_by` knowledge flagged · done items and
old logs archived · dead code and TODO census filed as suggestions · CI
duration and flake check · scoreboard row updated. Nothing behavioural
changes in a MAINT order; discoveries become suggestions.

## PB-020 · Research (WORK or PLAN)

1. Frame the question, the decision it informs and the good-enough bar
   on the order.
2. Gather from primary sources first (regulator, vendor docs, standards
   bodies); record every source with the date accessed.
3. Write the L0 note in `org/knowledge/research/`: findings, confidence,
   recommendation, expiry.
4. File the follow-on: a promotion suggestion, or the orders the
   findings imply. Research that changes nothing must say so.

## PB-021 · Compliance and regulation watch (cadence)

1. For each jurisdiction registry: check the primary sources for change
   (the regulator's news and guidance, the legislation register, the
   watch-list in the registry header).
2. Diff against registry entries: a new obligation adds a row (status
   gap) plus an order; a changed obligation updates the row and
   re-verifies the control; nothing changed records the check with date
   and sources in the registry changelog.
3. Verify evidence freshness for met rows on their `review_by`.
4. Escalate anything needing legal judgement to `org/QUESTIONS.md`.

This same shape, pointed at a different registry, is how any practice
watches its outside world (security advisories, accessibility updates,
vendor deprecations). Reuse it, don't fork it.

## PB-022 · Practice audit (VERIFY, cadence, rotating)

The generic continuous-improvement loop; see the VERIFY charter's
practice audit. Inputs: the practice charter, its registry, the last
audit. Outputs: the audit report, registry status updates, orders for
critical and major findings, the scoreboard update. The first audit of
a practice bootstraps its registry from standards and observed reality.

## PB-030 · Change review (VERIFY)

See the VERIFY charter's change review; the checklist is authoritative
there. Record the verdict and evidence on the order.

## PB-031 · Release (WORK)

1. Preconditions: green `main`, the acceptance skip-count at the agreed
   bar, no open critical findings, the human's approval recorded.
2. Follow the deploy runbook: migrate, deploy each surface, post-deploy
   smoke checks against live URLs, monitor window.
3. Tag, scoreboard, log. Any post-deploy failure: roll back per
   runbook, file the FIX order, write the root-cause note.

## PB-032 · Incident (WORK, P0)

Stabilise first (rollback or kill-switch per runbook), then diagnose,
then the minimal durable fix. Timeline and root cause written while
fresh. Follow-up orders for whatever was missing (a monitor, a test, a
control). Registry and standards updated if a control failed.
Blameless, evidence-led.

## PB-040 · Knowledge promotion (PLAN, cadence)

Review L0 and L1 items proven in practice. Promote (research to
guidance to standard) with sources and `review_by`. For each standard
ask "can a machine enforce this?" and file the automation order. Mark
superseded items; prune contradictions. This is the organisation's
compounding-interest mechanism; protect it.

## PB-050 · Retrospective and self-improvement (PLAN, monthly)

Inputs: the month's logs, audit reports, scoreboard, verification
verdicts, suggestion queue, operator friction notes. Outputs: what
worked and what hurt (five evidenced bullets each) · playbook, template
and launcher improvements applied · operating-model change proposals
(an ADR where protected) · WIP, budget and cadence tuning · one
deliberate experiment for next month. The organisation edits itself
here, nowhere else, and never mid-task.

## PB-051 · Stakeholder update (PLAN, cadence)

Compile, don't compose: from the period's session logs, STATE, verdicts
and scoreboard, produce `org/product/updates/SU-YYYY-WW.md` with
exactly four sections, Built, Blocked, Changed, Next, plus the current
acceptance burn-down where an agreement defines one. One page, plain
English, no jargon; written for the stakeholder the agreement names,
sent by the operator. Anything needing their decision links a QUESTIONS
item.

*Adding a playbook:* copy the closest existing one, give it the next PB
number, state purpose, trigger, steps and outputs, and register any
cadence in `org/CADENCE.md`. If you write the same session instructions
twice, that is the signal.
