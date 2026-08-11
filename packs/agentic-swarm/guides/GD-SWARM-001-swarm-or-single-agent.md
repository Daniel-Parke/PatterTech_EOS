---
summary: Should this work be fanned out over lanes at all, or given to one agent?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
sources: [EV-0010, EV-0053, EV-0107, EV-0112, EV-0479]
review: on-change-of:agent-harness-major-release
type: guide
tags: [eos, arch, delivery]
---

# GD-SWARM-001: swarm, or one agent?

## The question

Fan-out costs roughly an order of magnitude more tokens than one
session and buys coverage, not correctness. The fork is whether this
particular job is one a graph helps with. Getting it wrong is the most
expensive mistake in the pack, because the loss is invisible: the work
looks done, it cost seven to fifteen times as much, and it is worse.

## It depends on

- **Decomposability.** Can the work be cut so that lanes do not need
  each other's intermediate results? This, not difficulty, is what
  separated a domain that gained 80.9 per cent from one that lost 70.0
  per cent at almost identical complexity.
- **Oracle strength.** Is there something decidable outside the lanes
  that says right or wrong? Fan-out multiplies coverage and does
  nothing for selection, so whatever picks the winner is the ceiling on
  the whole run: coverage scaled log-linearly to 56 per cent at 250
  samples where one sample got 15.9, and without an automatic verifier
  voting and reward models plateau (EV-0479).
- **Single-agent baseline.** How often does one agent already succeed?
  Above roughly 45 per cent, adding agents predicts a loss.
- **Value of the work.** The token multiple has to be worth paying, and
  the vendor that reports the largest uplift says so in the same
  breath (EV-0112).
- **Hub density.** How many artefacts would more than one lane want to
  write? Every one of those is either integrator-owned or a conflict.

## Options

### A. One agent, one session
The default. Buys shared context, no merge gate, no coordination
overhead, and it is the arm that beats most multi-agent systems on a
normalised benchmark suite. Costs wall-clock time, and degrades on work
that overflows one context window.

### B. One writer, several readers
One session writes; other agents research, review or answer questions
without touching the tree. Buys extra intelligence with no merge
surface. This is the shape a practitioner who publicly argued against
multi-agent systems settled on ten months later (EV-0107). Costs the
extra tokens, and nothing else.

### C. Fan-out over a measured graph, one integrator
The pack's governing shape. Buys real parallelism and independent
contexts, which is the only known defence against one lane's errors
poisoning another's reasoning. Costs a partition artefact, a claim set,
an integrator, and a merge gate that becomes the constraint.

### D. Wide fan-out, ten lanes or more
Only against a decidable external oracle. Buys throughput on work that
can be checked automatically per unit. Sixteen lanes produced a working
compiler this way, with a conformance suite and a reference
implementation in place before the agents started (EV-0053). Costs
everything C costs, at a scale where a weak oracle becomes a disaster
rather than a nuisance.

## Decision rule

Start at A. Move to B when the job needs judgement one session cannot
hold, not when it needs speed. Move to C only when all four hold: the
dependency graph cuts into groups with low coupling, the hub artefacts
can be held back, an external verifier exists or can be written before
the lanes start, and the single-agent baseline is not already high.
Move to D only when the oracle is decidable per unit, and record the
reason. If the graph will not cut, or the work is a chain, run A and
say so on the record. That is a decision, not a failure.

## Default

Three to five lanes when C is chosen. This is a converging heuristic
from three independent directions, not a measured optimum, and the pack
says so in its counter-evidence.

## Worked rulings

- **PatterTech_EOS, 2026-08-10, argued.** C at about a dozen lanes for
  the v2.1 documentation build. The artefacts cut cleanly by pack and
  by kernel file, the derived views were held back to the integrator,
  and the verifier, `python -m tools.eos check --repo`, predates every
  lane by months. The oracle is mechanical but partial: it checks
  structure, references and voice, not whether an argument is any good,
  which is why review stayed human at the gate. Worked example in
  `packs/agentic-swarm/exemplars/EX-SWARM-001-eos-v2-1-partition.md`.
- **Any single pack edit, inherited.** A. One file, one owner, no graph.

## Notes

Felt speed is not evidence. One randomised trial measured developers 19
per cent slower with agent tooling while they believed they had been 20
per cent faster (EV-0010). Whatever this fork decides, the run gets
instrumented, or the next decision is made on a feeling again.
