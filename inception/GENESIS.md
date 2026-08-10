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

The word used to mean something else here. v1 carried a playbook,
PB-001, that a venture's own organisation ran to produce its design set;
it is history, at the archive/v1-final tag. Genesis now means this phase
and nothing else, so a live file that says Genesis and means a standing
playbook is stale prose. Two things came forward from PB-001 because
they earned it: the scale grading, and the acceptance walk-through
written as a failing suite that goes green journey by journey.

Genesis is a compiled hand-off. Its templates ship in the seed, the
phase runs in the venture's own tree, and the EOS does not run inside
the venture afterwards. No standing service, and no EOS session owed a
report.

## When it runs, and who decides

Straight after phase E of inception/INCEPTION.md: the rubric is signed,
the auto checks are green, the venture's row is in registry/PROJECTS.md.
The operator then either launches Genesis or writes one line in the
sign-off block saying why not. It is a launch decision rather than a
gate. A venture may build with no blueprint; the cost is that the first
lanes settle the architecture one file at a time, privately.

## Scale

Full form at ORG, and that is the ORG default. At S the lite form is the
default: at most one research packet, a one-page product map, a build
plan in place of separate work packages, and the acceptance spine as a
written checklist rather than a suite. Express skips Genesis unless the
operator asks for the lite form.

Four templates under kernel/templates compile into the seed at both
scales, because an S venture that rescales must not need a second
compile to get them: RESEARCH_PACKET, PRODUCT_MAP, WORK_PACKAGE and
ACCEPTANCE_SPINE.

## Inputs

The signed seed with its lock-book rulings, the venture's policy file,
and docs/VENTURE_BRIEF.md, whose risk surface names the venture's
material workstreams. That list is what packets and packages get cut
from, so a brief with no workstream list blocks Genesis rather than
shortening it.

## Output 1 · Research packets

One packet per material workstream at most, in docs/research/RP-NN.md.
A packet holds sourced facts and decisions, not a survey of a subject.
Four bounds hold it, and each one prevents research that runs until
somebody gets bored.

- **Stopping condition.** A packet stops when it is decision-complete
  for the packages that will cite it: every decision a builder would
  otherwise take differently is pinned. It does not stop when the
  subject is exhausted, because subjects are not.
- **Evidence sufficiency.** A claim a package will rely on carries a
  source and the date it was read, or it is written as an open decision
  with an owner instead of a finding. Nothing gets inferred to make the
  packet look finished.
- **Hard cap.** 150 lines a packet, the guide cap. A packet that needs
  more is two workstreams: split it, and say so on the map.
- **Changes nothing, says so.** Research that changes no decision writes
  one line saying exactly that and stops. The line survives even where
  the packet does not; lose it and the next session asks the same
  question from the start.

## Output 2 · The product map

docs/PRODUCT_MAP.md, one file, integrated by one session even when the
packets were written wide. It carries the domain model; the components
and what contains them; the contract between each pair that talks; the
dependency graph; the integration points with anything outside; the
acceptance conditions for each journey; the risks; and the open decisions
with an owner and a date on each.

Every section carries one lifecycle marker: draft, settled or stale.
Settled means a package may be cut from it. A lane that finds reality
disagreeing with a settled section flips it back to draft and records
the disagreement on its package, when it finds it rather than at some
later review. Stale means the build has moved past the section, so fix
it or delete it. An ignored map is worse than no map, because it still
gets cited.

Cross-cutting decisions are settled here, before any lane diverges, and
recorded as venture ADRs. A decision two lanes each take privately is a
merge conflict with a schedule attached.

## Output 3 · Work packages

docs/packages/WP-NN.md, one per unit of work, cut from the settled map.
Each states the objective; the interface contract it consumes and the one
it publishes; its file ownership boundary; its context packet, meaning
the exact files to read under a stated line budget; its acceptance
conditions, written from the map and never from code that does not exist
yet; the packages it depends on; what done means; and the suggested
execution mode.

File ownership is disjoint by construction rather than by discipline, and
hub files, the ones many packages touch, stay with the integrator and are
never delegated. Concurrent agent work on shared files conflicts often
enough that discipline is not a control.

## Output 4 · The acceptance spine

docs/ACCEPTANCE_SPINE.md, the journey walk-through from the map, encoded
as an executable suite that runs and fails on the day it is written and
then goes green one journey at a time. It is authored before any build
lane opens, by a session that will not implement against it.

The ordering is not the point and never was (EV-0178). Authoring it early
is simply the cheapest way to get an oracle the implementer did not
write, and that is the part that holds: tests generated after faulty code
detect roughly half the faults that independently generated tests catch,
because the code and its tests agree with each other (EV-0007). The spine
also gives the venture an honest progress signal, journeys green out of
journeys total, rather than a percentage of a plan.

## Running it

Genesis sits after the gate, so it works under the venture's own rules,
branches included. Session 0's write-to-main exemption ended at sign-off.

Genesis is itself run wide: packets fan out, one session integrates the
map, packages get cut from the settled map. Every run declares a budget
in turns, tokens and wall clock, and stops on two of the three rather
than on somebody's judgement in the moment. The method is the
packs/agentic-swarm pack, whose executable half an ORG seed carries as
org/GRAPH_BUILD.md.

## The end

Genesis ends when the operator reads the map and the packages and says
go. That is the one human gate in the phase, and it is held by the same
person who already decides whether the build starts. If they will not say
go, whatever stopped them goes on the map as an open decision with their
name against it, and Genesis is not finished.
