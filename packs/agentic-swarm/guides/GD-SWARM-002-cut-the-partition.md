---
id: GD-SWARM-002
summary: Where do the cuts go when work is split across lanes, and what is never cut at all?
kind: wargame
type: wargame
tags: [arch, delivery, eos, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SWARM-001]
applies_when: [fans_work_across_lanes]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0053, EV-0109, EV-0471]
review: on-change-of:agent-harness-major-release
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SWARM-002: where do the cuts go?

## Decision question and stakes

Once the answer to `GD-SWARM-001` is fan-out, something has to decide
which lane owns what. This is the decision the run's cost and its
conflict rate both come from, and it is made once, before any lane
starts. A cut made from the feature list looks reasonable and produces
lanes that write the same files.

## Doctrines or coverage gap under pressure

- `DOC-SWARM-001` (binding): The partition is written before any lane starts, and it is cut on the dependency graph.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **The actual dependency graph**, from static analysis or from the
  product map, not from the backlog headings.
- **Coupling across the cut.** The objective is to minimise what
  crosses, not to equalise what sits inside.
- **Hub artefacts.** Registries, schemas, routing tables, shared types,
  configuration and every derived file. These are the files most lanes
  want to touch.
- **The failure surface.** If one build, one suite or one integration
  target can fail for everyone at once, the cut has not finished.
- **Lane capacity.** A lane should hold about five or six deliverables,
  each with a clear artefact, and should fit inside the model's working
  horizon for that class of work. Agent success decays exponentially
  with the human duration of the task, at a roughly constant hazard per
  minute, so node size is a reliability parameter rather than a
  convenience (EV-0471).

Applicability is `fans_work_across_lanes`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Cut by dependency-graph community
Build the graph, pull hub files out into single-owner or
integrator-owned groups, then partition the remainder by community
detection and schedule in dependency order. Buys the measured result:
better pass rate than sequential at roughly two thirds the cost. Costs
a graph you have to build and keep current.

### B. Cut by product-map component
Where a written product map already declares components and contracts,
use those boundaries and verify them against the file graph rather than
computing communities from scratch. Buys speed and a partition a person
can read. Costs accuracy where the map has drifted from the code.

### C. Cut by file or by feature
One lane per file, or one lane per backlog item. Buys nothing measured:
it cost 44 to 60 per cent more than sequential for one to three points
of pass rate. Listed here so it is recognised and refused.

### D. Do not cut
Cohesion returns one group, or the work is a chain. Run it in one lane.

## Failure premises

### Premortem for A. Cut by dependency-graph community

Assume `A. Cut by dependency-graph community` was selected and the outcome failed. Test this option's stated failure mechanism first: Costs a graph you have to build and keep current.

### Premortem for B. Cut by product-map component

Assume `B. Cut by product-map component` was selected and the outcome failed. Test this option's stated failure mechanism first: accuracy where the map has drifted from the code.

### Premortem for C. Cut by file or by feature

Assume `C. Cut by file or by feature` was selected and the outcome failed. Test this option's stated failure mechanism first: 44 to 60 per cent more than sequential for one to three points of pass rate. Listed here so it is recognised and refused.

### Premortem for D. Do not cut

Assume `D. Do not cut` was selected and the outcome failed. Test this option's stated failure mechanism first: Cohesion returns one group, or the work is a chain. Run it in one lane.

## Decision rule

A where the code exists and a graph can be computed. B at the start of
a venture, when the map is the only thing there, with the cut re-checked
against the file graph as soon as code exists. Never C. D whenever A or
B returns a single group, and record that it did.

Then, whichever was used, do these four things before dispatch:

1. **Hold back the hubs.** Every artefact more than one lane would
   write becomes integrator-owned. This is binding requirement B1 in
   the pack, and it is the graph-engineering addition to the neighbour
   pack's one-writer rule: not just one owner per file, but a class of
   file with no owner but the integrator.
2. **Split the failure surface.** Sixteen agents pointed at one
   monolithic build hit identical bugs at the same moment and
   parallelism was worth nothing until the failure was decomposed with
   delta debugging (EV-0053).
3. **Write the partition down.** Per lane: files owned, interfaces
   consumed, interfaces published, lanes depended on. Handing agents
   the relations rather than making them infer relations is worth 22 to
   50 points of delivery score.
4. **Commit the claims.** The claim file is the mutex, and its history
   is the audit trail.

## Safe default

A, with hubs held back and the partition committed before dispatch.
Five or six deliverables per lane.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****The actual dependency graph**, from static analysis or from the product map, not from the backlog headings.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with hubs held back and the partition committed before dispatch. Five or six deliverables per lane.

**Exit condition:** Stop or roll back the selected branch when Costs a graph you have to build and keep current, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The actual dependency graph**, from static analysis or from the product map, not from the backlog headings.

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

In the annotated multi-agent corpus, the two largest failure categories
are specification and system design, and misalignment between agents.
Both sit before or between the lanes rather than in the checking step
(EV-0109). The partition is where most of that is either prevented or
created. A partition also decays: the moment a lane
publishes an interface the graph did not have, the cut is stale and the
integrator, not the lane, decides what to do about it.
### Historical ruling boundary

The baseline file carried 1 worked ruling note. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
