---
summary: What a reviewer or checker can verify about agent workflow design, split into executable today and judgement
kind: recipe
scope: estate
sources: [EV-0051, EV-0079, EV-0087, EV-0107, EV-0111, EV-0118, EV-0121]
type: guide
tags: [eos, arch, delivery]
review: 2027-10
---

# CHECKS: agentic development

Evaluation criteria for work in this domain. Each row says what is
checked, against which requirement, and whether a script can decide it
today or a person must.

## Executable today

These reduce to a regex, a parse or a count over the design record and
the code, and need no model in the loop.

| Id | Check | Against |
| --- | --- | --- |
| C1 | A topology above direct single-agent has a decision record with the six sections Topology, Pressures, Bounds, Resumability, Verification, Approval | B5 |
| C2 | The record names topologies using the canonical strings from the topology card | B5 |
| C3 | At least three of the eight pressure names appear in the Pressures section | B5 |
| C4 | Bounds gives numeric limits with units for at least two of turns, tokens, wall-clock | B2 |
| C5 | The string single-writer or one writer appears, and one owner is named per shared artefact | B1 |
| C6 | Resumability names checkpoint or event-log replay and asserts idempotent resumed side effects | B7 |
| C7 | Every irreversible or externally visible act named in the design appears in Approval | B3 |
| C8 | At least four evidence ids matching EV-nnnn are cited, at least two from EV-0109 to EV-0121, and every one resolves in `registry/evidence.json` | pack law |
| C9 | Record is under 120 lines, carries front-matter with summary, type and tags including eos, and passes the voice checks | house law |
| C10 | Loop implementations pass a bound to the runner, and child budgets are counted against the run total rather than set per child | B2 |
| C11 | Tracing is configured with the seven span names, a workflow name and a group id | B6 |
| C12 | Where an evaluator-optimizer loop is claimed, the evaluator is a distinct process or context from the generator | B4 |

C1 to C9 are exactly the shape the frozen acceptance drill in
`benchmark/drills/agentic-development.md` asserts, so a pack change
that breaks them breaks the drill.

## Judgement, for a reviewer

These need a person, and saying so is more honest than pretending a
script can decide them.

- **Is the named pressure real?** C3 checks that a pressure is named,
  not that it is present. A reviewer asks whether decomposability
  actually holds or whether the subtasks share an assumption.
- **Is the oracle any good?** A schema validator that accepts almost
  anything satisfies C12 and verifies nothing (EV-0111).
- **Is this the simplest topology that works?** The single most
  valuable review question, and the one no checker answers.
- **Are the bounds sane?** C4 sees the numbers, not whether 5 million
  tokens is proportionate to the outcome.
- **Does the approval sit at the risky act?** C7 sees that an approval
  exists. Whether it sits at the act or at a tidy phase boundary is a
  reading of the design (EV-0079).
- **Is harness scaffolding still earning its place?** Every component
  should name the model limitation it compensates for, and that claim
  expires as models improve.

## Suite level

Beyond a single design, an agent workflow that ships repeatedly carries
an evaluation suite: twenty to fifty tasks harvested from real
failures, scored with pass@k and pass^k because the system is
non-deterministic (EV-0087). A single green run is not evidence. Suite
existence is executable; suite quality is judgement.

## Not checked here

Prompt wording, model choice, inference cost tuning and sandbox
security posture. The first three are out of scope for this pack, and
the last belongs to the security-privacy pack.
