---
summary: Fifteen risks a graph build carries, with mechanism, evidence, detection signal and control
kind: recipe
scope: estate
sources: [EV-0010, EV-0013, EV-0107, EV-0108, EV-0112, EV-0219, EV-0244, EV-0473, EV-0474, EV-0475, EV-0476]
type: guide
tags: [eos, security, arch, ops]
review: on-change-of:agent-harness-major-release
---

# Risk register: graph builds

Fifteen rows. Each names the mechanism, the evidence, the signal that
detects it, and the rule in `packs/agentic-swarm/PACK.md` that controls
it. A risk with no detection signal is a hope, so every row has one.

## Outcome and cost

**R1. Fan-out underperforms one strong agent.** Coordination cost
exceeds the parallelism gain. On a normalised ten-benchmark substrate,
five of six multi-agent systems scored below a single-agent baseline
and the sixth was inside the uncertainty band, while the six as a group
spent 24 to 286 per cent more tokens. Single agents also match or beat
multi-agent systems under equal thinking budgets. *Detect*: the swarm
loses to a single-agent control on the same task. *Control*: D1, D2,
D3, D14.

**R2. Cost outruns value.** Multi-agent runs use roughly fifteen times
chat tokens and scale with lane count, and loops without a terminator
do not stop (EV-0112). *Detect*: spend per merged change against the
control. *Control*: B6, D14.

**R3. Runaway recursion and unbounded fan-out.** Nesting defaults move
between releases and concurrency ceilings have documented bypasses.
*Detect*: live agent count above the declared ceiling. *Control*: B6,
with depth set explicitly rather than inherited.

## Correctness

**R4. Semantic conflict that compiles.** Lanes hold partial, isolated
context; changes correct in isolation contradict when composed. *Detect*:
green build, failing integration behaviour. *Control*: B1 hub
isolation, seam review, integrator-owned cross-lane behaviour.

**R5. Agreement mistaken for confirmation.** Independently generated
implementations co-failed 429 times against 115.36 predicted under
independence, concentrated on the specification's ambiguous clauses.
*Detect*: a merge criterion that reads "all three lanes agree".
*Control*: B8.

**R6. The oracle was written by the thing it judges.** Generating tests
with the buggy implementation in context produced 104 effective tests
against 304 from the correct implementation. Models under evaluation
have also patched their own test configuration. *Detect*: verifier
timestamp after lane dispatch, or a test path inside a lane's write
set. *Control*: B7, checks C9 and C10.

**R7. Integrator context rot.** The single synthesis point holds the
longest context in the system and accumulates every lane's output. One
model family dropped 30 to 45 per cent as irrelevant context grew from
about 300 to about 113,000 tokens (EV-0244). *Detect*: integrator
quality falling as lane count rises. *Control*: bounded pointer-based
returns, D13, periodic re-grounding on external truth rather than on
lane summaries.

**R8. Constraint loss through compaction.** Violations were zero with
the policy visible and averaged 30 per cent after compaction, reaching
59 per cent for some model families. *Detect*: a lane breaking a rule
its packet contained at dispatch. *Control*: B5.

## Security

**R9. Injection replicating lane to lane.** Malicious prompts
self-replicate across connected agents and the systems stay vulnerable
even when agents limit what they share. *Detect*: instruction-shaped
text crossing a lane boundary. *Control*: B4, plus message screening at
the boundary.

**R10. The lethal trifecta assembling across the graph.** No single lane
holds private data, untrusted content and egress, and the transitive
closure of the message graph does (EV-0219). The trifecta is Willison's
framing; evaluating it over the closure rather than per agent is this
pack's inference. *Detect*: reachability analysis over the message
graph. *Control*: evaluate per run, not per lane. The constructive
answer is the structural patterns that make injection unable to change
the action set at all, of which plan-then-execute and map-reduce map
directly onto graph fan-out (EV-0473).

**R11. Privilege inheritance and the confused deputy.** Teammates start
with the lead's permission settings including a permission-skipping
flag, and per-teammate modes cannot be set at spawn (EV-0108).
Protocol guidance is normative that a server must not accept a token
not issued for it, because passthrough breaks the audit trail and turns
the server into an exfiltration proxy (EV-0474).
*Detect*: a lane holding authority wider than its packet declares.
*Control*: credentials issued per lane, scoped and short-lived, never
inherited; teardown revokes them.

**R12. The checkpoint store as an execution surface.** Deserialisation
reconstructs arbitrary callables, so write access to the store is code
execution in the application runtime (EV-0475), and injection in the
metadata filter supplies that write access, which removes the need for
any prior hold on the store (EV-0476).
This is distinct from the neighbour pack's checkpoint-trust rule: that
governs believing a checkpoint's contents, this governs the store as a
place code runs. *Detect*: user-controlled filters reaching state
history, or a pickle fallback enabled. *Control*: no deserialisation
that can reconstruct callables, parameterised queries, write access
treated as privileged.

**R13. Hallucinated dependencies entering the trunk.** Commercial models
emit non-existent package names at 5.2 per cent or more, open-source at
21.7 per cent, over 576,000 samples. N lanes is N chances, and an
integrator merging lock files without re-resolving gives the bad name
its authority. *Detect*: any name that does not resolve before merge.
*Control*: B10.

## Operations

**R14. Non-idempotent effects executed N times, and orphans left
behind.** Retries and losing speculative branches externalise anyway
unless fenced; a commit gate gave about seven times the task success of
immediate-effect baselines under fault injection and leaked nothing
where the comparators leaked over a thousand messages. Separately,
sessions and credentials outlive runs. *Detect*: duplicate external
records; live agents or valid tokens with no owning run. *Control*:
D11, plus a teardown step that stops every worker and revokes every
issued credential, with the run incomplete until it passes.

**R15. The run cannot be traced across the delegation chain.** Tracing
itself is B6 of `packs/agentic-development/PACK.md`, a default since the
2026-08 authority audit, so a run that skips it says so in writing.
What a graph adds is that the standard span vocabulary defines agent
identity and token usage but no parent node, no graph edge a node
satisfies and no granted write set, so the harness carries those
itself, and every document in that convention is marked Development
status (EV-0013). *Detect*: you cannot answer which lane
told this node to act, and whether it was allowed to. *Control*: one
run id and one span per node, delegation attributes added locally, and
the convention version recorded so a rename is visible.

## The meta-risk

**Scaffolding rot.** Every rule here compensates for something a model
currently cannot do, and those assumptions expire. The clearest public
instance is a practitioner arguing against multi-agent systems in 2025
and publishing three working patterns ten months later (EV-0107).
*Detect*: a rule whose stated failure can no longer be reproduced.
*Control*: every rule in this pack names its failure precisely, no
vendor number or model name appears in pack prose, and the review
trigger is a harness release rather than a date. When the failure stops
happening, the rule goes, and that is a success rather than an
embarrassment.

## What this register does not cover

Perceived speed. It is not a risk, it is a measurement error, and it is
large: one randomised trial found developers 19 per cent slower while
believing they were 20 per cent faster (EV-0010). It belongs in D14,
not here.
