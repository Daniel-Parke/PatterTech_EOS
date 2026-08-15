---
id: GD-AGENT-003
summary: Should this work be a subagent at all, and if so as a tool, a handoff or a peer worker?
kind: wargame
type: wargame
tags: [arch, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-AGENT-001]
applies_when: [builds_agent_workflow]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0084, EV-0086, EV-0106, EV-0107, EV-0108, EV-0109, EV-0112, EV-0116]
review: on-change-of:agent-sdk-major-release
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-AGENT-003: Should this be a subagent at all?

## Decision question and stakes

Delegation is the most over-used move in agent design. It looks like
modularity and behaves like distributed systems. This guide is the gate
before the topology guide: it asks whether a second agent should exist,
and if so what relationship it has to the first.

## Doctrines or coverage gap under pressure

- `DOC-AGENT-001` (binding): One writer.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `builds_agent_workflow`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. No subagent

Assume `A. No subagent` was selected and the outcome failed. Test this option's stated failure mechanism first: window space in the parent.

### Premortem for B. Subagent as a tool

Assume `B. Subagent as a tool` was selected and the outcome failed. Test this option's stated failure mechanism first: a hop, and the child cannot see the parent's reasoning.

### Premortem for C. Handoff

Assume `C. Handoff` was selected and the outcome failed. Test this option's stated failure mechanism first: continuity, since the parent is no longer driving (EV-0116).

### Premortem for D. Peer workers under an orchestrator

Assume `D. Peer workers under an orchestrator` was selected and the outcome failed. Test this option's stated failure mechanism first: the token multiple, duplicated work, over-spawning, and the coordination failures that dominate multi-agent traces (EV-0112, EV-0109).

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

## Safe default

A. The burden of proof is on the spawn, and the reason goes in the
topology decision record.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Context pressure**: is the parent's window the actual constraint?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. The burden of proof is on the spawn, and the reason goes in the topology decision record.

**Exit condition:** Stop or roll back the selected branch when window space in the parent, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Context pressure**: is the parent's window the actual constraint?

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

Cognition's public position moved from do not build multi-agents
(EV-0106) to writes single-threaded while other agents contribute
intelligence (EV-0107). Read the reversal as the field converging on
the writer constraint rather than on a headcount. Agent-team features
in vendor harnesses make spawning cheap to type and no cheaper to run
(EV-0108).
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
