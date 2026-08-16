---
id: WG-AGENT-002
summary: How does context reach an agent, and what happens when the window runs out?
kind: wargame
type: wargame
tags: [arch, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AGENT-010, DOC-AGENT-012]
applies_when: [builds_agent_workflow]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0080, EV-0083, EV-0085, EV-0086, EV-0106, EV-0113, EV-0114, EV-0117, EV-0121]
review: on-change-of:anthropic-context-engineering-publication
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-AGENT-002: How does context reach the agent?

## Decision question and stakes

Every agent run has a finite window and a job that may not fit in it.
Four strategies compete: load everything up front, fetch on demand,
compress what has happened, or write it down outside the window. They
have different failure modes, and the wrong one shows up as an agent
that forgets a decision it made an hour ago.

## Doctrines or coverage gap under pressure

- `DOC-AGENT-010` (default): Context arrives just in time, by progressive disclosure.
- `DOC-AGENT-012` (default): Continuity across context windows rides on artifacts and git history, not on compaction alone.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Context pressure**: does the whole job fit one window with room to
  reason, or not?
- **Run length**: minutes, or hours across several windows?
- **Retrieval cost**: is fetching a body cheap and reliable, or slow
  and flaky?
- **Reference stability**: will an identifier still resolve later?
- **Auditability**: does someone need to see what the agent knew?

Applicability is `builds_agent_workflow`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Pre-load everything
Put the whole corpus, tool catalogue and history in the prompt. Buys
simplicity and no retrieval failure mode. Costs the window: a large
tool estate alone consumed about 150,000 tokens in one worked vendor
example (EV-0114). Poor for anything long.

### B. Just-in-time retrieval with progressive disclosure
Load identifiers, summaries and a map; fetch bodies only when needed.
Buys a window that stays mostly free, and it scales with the estate
rather than against it. The same worked example fell to roughly 2,000
tokens (EV-0114, EV-0086). Costs a retrieval path that can fail, and
the agent must know what exists to ask for it (EV-0083).

### C. Compaction or condensing
Summarise older turns when a threshold is crossed, always preserving
the opening events. Buys a run that continues past the window. Costs
detail, and the detail lost is often the decision you need later
(EV-0080, EV-0117).

### D. External artifacts plus version history
The agent writes progress, decisions and state to files, and reads
them back. Buys durable, inspectable continuity across any number of
windows, and a human-readable audit trail. Costs discipline and an
extra write step (EV-0085).

## Failure premises

### Premortem for A. Pre-load everything

Assume `A. Pre-load everything` was selected and the outcome failed. Test this option's stated failure mechanism first: the window: a large tool estate alone consumed about 150,000 tokens in one worked vendor example (EV-0114). Poor for anything long.

### Premortem for B. Just-in-time retrieval with progressive disclosure

Assume `B. Just-in-time retrieval with progressive disclosure` was selected and the outcome failed. Test this option's stated failure mechanism first: a retrieval path that can fail, and the agent must know what exists to ask for it (EV-0083).

### Premortem for C. Compaction or condensing

Assume `C. Compaction or condensing` was selected and the outcome failed. Test this option's stated failure mechanism first: detail, and the detail lost is often the decision you need later (EV-0080, EV-0117).

### Premortem for D. External artifacts plus version history

Assume `D. External artifacts plus version history` was selected and the outcome failed. Test this option's stated failure mechanism first: discipline and an extra write step (EV-0085).

## Decision rule

If the job fits one window with headroom, A is fine and cheapest to
build. If the tool or document estate is large, B for the estate
regardless of run length. If the run spans several windows, D is the
carrier of continuity and C is at most a shock absorber inside it. If
several agents run at once, each holds only what it needs and the
shared truth lives in D, because fragmented context is how parallel
work produces work that does not compose (EV-0106). If anyone must
later audit what the agent knew, D, because a condenser leaves no
record of what it dropped.

## Safe default

B for the estate, D for continuity, C only as a shock absorber with the
opening events preserved. Recorded overrides are fine; silently relying
on compaction alone for a multi-window run is the anti-pattern.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Context pressure**: does the whole job fit one window with room to reason, or not?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B for the estate, D for continuity, C only as a shock absorber with the opening events preserved. Recorded overrides are fine; silently relying on compaction alone for a multi-window run is the anti-pattern.

**Exit condition:** Stop or roll back the selected branch when the window: a large tool estate alone consumed about 150,000 tokens in one worked vendor example (EV-0114). Poor for anything long, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Context pressure**: does the whole job fit one window with room to reason, or not?

## Counter-evidence and transfer limits

### Preserved reasoning: Notes

Memory stores are configuration, not agent logic: one interface, a
retrieval limit and an explicit trimming policy (EV-0117). Tools are
part of context too, so consolidate them around workflows and namespace
them rather than exposing one per endpoint (EV-0113). A resumed run
rehydrates its context from the checkpoint, which is why the checkpoint
store is a trust boundary (EV-0121).
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
