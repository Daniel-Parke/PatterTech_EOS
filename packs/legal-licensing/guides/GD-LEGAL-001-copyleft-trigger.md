---
summary: Can we use this copyleft dependency for what we actually ship, and what fires the obligation
type: guide
tags: [security, delivery]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0340, EV-0341, EV-0342, EV-0338]
review: on-change-of:https://opensource.org/license/agpl-v3
---

# GD-LEGAL-001: Does this copyleft dependency's obligation actually fire?

## The question

A dependency carries a reciprocal licence. The fork is not whether the
licence is acceptable in the abstract. It is which event the obligation
attaches to, and whether this venture performs that event.

## It depends on

- Does anything leave the building? A source release, a package, a
  binary, a container image handed to someone else.
- Do people reach the software over a network instead?
- Is the component modified, or used as it came?
- Is it linked into our program, or run as a separate process behind an
  interface?
- Is it a build-time or test-time tool that never reaches the artefact?

## Options

### A. Treat distribution as the trigger

The mature published policy sorts licences into freely includable,
includable under conditions, and never, reasoning throughout about
source and binary releases (EV-0342). Buys: a standing
verdict anyone can apply without judgement, and a defensible line for
anything shipped as an artefact. Costs: it says nothing about a hosted
service, because nothing is distributed, so on our most common shape
the whole framework returns no answer.

### B. Treat network interaction as the trigger

Section 13 of the network copyleft licence attaches the obligation to a
modified version that users reach remotely, with no distribution needed
(EV-0341). Buys: it catches the one term most likely to
bite a venture selling a hosted product. Costs: it turns on what counts
as modification and where the program boundary sits, and the licence
text resolves neither.

### C. Treat combination as the trigger

Compatibility means merging the code and still complying with every
licence at once, and it is directional: lax licences absorb into
anything, reciprocal licences are mutually incompatible unless one
carries an explicit provision (EV-0340). Buys: the
right frame when the question is whether two licences can sit in one
program. Costs: it addresses combination of source into one program and
does not settle where a program boundary lies for a service, an image
or a plug-in.

### D. Avoid the question by substitution

Replace the component. Buys: no obligation, no decision record, no
lawyer. Costs: a real engineering cost, sometimes a worse component,
and it becomes a reflex that quietly bans good software.

## Decision rule

- Build-time or test-time only, nothing reaching the artefact: A, and
  the answer is almost always yes. Record it and move on.
- Something leaves the venture as an artefact: A first, then C for
  whether it can sit in the same program as our own licence.
- Nothing leaves and people reach it over a network: B. A is silent
  here, and treating its silence as permission is the failure this
  guide exists to prevent.
- Modified, network-reachable, and the boundary is arguable: stop. This
  is escalation trigger one under B7 in `packs/legal-licensing/PACK.md`.
  Do not reason your way to a boundary.
- The cost of substitution is lower than the cost of the decision
  record: D, and say so plainly in the record.

## Default

A for anything shipped, B for anything hosted, and the venture writes
down which shape it is before the first reciprocal dependency arrives
rather than during the argument about one.

## Evidence boundary

The three-bucket policy is tuned to one distributor's promise that
everything it releases stays permissively licensed
(EV-0342). Its categories are that promise, not the
law, and the page carries no revision date. The compatibility position
is one advocacy organisation's doctrine, stated rather than tested in
court (EV-0340). The network trigger is licence text,
which is the strongest source here, and it is still silent on the two
questions people actually ask (EV-0341). Read narrowly,
an unmodified component run as a back end triggers nothing extra, which
is why some teams use these licences freely and others ban them. The
disagreement is about the modification boundary rather than the text.

Whatever the answer, it is recorded as one identifier and never as a
raw choice expression (EV-0338).

## Worked rulings

- **PatterTech EOS legal-licensing pack (2026-08, argued)**: A for
  artefacts and B for hosted products, with the modification boundary
  routed to a lawyer rather than ruled. Argued from
  EV-0341 against EV-0342, where the
  dominant industry policy and the term most likely to bite point at
  different events.
- **PatterTech EOS itself (2026-08, inherited)**: A. This repository is
  documentation and tooling, published as an artefact, nothing hosted.
