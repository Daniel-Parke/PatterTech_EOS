---
summary: Where do the cuts go when work is split across lanes, and what is never cut at all?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
sources: [EV-0053, EV-0109, EV-0471]
review: on-change-of:agent-harness-major-release
type: guide
tags: [eos, arch, delivery]
---

# GD-SWARM-002: where do the cuts go?

## The question

Once the answer to `GD-SWARM-001` is fan-out, something has to decide
which lane owns what. This is the decision the run's cost and its
conflict rate both come from, and it is made once, before any lane
starts. A cut made from the feature list looks reasonable and produces
lanes that write the same files.

## It depends on

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

## Default

A, with hubs held back and the partition committed before dispatch.
Five or six deliverables per lane.

## Worked rulings

- **PatterTech_EOS, 2026-08-10, argued.** B, because the unit of work
  was documentation with an explicit file map, verified against a
  disjointness check across lane write sets. Every derived file,
  `GOVERNANCE.md`, `org/` and the kernel specifications went to the
  integrator, which is why a lane authoring a pack could not also add
  its own row to `registry/coverage.json`.

## Notes

In the annotated multi-agent corpus, the two largest failure categories
are specification and system design, and misalignment between agents.
Both sit before or between the lanes rather than in the checking step
(EV-0109). The partition is where most of that is either prevented or
created. A partition also decays: the moment a lane
publishes an interface the graph did not have, the cut is stale and the
integrator, not the lane, decides what to do about it.
