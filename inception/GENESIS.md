---
summary: The Genesis phase, run in the venture repo after the seed gate, and the development blueprint it produces
type: kernel
tags: [eos]
sources: [EV-0007, EV-0178]
---

# GENESIS

Genesis is one phase. It runs once, in the new venture's repository,
after the seed gate, and it turns a signed seed into a development
blueprint: bounded research, a product map, work packages, and an
acceptance spine that starts red. ADR-0006 authorises it.

The word meant something else in v1, a standing playbook called PB-001
that a venture's own organisation ran to produce its design set. That is
history, at the archive/v1-final tag, so a live file saying Genesis and
meaning a standing playbook is stale prose. Two things came forward from
PB-001 because they earned it: the scale grading, and the acceptance
walk-through written as a failing suite that goes green journey by
journey.

Genesis is a compiled hand-off. Its forms ship in the seed, the phase
runs in the venture's own tree, and the EOS does not run inside the
venture afterwards. No standing service, and no EOS session owed a
report.

## When it runs, and who decides

Straight after phase E of inception/INCEPTION.md: the rubric is signed,
the auto checks are green, the venture's row is in registry/PROJECTS.md.
The operator then either launches Genesis or writes one line in the
sign-off block saying why not. It is a launch decision rather than a
gate. A venture may build with no blueprint; the cost is that the first
lanes settle the architecture one file at a time, privately.

The phase sits after the gate, so it works under the venture's own
rules, branches included. Session 0's write-to-main exemption ended at
sign-off.

## Inputs

The signed seed with its lock-book rulings, the venture's policy file,
and docs/VENTURE_BRIEF.md, whose list of material workstreams is what
packets and packages get cut from. A brief with no workstream list
blocks Genesis rather than shortening it.

## The four outputs, and where they live

Each output has a form already in the seed, blank, at both scales. A
venture that declined Genesis at the gate can run it later without a
recompile.

| output | form in the seed | where the filled work lands |
| --- | --- | --- |
| Research packets | docs/genesis/RESEARCH_PACKET.md | docs/research/RP-NN.md, one per packet |
| The product map | docs/PRODUCT_MAP.md | the same file, filled in place |
| Work packages | docs/genesis/WORK_PACKAGE.md | docs/packages/WP-NN.md, one per package |
| The acceptance spine | docs/ACCEPTANCE_SPINE.md | the same file, filled in place |

A fifth form ships beside them, docs/genesis/LENS.md: the contract for
studying something the venture did not build, agreed before the source
is read. It is the form PB-E11 of org/PLAYBOOKS.md runs on here.
Research that means reading someone else's product or repository is a
study, and the contract is what makes it defensible afterwards. The
venture copies it to docs/lenses/LENS-NNNN.md, one per study.

## Scale

The grading is in the forms themselves. Each one was pruned for the
ruled scale when the seed compiled, so an S venture holds the S variant
and never has to work out what to leave out. What S drops on top of
that is volume rather than artefacts.

- At most one research packet, and none is a common answer.
- A product map of about a page.
- One work package per material workstream.
- The acceptance spine, still a suite that starts red. What the S form
  drops is the mutation run, not the suite.

ORG runs the full form and that is its default. Express skips Genesis
unless the operator asks for the lite form.

## The run, in order

1. Cut the research packets from the workstreams: at most one each, and
   only where a decision is waiting on one.
2. Integrate the product map, in one session, however wide the packets
   ran.
3. Settle the cross-cutting decisions on the map, and mark as settled
   every section a package may be cut from.
4. Cut the work packages from the settled map.
5. Author the acceptance spine from the map's conditions, by a session
   that will not implement against it. It can be written alongside step
   4; what matters is that it is finished before any build lane opens.
6. Put the map and the packages to the operator.

Steps 1 and 4 can fan out. Steps 2, 3 and 5 are one session each: the
map is integrated by one session by construction, and the spine is
authored by a session that will not implement against it. The method
for running wide is packs/agentic-swarm, whose executable half an ORG
seed carries as org/GRAPH_BUILD.md, and that pack's budget and stop
rules govern the run. At S there is nothing to fan and the phase is one
session throughout.

## Output 1 · Research packets

One packet per material workstream at most. A packet holds sourced facts
and decisions, not a survey of a subject. Four bounds hold it, and each
one prevents research that runs until somebody gets bored.

- **Stopping condition.** A packet stops when it is decision-complete
  for the packages that will cite it: every decision a builder would
  otherwise take differently is pinned. It does not stop when the
  subject is exhausted, because subjects are not.
- **Evidence sufficiency.** A claim a package will rely on carries a
  source and the date it was read, or it is written as an open decision
  with an owner instead of a finding. Nothing gets inferred to make the
  packet look finished.
- **Hard cap.** 150 lines. Reaching it without meeting the stopping
  condition is a finding: say what is still open and hand it to the
  operator. A packet that genuinely needs more is two workstreams, so
  split it and say so on the map.
- **Changes nothing, says so.** Research that changes no decision writes
  one line saying exactly that and stops. Where the packet is not worth
  keeping, that line goes on the map instead; lose it and the next
  session asks the same question from the start.

## Output 2 · The product map

One file, integrated by one session even when the packets were written
wide. It carries the domain model; the components and what contains
them; the contract between each pair that talks; the dependency graph;
the integration points with anything outside; the acceptance conditions
for each journey; the risks; and the open decisions with an owner and a
date on each.

Every section carries a lifecycle marker, and the form says what the
three mean. Only a settled section may have a package cut from it. A
lane that finds reality disagreeing with a settled section flips it back
to draft and records the disagreement on its package, when it finds it
rather than at some later review. An ignored map is worse than no map,
because it still gets cited.

Cross-cutting decisions are settled here, before any lane diverges, and
recorded where the form's table says: a venture ADR at ORG, a lock-book
ruling or a task row at S. A decision two lanes each take privately is a
merge conflict with a schedule attached.

## Output 3 · Work packages

One per unit of work, cut from the settled map. The form lists what a
package states. Two of those are rulings rather than headings, and they
are the reason the form exists.

File ownership is disjoint by construction rather than by discipline.
Where the run fans out, hub files, the ones many packages touch, stay
with the integrator and are never delegated. Concurrent agent work on
shared files conflicts often enough that discipline is not a control.

Acceptance conditions are copied from the map and never written from
code that does not exist yet. A package does not get to reword a
condition; the map changes first.

## Output 4 · The acceptance spine

The journey walk-through from the map, encoded as an executable suite
that runs and fails on the day it is written and then goes green one
journey at a time.

The ordering is not the point and never was (EV-0178). Authoring it
early is simply the cheapest way to get an oracle the implementer did
not write, and that is the part that holds: tests generated after faulty
code detect roughly half the faults that independently generated tests
catch, because the code and its tests agree with each other (EV-0007).
The spine also gives the venture an honest progress signal, journeys
green out of journeys total, rather than a percentage of a plan.

## The end

Genesis ends when the operator reads the map and the packages and says
go. That is the one human gate in the phase, and it is held by the same
person who already decides whether the build starts. If they will not say
go, whatever stopped them goes on the map as an open decision with their
name against it, and Genesis is not finished.
