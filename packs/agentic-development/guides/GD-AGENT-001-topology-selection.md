---
id: GD-AGENT-001
summary: Which of the ten agent topologies does this work need, and what pressure justifies promoting past a single agent?
kind: wargame
type: wargame
tags: [arch, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AGENT-006, DOC-AGENT-008, DOC-SWARM-012, DOC-SWARM-013, DOC-SWARM-024]
applies_when: [builds_agent_workflow]
engages_when: [agent_coordination_cost_is_material]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0001, EV-0048, EV-0051, EV-0052, EV-0053, EV-0077, EV-0078, EV-0079, EV-0084, EV-0086, EV-0088, EV-0089, EV-0106, EV-0107, EV-0108, EV-0109, EV-0111, EV-0112, EV-0116, EV-0121, EV-0452]
review: on-change-of:agent-sdk-major-release
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-AGENT-001: Which topology does this work need?

## Decision question and stakes

Ten shapes are available, from one agent in a loop to a resumable graph
of specialists behind a human gate. They differ in cost, coherence and
where failure lands. The fork is which one this piece of work actually
needs, and what evidence justifies anything richer than the simplest.

## Doctrines or coverage gap under pressure

- `DOC-AGENT-006` (default): Any topology above direct single-agent is recorded.
- `DOC-AGENT-008` (default): Start at direct single-agent with a strong oracle.
- `DOC-SWARM-012` (default): Do not swarm work a single agent already does well.
- `DOC-SWARM-013` (default): If the graph will not cut, do not swarm.
- `DOC-SWARM-024` (default): Run a single-agent control on a sample, and instrument the landing.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `builds_agent_workflow`. Engagement is `agent_coordination_cost_is_material`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Direct single-agent

Assume `A. Direct single-agent` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing until the job outgrows one window or one oracle (EV-0088, EV-0052).

### Premortem for B. Sequential pipeline

Assume `B. Sequential pipeline` was selected and the outcome failed. Test this option's stated failure mechanism first: flexibility when order is not actually stable (EV-0077, EV-0116).

### Premortem for C. Bounded loop

Assume `C. Bounded loop` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing but the discipline of setting the numbers (EV-0051, EV-0052).

### Premortem for D. Router

Assume `D. Router` was selected and the outcome failed. Test this option's stated failure mechanism first: a hop and a misroute mode (EV-0116, EV-0077).

### Premortem for E. Dependency graph (DAG)

Assume `E. Dependency graph (DAG)` was selected and the outcome failed. Test this option's stated failure mechanism first: ceremony, and a graph is easy to reach for too early (EV-0048, EV-0078).

### Premortem for F. Fan-out/fan-in

Assume `F. Fan-out/fan-in` was selected and the outcome failed. Test this option's stated failure mechanism first: a token multiple and demands a single writer at the join (EV-0112, EV-0084).

### Premortem for G. Orchestrator-worker

Assume `G. Orchestrator-worker` was selected and the outcome failed. Test this option's stated failure mechanism first: roughly an order of magnitude in tokens and suits neither shared context nor most coding (EV-0112).

### Premortem for H. Evaluator-optimizer

Assume `H. Evaluator-optimizer` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing but harm when the oracle is absent, because self-review without external feedback degrades answers (EV-0111, EV-0089, EV-0053).

### Premortem for I. Event-driven resumable

Assume `I. Event-driven resumable` was selected and the outcome failed. Test this option's stated failure mechanism first: a store, a trust boundary and idempotent side effects (EV-0001, EV-0121, EV-0079).

### Premortem for J. Human checkpoint

Assume `J. Human checkpoint` was selected and the outcome failed. Test this option's stated failure mechanism first: latency exactly where you want it (EV-0079, EV-0108).

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

## Safe default

A, bounded by C, with J at any irreversible act. Anything richer is
recorded per B5 in
`packs/agentic-development/PACK.md`, naming the pressure and the
failure mode it removes.

## Cheapest discriminating test

Compare one bounded single-agent baseline with the smallest justified decomposition under the same task set, model budget and external verifier. Measure useful accepted work and coordination cost separately.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, bounded by C, with J at any irreversible act. Anything richer is recorded per B5 in `packs/agentic-development/PACK.md`, naming the pressure and the failure mode it removes.

**Exit condition:** Stop or roll back the selected branch when nothing until the job outgrows one window or one oracle (EV-0088, EV-0052), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Decomposability**: do subtasks separate cleanly with no cross-talk?

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Current research boundary

EV-0452 is benchmark evidence across stated models, harnesses and task graphs. It supports decomposability, tool load and verifier placement as pressures, not a universal topology ranking or cut-off.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
