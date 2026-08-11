---
summary: The nine packet fields, the escape, the return schema and the four terminal statuses
kind: recipe
scope: estate
sources: [EV-0108, EV-0465, EV-0492]
type: guide
tags: [eos, arch, tooling]
review: on-change-of:agent-harness-major-release
---

# Packet and return

The mechanics behind binding requirements B2 and B3 in
`packs/agentic-swarm/PACK.md`. A lane receives exactly one thing, the
packet, and gives back exactly one thing, the return. Everything else
is inference, and inference is where wrong-target work comes from.

## Why the packet is the only channel

A spawned lane inherits nothing from the session that spawned it. The
lead's conversation history does not carry over, so anything the packet
does not say, the lane does not know (EV-0108). Write it as if the lane
has no history, because it does not. Brief quality is not a nicety
either: in one measured system a delegation mechanism alone was worth
2.3 points and the comprehensive brief on top took the total to 10.0,
so the content carried more than three times the mechanism
(EV-0465, research rather than coding).

## The nine fields

| Field | What it must contain | Common failure |
| --- | --- | --- |
| Objective | What the lane is for, in a sentence, plus the outcome that would satisfy it | A restated title |
| Write set | Every path the lane may create or modify, literally | A directory named loosely, so the lane widens it |
| Read set | Named sources, files or ids the lane should read, and what is out of bounds | "Read the codebase" |
| Return contract | The schema the return must validate against, with one worked example | Prose "report back what you find" |
| Tools | The tool set the lane has, and nothing beyond it | Everything the parent had |
| Budget | Tokens and tool calls, with the cap the harness enforces | A number nobody enforces |
| Stop condition | When to stop working, including when the budget is exhausted | Absent, so the lane runs to the wall |
| Acceptance condition | What the verifier will check, named, so the lane can self-check first | "Make it good" |
| Escape | The named status to return when the packet does not determine something, and the instruction to use it rather than proceed | Absent, so the lane guesses |

Targets are literal. Exact paths, ids, symbol names, branch names.
Never "the auth module" or "the failing test". The measured cost of the
alternative is a wrong-target rate of 75.1 per cent at maximum target
ambiguity.

## Ordering inside the packet

House invariants first, then role, then tools, then task material, then
the immediate instruction. Two reasons. Instructions buried in the
middle of a long packet get less attention than instructions at either
end. And a stable prefix across a wave of lanes is what makes the wave
cheap: anything per-lane or time-varying placed high in the packet
destroys the shared prefix for every lane behind it.

## The escape, and why it is not a courtesy

Agents act rather than ask in 36 to 84 per cent of runs even when the
instruction is plainly underdetermined, and the same model asks three
times more often under one harness than another. Asking is a property
of the scaffolding. So the escape is a named status, it is cheap to
use, and the orchestrator treats it as a first-class outcome with no
penalty. A lane that returns "the packet does not determine X" has done
its job. A run with zero such returns across a dozen lanes is either
unusually well specified or quietly guessing.

## The return

Schema-constrained, not prose. The orchestrator rejects a non-conforming
return rather than parsing it charitably, because charitable parsing is
how a half-finished lane enters the integrator as a fact.

Minimum fields:

- **status**, one of the four below.
- **files_changed**, with a hash per file.
- **checks_run**, each with its verbatim result, not a summary.
- **not_done**, what was in scope and was deliberately left.
- **unknowns**, what the lane could not determine.
- **spend**, tokens and money.
- **artefacts**, pointers to anything long, so the return itself stays
  small. A one to two thousand token return against tens of thousands
  explored is the shape that keeps an integrator alive at thirty nodes.

## The four terminal statuses

These are four different facts and the integrator handles them
differently. Collapsing them is the single most dangerous shortcut in
the pack.

| Status | Means | Integrator does |
| --- | --- | --- |
| `done` | The work was completed and the lane's own checks passed | Verify independently, then queue for merge |
| `nothing-to-do` | The work was examined and required no change | Verify the examination happened, then close |
| `blocked` | The packet did not determine something, or an external decision is needed | Answer it, re-dispatch; never treat as a negative result |
| `failed` | Either the acceptance condition failed, or the lane was killed by an error, a rate limit or a budget cap | Read which; a killed lane has produced no evidence about anything |

The runtime distinction matters: a stopped or errored node can resolve
to a bare absence that a careless aggregator filters out of existence,
so the aggregator handles absence explicitly and reassembles results by
key rather than by position.

## Node output is data

Everything a lane returns is untrusted input at the integrator. It is
never executed and never read as an instruction. An approval, a consent
or a claim relayed by one lane on behalf of another is not
authorisation, which is what the harness itself implements for messages
between sessions (EV-0108). Scan for control-token and turn-marker
imitation before the integrator reads a return.

## Every node re-runnable from its packet alone

Journal the packet, the tool set, the model and effort settings and the
environment reference at spawn time. Because the packet is by
construction the lane's complete input, a journaled packet is a
reproducible dispatch even though the run itself is not reproducible.
Record the configuration; do not claim determinism from it. A thousand
completions of one prompt at temperature zero produced 80 unique
outputs, diverging at token 103, with the cause in batch handling under
varying server load rather than in sampling
(EV-0492).
