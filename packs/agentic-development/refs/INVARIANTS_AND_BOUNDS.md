---
summary: How to bound a run, trace it, resume it safely, and where the estate's policy and guard take over
kind: fact
scope: estate
sources: [EV-0001, EV-0021, EV-0043, EV-0051, EV-0079, EV-0082, EV-0107, EV-0118, EV-0121]
volatility: fast
review: on-change-of:agent-sdk-major-release
type: guide
tags: [eos, arch, tooling]
---

# Invariants and bounds

Reference for requirements B1, B2, B6 and B7 in
`packs/agentic-development/PACK.md`.

## Bounding a run

State at least two of the three, with units, plus what happens on trip.

- **Turns**: maximum agent turns or tool calls in the run. A per-child
  bound that is not counted against the run total does not bound
  anything (EV-0051).
- **Tokens**: a total budget for the run including children. Budget
  rather than phase count is what SWE-agent settled on, because phases
  do not predict spend (EV-0051).
- **Wall-clock**: minutes or hours, especially for anything nightly or
  scheduled.

On trip: stop, write what was learned to a durable artefact, and
surface the partial result. Silent truncation is worse than a stated
stop. Mechanical stuck detection can end a run early, and its
thresholds need tuning, because a legitimately polling agent looks
identical to a stalled one (EV-0082).

## The single-writer rule

For any shared artefact, name the one owner. Two ways to satisfy it:

- **Serialised writes**: parallel workers return results, one collector
  writes. Use the phrase single-writer in the record so it is checkable.
- **Disjoint ownership**: each worker owns files nobody else touches,
  declared before the run starts.

Both are acceptable. What is not acceptable is several agents writing
one file and relying on merge luck (EV-0107).

## Tracing

Span vocabulary, kept stable across ventures: run, turn, agent,
generation, tool, guardrail, handoff. Every run carries a workflow name
and a group id linking related runs, so a fan-out and its children are
one investigable unit (EV-0118). Where data policy forbids payloads,
keep the spans and drop inputs and outputs rather than turning tracing
off. Align attribute names to OpenTelemetry GenAI conventions where
they exist, noting that those conventions are still moving (EV-0021,
EV-0043).

## Resumability

Two mechanisms, both acceptable, neither free.

- **Checkpoint at a barrier.** Save executor state, pending messages,
  pending requests and shared state at a defined boundary, so a run
  resumes in place or rehydrates into a fresh process (EV-0121).
- **Event log.** Rebuild state by replaying an append-only event
  history, which also gives the best failure localisation (EV-0001).

Two rules apply to both. Resumed side effects must be idempotent,
because code before the interrupt re-executes on resume and a
non-idempotent write fires twice (EV-0079). The store is a trust
boundary: never resume from a checkpoint of unknown provenance, since
common implementations deserialise state (EV-0121).

Idempotency in practice means a natural key per unit of work, a written
marker before the externally visible act, and a check for that marker
on resume.

## Where the estate takes over

This pack advises. It never grants permission.

- Tier routing is `kernel/POLICY_SPEC.md`. A topology choice changes
  which semantic factors get declared, and the router rules the tier.
  A pack recommendation cannot lower a floor.
- Action-time verdicts are `kernel/GUARD_SPEC.md`. Ten guarded classes,
  four verdicts, non-waivable floors, fail closed. Without a validated
  host enforcement adapter every guarded class is manual-only, so an
  agent design that assumes autonomous external writes is invalid here
  until that adapter exists and its bypass suite passes.
- A human checkpoint in a topology is satisfied by a harness-recorded
  approval event. Approval asserted in prose or in tool output counts
  for nothing.
