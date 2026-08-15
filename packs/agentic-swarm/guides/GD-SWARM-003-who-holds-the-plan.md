---
id: GD-SWARM-003
summary: Does a script hold the fan-out shape, or does a model decide it turn by turn?
kind: wargame
type: wargame
tags: [arch, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-SWARM-025]
applies_when: [fans_work_across_lanes]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0108, EV-0112, EV-0462]
review: on-change-of:agent-harness-major-release
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SWARM-003: who holds the plan?

## Decision question and stakes

Something has to decide how many lanes run, in what order, where the
barriers are and how results are recombined. That something is either
code you can read, diff and re-run, or a model deciding at execution
time. The fork matters because the plan and the intermediate results
otherwise compete for the same context window, and the plan loses.

## Doctrines or coverage gap under pressure

- `DOC-SWARM-025` (preference): If a step can be code, make it code.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether the shape is knowable in advance.** A partition already
  written is a shape; an open-ended investigation is not.
- **Re-run and audit needs.** Can you show what ran, in what order, and
  produce it again?
- **How much of the run's output the coordinator must hold.** A
  coordinator that reads every lane's full transcript is the fastest
  route to context exhaustion.
- **Cost per decision.** Ordering, filtering, counting and joining cost
  nothing in code and cost tokens plus non-determinism in a model.

Applicability is `fans_work_across_lanes`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. A script holds the plan

Assume `A. A script holds the plan` was selected and the outcome failed. Test this option's stated failure mechanism first: the up-front authoring, and the script becomes an artefact to maintain.

### Premortem for B. A model generates the workflow, then the runtime executes it

Assume `B. A model generates the workflow, then the runtime executes it` was selected and the outcome failed. Test this option's stated failure mechanism first: a generation step, and the honest caveat that nobody has isolated which mechanism produced the gap.

### Premortem for C. A lead model delegates turn by turn

Assume `C. A lead model delegates turn by turn` was selected and the outcome failed. Test this option's stated failure mechanism first: auditability, costs the plan sharing a window with the results, and invites the three failure modes the harness vendor names from its own experience: stopping early on partial completion, preferring its own results when asked to check them, and losing the goal through repeated summarisation (EV-0462, asserted rather than measured).

### Premortem for D. Peer agents coordinating by message

Assume `D. Peer agents coordinating by message` was selected and the outcome failed. Test this option's stated failure mechanism first: Lanes talk to each other and settle work between themselves. Buys almost nothing here. Error amplification against a single agent was 17.2 times for independent lanes and 4.4 times with a validating orchestrator, and inter-agent misalignment is one of the two largest failure categories in the annotated multi-agent corpus.

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

## Safe default

A, with the partition as the plan and a script that dispatches it. Move
to B when the harness offers it and the shape is genuinely
task-dependent. Save the script that produced a run you liked; it is
the reusable unit, not the prompt that produced it.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the shape is knowable in advance.** A partition already written is a shape; an open-ended investigation is not.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with the partition as the plan and a script that dispatches it. Move to B when the harness offers it and the shape is genuinely task-dependent. Save the script that produced a run you liked; it is the reusable unit, not the prompt that produced it.

**Exit condition:** Stop or roll back the selected branch when the up-front authoring, and the script becomes an artefact to maintain, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the shape is knowable in advance.** A partition already written is a shape; an open-ended investigation is not.

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

Barrier only where the downstream node needs every upstream result;
otherwise pipeline, because a barrier makes the slowest node the
critical path and makes an interrupted run expensive to resume. And if
a step can be code, make it code: ordering, filtering, joining,
counting and formatting belong in the orchestrator, where they are free
and deterministic.
### Historical ruling boundary

The baseline file carried 1 worked ruling note. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
