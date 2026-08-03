---
summary: Should this work be a subagent at all, and if so as a tool, a handoff or a peer worker?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
sources: [EV-0084, EV-0086, EV-0106, EV-0107, EV-0108, EV-0109, EV-0112, EV-0116]
review: on-change-of:agent-sdk-major-release
type: guide
tags: [eos, arch, tooling]
review_by: 2027-06
---

# GD-AGENT-003: Should this be a subagent at all?

## The question

Delegation is the most over-used move in agent design. It looks like
modularity and behaves like distributed systems. This guide is the gate
before the topology guide: it asks whether a second agent should exist,
and if so what relationship it has to the first.

## It depends on

- **Context pressure**: is the parent's window the actual constraint?
- **Decomposability**: is the subtask genuinely separable?
- **Shared-state coupling**: will the child write anything the parent
  also writes?
- **Return shape**: can the child's result be condensed to something
  small and typed, or must the parent see everything the child saw?
- **Cost**: is the outcome worth the coordination overhead, which
  vendor practice puts at roughly an order of magnitude in tokens for
  breadth-first work (EV-0112)?
- **Failure localisation**: if the child fails, will you know?

## Options

### A. No subagent
The parent does it inline. Buys full context, one trace, no
coordination failure modes, and it is right far more often than it
looks. Costs window space in the parent.

### B. Subagent as a tool
The parent calls a specialist for a bounded subtask and keeps the
conversation and the writes. Buys a condensed return that protects the
parent's window (EV-0084, EV-0086). Costs a hop, and the child cannot
see the parent's reasoning.

### C. Handoff
Routing is the workflow: the specialist takes over and owns what
follows. Buys clean separation where the decision really is which
specialist. Costs continuity, since the parent is no longer driving
(EV-0116).

### D. Peer workers under an orchestrator
Several agents work at once under a lead that holds the plan. Buys
wall-clock and coverage on read-mostly, separable work. Costs the token
multiple, duplicated work, over-spawning, and the coordination failures
that dominate multi-agent traces (EV-0112, EV-0109).

## Decision rule

Do not spawn to be tidy. Spawn only when one of these holds.

If the subtask would flood the parent's window and its result condenses
to something small, B. If routing itself is the decision and the
specialist owns the rest of the task, C. If subtasks are separable,
read-mostly and coverage or wall-clock is worth the token multiple, D,
with exactly one writer at the join and a shared budget across
children. Otherwise A.

Two constraints apply to every spawn. Children read, one owner writes
(EV-0107). Every child inherits a bound: turns, tokens or wall-clock,
counted against the run, not per child, or over-spawning follows
(EV-0112).

## Default

A. The burden of proof is on the spawn, and the reason goes in the
topology decision record.

## Worked rulings

- **PatterTech_EOS (2026-08, argued)**: D for the pack build, because
  eight domains are genuinely separable and each research pass would
  otherwise flood one window. Writes to shared registries were removed
  from the children entirely by path claims, which is B1 satisfied by
  construction rather than by care.
- **PatterTech_EOS (2026-08, inherited)**: A for checker changes. The
  work fits one window and has a test oracle, so no spawn was argued.

## Notes

Cognition's public position moved from do not build multi-agents
(EV-0106) to writes single-threaded while other agents contribute
intelligence (EV-0107). Read the reversal as the field converging on
the writer constraint rather than on a headcount. Agent-team features
in vendor harnesses make spawning cheap to type and no cheaper to run
(EV-0108).
