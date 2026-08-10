---
summary: Proposed cold-agent acceptance drill for the swarm pack, cut a partition and refuse the bad one
type: example
tags: [eos]
---

# Drill proposal: cut a partition, or refuse to

Proposed, not frozen. No drill spec exists for this pack yet, and no
drill run is authorised by the task that wrote it. This file states
what the drill should ask so that whoever freezes it does not have to
rediscover the shape.

**The prompt.** Give a cold agent a small repository description with a
stated dependency graph, a backlog of seven items, one file every item
touches, and one end-to-end suite that gates everything. Ask for a
partition and a dispatch plan.

**What a pass looks like.** The agent isolates the shared file as
integrator-owned rather than assigning it. It splits or refuses the
single gating suite. It cuts on the graph rather than on the seven
backlog items. It states a lane count with a reason. It names a
verifier that exists before the lanes. It says plainly if the graph
does not cut, rather than producing a partition anyway.

**What a fail looks like.** Seven lanes, one per backlog item, with the
shared file in more than one write set and no mention of the gating
suite.

**Why this shape.** The failure the pack most wants to prevent is a
cut made from the feature list, and it is the failure a cold agent
makes by default because the backlog is the most legible thing in the
prompt. A drill that only asks whether the agent can recite the rules
would pass on that.

**Acceptance criteria should stay mechanical.** Regex and count
assertions over one output file, in the house style, so no model grades
the drill. See `packs/agentic-swarm/CHECKS.md` for the rows that are
already mechanical; C1 to C5 map onto this drill almost directly.
