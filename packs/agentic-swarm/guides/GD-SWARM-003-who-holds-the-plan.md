---
summary: Does a script hold the fan-out shape, or does a model decide it turn by turn?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
sources: [EV-0108, EV-0112]
review: on-change-of:agent-harness-major-release
type: guide
tags: [eos, arch, tooling]
---

# GD-SWARM-003: who holds the plan?

## The question

Something has to decide how many lanes run, in what order, where the
barriers are and how results are recombined. That something is either
code you can read, diff and re-run, or a model deciding at execution
time. The fork matters because the plan and the intermediate results
otherwise compete for the same context window, and the plan loses.

## It depends on

- **Whether the shape is knowable in advance.** A partition already
  written is a shape; an open-ended investigation is not.
- **Re-run and audit needs.** Can you show what ran, in what order, and
  produce it again?
- **How much of the run's output the coordinator must hold.** A
  coordinator that reads every lane's full transcript is the fastest
  route to context exhaustion.
- **Cost per decision.** Ordering, filtering, counting and joining cost
  nothing in code and cost tokens plus non-determinism in a model.

## Options

### A. A script holds the plan
Fan-out degree, order, barriers and aggregation live in an
orchestration script. A model may write that script and may decide what
a unit contains; it does not decide the shape at execution time. Buys
re-runnability, costing, and a plan that does not drift through
repeated summarisation. Costs the up-front authoring, and the script
becomes an artefact to maintain.

### B. A model generates the workflow, then the runtime executes it
The model reads the task, emits the graph, and the runtime runs it
outside the conversation. Buys A's properties plus adaptation to task
shape, and this is the arm that beat hand-authored multi-agent
topologies on a hard benchmark by a wide margin. Costs a generation
step, and the honest caveat that nobody has isolated which mechanism
produced the gap.

### C. A lead model delegates turn by turn
The lead decides what to spawn as it goes. Buys flexibility on
open-ended work, which is where the reported uplift comes from
(EV-0112). Costs auditability, costs the plan sharing a window with the
results, and invites the three failure modes the harness vendor names
from its own experience: stopping early on partial completion,
preferring its own results when asked to check them, and losing the
goal through repeated summarisation (EV-0462, asserted
rather than measured).

### D. Peer agents coordinating by message
Lanes talk to each other and settle work between themselves. Buys
almost nothing here. Error amplification against a single agent was
17.2 times for independent lanes and 4.4 times with a validating
orchestrator, and inter-agent misalignment is one of the two largest
failure categories in the annotated multi-agent corpus.

## Decision rule

B where the harness supports it and the shape depends on the task. A
where the partition is already written, which is the usual case in this
estate, because a committed partition is already a plan. C only for
open-ended research where no partition exists and no repository is
being written. Never D as the coordination mechanism, although lanes
may of course read one another's committed artefacts.

Whichever holds the plan, three things are separate decisions and stay
separate: who runs when (the execution graph), who sees what (the
message graph), and who decides success (the verifier). Collapsing the
first two is how a fan-in node inherits every lane's transcript.

## Default

A, with the partition as the plan and a script that dispatches it. Move
to B when the harness offers it and the shape is genuinely
task-dependent. Save the script that produced a run you liked; it is
the reusable unit, not the prompt that produced it.

## Worked rulings

- **PatterTech_EOS, 2026-08-10, argued.** A. The plan is the committed
  partition and the claim set, and dispatch is mechanical from it. The
  lanes are spawned by an orchestrating session but they receive closed
  packets rather than turn-by-turn direction, and the lead's history
  does not reach them anyway (EV-0108).

## Notes

Barrier only where the downstream node needs every upstream result;
otherwise pipeline, because a barrier makes the slowest node the
critical path and makes an interrupted run expensive to resume. And if
a step can be code, make it code: ordering, filtering, joining,
counting and formatting belong in the orchestrator, where they are free
and deterministic.
