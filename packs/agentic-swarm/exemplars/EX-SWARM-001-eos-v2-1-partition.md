---
summary: The partition, packets and merge plan for the EOS v2.1 build, written as it was dispatched
kind: exemplar
scope: estate
type: example
tags: [eos, arch, delivery]
---

# EX-SWARM-001: the EOS v2.1 partition

A worked example, taken from the run this pack was written inside. It
records the partition as dispatched on 2026-08-10, and the two places
where that partition departed from this pack's own rules. Whether it
landed cleanly is a fact for that run's own record and its merge
verdicts, not for this file, and nothing below should be read as an
outcome claim.

## The situation

One documentation repository, no build, twenty existing packs and a
kernel of specifications and templates. The job, authorised by ADR-0006
and ADR-0008, was a wide edit: a new inception phase, a new registry, a
twenty-first pack, an authority audit across every existing pack, a
licence declaration and a correction pass over false statements in the
tree. Twelve lane task records, T-0014 to T-0025. Verification is
mechanical and partial: `python -m tools.eos check --repo` decides
structure, path and id resolution, front-matter and voice, and decides
nothing about whether an argument is any good.

## Step 1: does this fan out at all?

Against `packs/agentic-swarm/guides/GD-SWARM-001-swarm-or-single-agent.md`:

- **Decomposable?** Yes. Packs are independent bodies of prose. The
  coupling is through a small set of shared registries and indexes.
- **Oracle?** Partial and decidable for the mechanical half only. It
  predates every lane by months, which satisfies the independence half
  of B7 for what it covers, and covers no argument at all.
- **Single-agent baseline?** Low. One session could not hold twenty
  packs plus a kernel plus new material inside one context.
- **Hub density?** High but enumerable, which is the condition that
  makes hub isolation possible rather than hopeless.

Ruling: fan out, twelve lanes. Twelve is more than B7 permits against an
oracle this thin, and the departure is recorded at the end of this file
rather than argued away here.

## Step 2: the cut

Against `packs/agentic-swarm/guides/GD-SWARM-002-cut-the-partition.md`,
option B, because the map exists and the artefacts are files rather
than a computed dependency graph.

**Lane-owned.** One lane per new or heavily reworked area: the swarm
pack directory, the inception phase file, the lessons registry, the
licence and provenance sweep, and the authority audit split by pack
group. Each lane owns whole directories, not scattered files.

**Integrator-owned, delegated to nobody.** `GOVERNANCE.md`; everything
under `org/`, including the claim file and the decision records; every
derived file, meaning `INDEX.md`, `packs/INDEX.md`,
`packs/GUIDE_INDEX.md`, `registry/CAPABILITIES.md`, `org/TASKS.md` and
`org/STATE.md`; the kernel specifications `kernel/SCALE_MATRIX.md`,
`kernel/POLICY_SPEC.md` and `kernel/GUARD_SPEC.md`; and `LICENSE`,
`NOTICE` and `CHANGELOG.md`.

**The hub that went to a lane.** `registry/evidence.json` is the
clearest hub in the repository. Every lane produces evidence, and if
every lane wrote to the ledger, twelve lanes would collide on one file
and race for id numbers. So lanes wrote
`packs/<pack>/research/sources.fragment.json` inside their own
directory, and one writer deduplicated by URL and assigned the ids. One
writer, one namespace, no race.

That writer was not the integrator. `org/claims.json` gives
`registry/evidence.json` to the lane `L12-registry-estate`, and the
intent recorded on `org/tasks/T-0025.json` is to run the import. B1 says
hub artefacts are integrator-owned and never delegated, and ADR-0002's
third binding clarification names the integrator as the one that
deduplicates and imports; this run delegated the ledger whole to a
single lane instead. The property B1 exists for, one writer on the hub,
survived. The ownership rule it states did not, and reading this
example as compliance with B1 would be reading it wrong.

**Failure surface.** The checker is a single command that every lane
runs, and it reports per-file findings, so one lane's error does not
mask another's. Had it been pass or fail for the whole tree, D4 would
have required splitting it before dispatch.

## Step 3: the packets

Each lane received a closed packet with the nine fields from
`packs/agentic-swarm/refs/PACKET_AND_RETURN.md`. Two fields did the
most work here.

**The write set, literally.** "You may create or modify ONLY the paths
listed below. Writing anywhere else is a defect, not initiative. If
your work needs a change to a file you do not own, do not make it:
describe it in your handoff and the integrator applies it." That
sentence is what turns B1 from a diagram into a rule a lane can obey,
and it is why this pack's lane could not add its own row to
`registry/coverage.json` even though the row is obviously needed.

**The escape.** "If your packet does not determine something material,
do not guess and do not invent a plausible answer. Do the parts you
can, and list the undetermined thing in `blocked`. That is a
first-class outcome, not a failure." Named status, cheap, no penalty.

The packets also stated what would be seen and should be ignored:
findings about files the lane does not own, and forward references to
files other lanes had not yet written. Without that, twelve lanes would
each have tried to fix the same twelve dangling references.

## Step 4: the return

Schema-constrained, with five fields: what was done and why, every path
written, the judgement calls a reviewer should check, anything the
packet did not determine, and the handoff to the integrator. The
handoff field is the one that makes B1 survivable: it is where a lane
puts the change it needed and was not allowed to make.

## Step 5: merge

Claims committed before dispatch. The integrator merges in an order it
recorded, runs the checker after each lane rather than once at the end,
and regenerates every derived view itself. The fragment import comes
last, because it is the step that assigns the ids the pack bodies then
cite. On the record, that import belonged to L12 rather than to the
integrator, and either way it could only run once every fragment file
existed. This pack's own lane had closed by then, so its citations were
rewritten from fragment ids to the assigned evidence ids afterwards,
outside any lane, and its front-matter source list was left holding the
pre-import ids until a later review pass caught it.

## The departure from B7

B7 gates lane count on oracle strength: with a decidable external
oracle, wide fan-out is permitted; without one, cap at one or two lanes
and put a person at the merge gate. The checker is mechanical and covers
structure rather than argument, so it is not the oracle B7 means, and
twelve lanes is six times the cap. That is a departure from a binding
rule, and this file records it as one rather than dressing it as
compliance.

What was argued for it at dispatch: the artefacts are prose in disjoint
directories, and a wrong merge is cheap to see and cheap to revert. The
other half of B7's fallback did hold, because the merge gate in this
repository belongs to one operator, who is a person and
alone commits claims and adopts or discards what a lane returns
(`OPERATORS_GUIDE.md`). What the argument is not is a rule.
Reversibility appears in neither B7, nor check C11, nor the compiled
GRAPH_BUILD template, so no later run may cite this one as permission.
If cheap reversal is going to license width, it belongs in B7 as a
stated condition with something behind it. Until then this is a
departure the run took knowingly, and on code with the same oracle
twelve lanes would be too many.

## What this example does not show

A measured result. No single-agent control ran alongside it, so this run
cannot say whether it beat one session. That is the honest position, it
is the same position the pack's counter-evidence takes, and D14 exists
so the next one can do better.
