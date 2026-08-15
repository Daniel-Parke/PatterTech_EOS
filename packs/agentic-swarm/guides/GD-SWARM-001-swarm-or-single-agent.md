---
id: GD-SWARM-001
summary: Should this work be fanned out over lanes at all, or given to one agent?
kind: wargame
type: wargame
tags: [arch, delivery, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AGENT-008, DOC-SWARM-012, DOC-SWARM-013, DOC-SWARM-024]
applies_when: [fans_work_across_lanes]
engages_when: [agent_coordination_cost_is_material]
consequence: routine
relations: [DREL-AGENT-001]
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0010, EV-0053, EV-0107, EV-0112, EV-0479, EV-0452]
review: on-change-of:agent-harness-major-release
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SWARM-001: swarm, or one agent?

## Decision question and stakes

Fan-out costs roughly an order of magnitude more tokens than one
session and buys coverage, not correctness. The fork is whether this
particular job is one a graph helps with. Getting it wrong is the most
expensive mistake in the pack, because the loss is invisible: the work
looks done, it cost seven to fifteen times as much, and it is worse.

## Doctrines or coverage gap under pressure

- `DOC-AGENT-008` (default): Start at direct single-agent with a strong oracle.
- `DOC-SWARM-012` (default): Do not swarm work a single agent already does well.
- `DOC-SWARM-013` (default): If the graph will not cut, do not swarm.
- `DOC-SWARM-024` (default): Run a single-agent control on a sample, and instrument the landing.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `fans_work_across_lanes`. Engagement is `agent_coordination_cost_is_material`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. One agent, one session

Assume `A. One agent, one session` was selected and the outcome failed. Test this option's stated failure mechanism first: wall-clock time, and degrades on work that overflows one context window.

### Premortem for B. One writer, several readers

Assume `B. One writer, several readers` was selected and the outcome failed. Test this option's stated failure mechanism first: the extra tokens, and nothing else.

### Premortem for C. Fan-out over a measured graph, one integrator

Assume `C. Fan-out over a measured graph, one integrator` was selected and the outcome failed. Test this option's stated failure mechanism first: a partition artefact, a claim set, an integrator, and a merge gate that becomes the constraint.

### Premortem for D. Wide fan-out, ten lanes or more

Assume `D. Wide fan-out, ten lanes or more` was selected and the outcome failed. Test this option's stated failure mechanism first: everything C costs, at a scale where a weak oracle becomes a disaster rather than a nuisance.

## Decision rule

Start at A. Move to B when the job needs judgement one session cannot
hold, not when it needs speed. Move to C only when all four hold: the
dependency graph cuts into groups with low coupling, the hub artefacts
can be held back, an external verifier exists or can be written before
the lanes start, and the single-agent baseline is not already high.
Move to D only when the oracle is decidable per unit, and record the
reason. If the graph will not cut, or the work is a chain, run A and
say so on the record. That is a decision, not a failure.

## Safe default

Three to five lanes when C is chosen. This is a converging heuristic
from three independent directions, not a measured optimum, and the pack
says so in its counter-evidence.

## Cheapest discriminating test

Compare one bounded single-agent baseline with the smallest justified lane split under the same task set, model budget and external verifier. Include merge and verification time in the result.

## Fallback, exit and revisit

**Fallback `safe-default`:** Three to five lanes when C is chosen. This is a converging heuristic from three independent directions, not a measured optimum, and the pack says so in its counter-evidence.

**Exit condition:** Stop or roll back the selected branch when wall-clock time, and degrades on work that overflows one context window, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Decomposability.** Can the work be cut so that lanes do not need each other's intermediate results? This, not difficulty, is what separated a domain that gained 80.9 per cent from one that lost 70.0 per cent at almost identical complexity.

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

Felt speed is not evidence. One randomised trial measured developers 19
per cent slower with agent tooling while they believed they had been 20
per cent faster (EV-0010). Whatever this fork decides, the run gets
instrumented, or the next decision is made on a feeling again.
### Current research boundary

EV-0452 reports gains on decomposable work and losses on sequential, tool-heavy work. Transfer the direction only: coordination cost, baseline capability and central verification still need measurement on this task.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
