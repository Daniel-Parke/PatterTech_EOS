---
summary: The ten topologies by canonical name, the pressure that licenses each, and the evidence behind it
kind: fact
scope: estate
sources: [EV-0001, EV-0048, EV-0051, EV-0052, EV-0053, EV-0077, EV-0078, EV-0079, EV-0084, EV-0088, EV-0089, EV-0108, EV-0111, EV-0112, EV-0116, EV-0121]
volatility: fast
review: on-change-of:agent-sdk-major-release
type: guide
tags: [eos, arch, tooling]
review_by: 2027-03
---

# Topology card

Canonical names. Use these exact strings when recording a decision, so
a reader and a checker see the same word.

| Topology | Licensed by | Evidence |
| --- | --- | --- |
| direct single-agent | nothing; this is the starting point | EV-0088, EV-0052 |
| sequential pipeline | stable stage order and a typed handover | EV-0077, EV-0116 |
| bounded loop | free agency wanted, resource envelope fixed | EV-0051, EV-0052 |
| router | classification is the decision | EV-0116, EV-0077 |
| dependency graph (DAG) | real dependencies, state inspected between steps | EV-0048, EV-0078 |
| fan-out/fan-in | decomposability high, shared-state coupling low, latency or coverage worth the cost | EV-0112, EV-0084 |
| orchestrator-worker | breadth-first search where coverage is the product | EV-0112 |
| evaluator-optimizer | an external oracle the generator does not hold | EV-0111, EV-0089, EV-0053 |
| event-driven resumable | run outlives its process, or failure localisation matters | EV-0001, EV-0121, EV-0079 |
| human checkpoint | irreversibility or external visibility | EV-0079, EV-0108 |

## The eight pressures

Use these exact names when justifying a promotion: decomposability,
shared-state coupling, oracle quality, reversibility, latency, cost,
context pressure, failure localisation.

Each pressure licenses specific moves and nothing else.

- Decomposability plus low shared-state coupling licenses fan-out/fan-in
  and orchestrator-worker, never on its own.
- Poor oracle quality forbids evaluator-optimizer and argues for a
  human checkpoint instead.
- Low reversibility demands a human checkpoint at the act.
- Latency licenses parallelism at a token multiple, and only there.
- Cost is a veto, never a licence.
- Context pressure licenses delegation with condensed returns, or
  just-in-time retrieval, which is usually cheaper.
- Poor failure localisation licenses the event log and tracing.

## Composition

Topologies stack rather than compete. The common shapes:

- direct single-agent inside a bounded loop, terminating in a human
  checkpoint. This is the default for almost everything.
- fan-out/fan-in over read-only inputs, joined by one writer, then a
  sequential pipeline to the externally visible act, ending at a human
  checkpoint.
- event-driven resumable wrapping any of the above when a run must
  survive a restart.
- evaluator-optimizer wrapping only the step that has an oracle, never
  the whole run.

## What the card does not say

It does not rank the topologies by quality. There is no controlled
study measuring topology against outcome; the ordering in the decision
rule comes from cost and blast radius, not from measured performance.
The benchmark figures behind the single-agent rows are narrow
single-repository coding results and several are maintainer-reported
(EV-0052). Treat them as evidence about that population and no wider.
