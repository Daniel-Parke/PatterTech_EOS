---
summary: Which of the ten agent topologies does this work need, and what pressure justifies promoting past a single agent?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
sources: [EV-0001, EV-0048, EV-0051, EV-0052, EV-0053, EV-0077, EV-0078, EV-0079, EV-0084, EV-0086, EV-0088, EV-0089, EV-0106, EV-0107, EV-0108, EV-0109, EV-0111, EV-0112, EV-0116, EV-0121]
review: on-change-of:agent-sdk-major-release
type: guide
tags: [eos, arch, tooling]
review_by: 2027-03
---

# GD-AGENT-001: Which topology does this work need?

## The question

Ten shapes are available, from one agent in a loop to a resumable graph
of specialists behind a human gate. They differ in cost, coherence and
where failure lands. The fork is which one this piece of work actually
needs, and what evidence justifies anything richer than the simplest.

## It depends on

Eight pressures. Name the ones that are active; each is the licence for
a specific promotion.

- **Decomposability**: do subtasks separate cleanly with no cross-talk?
- **Shared-state coupling**: how much do they write to the same thing?
- **Oracle quality**: is there external truth that says the work is
  right, and how good is it?
- **Reversibility**: can the act be undone without cost or apology?
- **Latency**: is wall-clock a real constraint or a preference?
- **Cost**: what token multiple is the outcome worth?
- **Context pressure**: does the whole job fit one window with room to
  think?
- **Failure localisation**: when it goes wrong, can you tell where?

## Options

### A. Direct single-agent
One agent, one context, tools in a loop. Cheapest, most coherent, easy
to trace. Costs nothing until the job outgrows one window or one
oracle (EV-0088, EV-0052).

### B. Sequential pipeline
Fixed stages, typed handover between them. Buys determinism of order
and a clear place to validate. Costs flexibility when order is not
actually stable (EV-0077, EV-0116).

### C. Bounded loop
Free agency inside a hard envelope of turns, tokens or wall-clock.
Buys exploration you can afford. Costs nothing but the discipline of
setting the numbers (EV-0051, EV-0052).

### D. Router
A classifying step hands off, and the specialist owns what follows.
Buys separation where routing is the real decision. Costs a hop and a
misroute mode (EV-0116, EV-0077).

### E. Dependency graph (DAG)
Nodes with declared edges, state inspectable and editable between them.
Buys real dependency ordering, retries and resumption points. Costs
ceremony, and a graph is easy to reach for too early (EV-0048,
EV-0078).

### F. Fan-out/fan-in
Independent workers over separable inputs, results gathered by one
collector. Buys wall-clock and coverage on read-mostly work. Costs a
token multiple and demands a single writer at the join (EV-0112,
EV-0084).

### G. Orchestrator-worker
A lead agent decomposes, spawns workers, holds the plan and writes the
result. Buys breadth-first search where coverage is the product. Costs
roughly an order of magnitude in tokens and suits neither shared
context nor most coding (EV-0112).

### H. Evaluator-optimizer
A generator and a separate evaluator holding external truth, iterating
until the oracle passes. Buys real improvement where the oracle is
strong. Costs nothing but harm when the oracle is absent, because
self-review without external feedback degrades answers (EV-0111,
EV-0089, EV-0053).

### I. Event-driven resumable
State on an event log or checkpoint barrier, so a run outlives its
process. Buys survival across restarts and long pauses, and gives the
best failure localisation. Costs a store, a trust boundary and
idempotent side effects (EV-0001, EV-0121, EV-0079).

### J. Human checkpoint
Execution pauses for a recorded approval. Buys a stop before harm.
Costs latency exactly where you want it (EV-0079, EV-0108).

## Decision rule

Start at A. Then, in this order, promote only on an active pressure.

If any act is irreversible or externally visible, add J at that act.
If the run must survive a restart or a long pause, add I. If subtasks
are decomposable and read-mostly and latency or coverage justifies the
token multiple, add F, with one writer at the join. If the decomposition
itself needs planning and the product is coverage rather than a change
to shared state, use G instead of F. If real dependencies exist and
state must be inspected between steps, use E. If stages have a stable
order and a typed handover, B. If classification is the decision, D. If
external truth exists that the generator does not hold, wrap the
generating step in H. Bound whatever you chose with C.

Topologies compose. A run is commonly A inside C, fanned out as F,
terminating in J.

## Default

A, bounded by C, with J at any irreversible act. Anything richer is
recorded per binding requirement B5 in
`packs/agentic-development/PACK.md`, naming the pressure and the
failure mode it removes.

## Worked rulings

- **PatterTech_EOS (2026-08, argued)**: the v2 pack build itself. Eight
  pack lanes fan out (F) over disjoint claimed paths, one integrator
  writes every shared registry, and the release stays behind a human
  checkpoint (J). Pressures: decomposability high, shared-state
  coupling forced to zero by path claims, reversibility low at release.
  Recorded in `org/claims.json` and ADR-0002.
- **PatterTech_EOS (2026-08, inherited)**: the checker and tooling work
  ran as A inside C with the test suite as oracle. No pressure was
  named for anything richer, so the default stood.
