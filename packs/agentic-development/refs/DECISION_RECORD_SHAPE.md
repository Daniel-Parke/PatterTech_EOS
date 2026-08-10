---
summary: The six-section shape of a topology decision record, and what each section must contain
kind: recipe
scope: estate
sources: [EV-0051, EV-0079, EV-0109, EV-0111, EV-0121]
type: guide
tags: [eos, arch, tooling]
review: 2027-10
---

# Topology decision record shape

Asked for by B5, a default since the 2026-08 audit, whenever a design uses anything
above direct single-agent. One file, under 120 lines, front-matter with
`summary`, `type` and `tags` including `eos`. Six level-two sections,
in this order.

## Topology

Name the topology for each stage of the work, using the exact strings
from `packs/agentic-development/refs/TOPOLOGY_CARD.md`. One per stage,
not a list of candidates. Say what each stage does.

## Pressures

Name at least three of the eight pressures by name, and tie each one to
the choice it justified. Decomposability, shared-state coupling, oracle
quality, reversibility, latency, cost, context pressure, failure
localisation. A pressure named without a consequence is decoration
(EV-0109).

## Bounds

Numeric limits with units for at least two of turns, tokens and
wall-clock, plus the stop condition and what happens when it trips
(EV-0051).

## Resumability

Say whether state survives a restart, and how: checkpoint at a barrier
or event-log replay. State that resumed side effects are idempotent and
say what makes them so, because pre-interrupt code re-executes on
resume (EV-0079, EV-0121).

## Verification

Say what holds external truth for each output, and where nothing does,
say that plainly and do not claim an evaluator-optimizer loop for it
(EV-0111). Name the single writer for every shared artefact, using the
phrase single-writer.

## Approval

Name every irreversible or externally visible act and the human
approval that gates it, with the approval placed at the act rather than
at a phase boundary.

## Citing evidence

Cite the evidence ids that carried each choice, at least four, drawn
from `registry/evidence.json`. At least two must come from this pack's
own set, EV-0109 to EV-0121, because those are the rows that carry the
topology and verification claims. The shared estate rows most often
relevant alongside them are EV-0001, EV-0051, EV-0052, EV-0079,
EV-0084, EV-0088, EV-0106, EV-0107 and EV-0108. Cite ids, never
re-record sources.

## Voice

House voice law applies: plain spoken British English, no em-dashes, no
exclamation marks, no marketing register.
