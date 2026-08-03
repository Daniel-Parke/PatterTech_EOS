---
summary: How does context reach an agent, and what happens when the window runs out?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
sources: [EV-0080, EV-0083, EV-0085, EV-0086, EV-0106, EV-0113, EV-0114, EV-0117, EV-0121]
review: on-change-of:anthropic-context-engineering-publication
type: guide
tags: [eos, arch, tooling]
review_by: 2027-06
---

# GD-AGENT-002: How does context reach the agent?

## The question

Every agent run has a finite window and a job that may not fit in it.
Four strategies compete: load everything up front, fetch on demand,
compress what has happened, or write it down outside the window. They
have different failure modes, and the wrong one shows up as an agent
that forgets a decision it made an hour ago.

## It depends on

- **Context pressure**: does the whole job fit one window with room to
  reason, or not?
- **Run length**: minutes, or hours across several windows?
- **Retrieval cost**: is fetching a body cheap and reliable, or slow
  and flaky?
- **Reference stability**: will an identifier still resolve later?
- **Auditability**: does someone need to see what the agent knew?

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

## Default

B for the estate, D for continuity, C only as a shock absorber with the
opening events preserved. Recorded overrides are fine; silently relying
on compaction alone for a multi-window run is the anti-pattern.

## Worked rulings

- **PatterTech_EOS (2026-08, argued)**: the pack format itself is B.
  Level one is the first paragraph of the pack body, level two is the
  body, level three is `refs/`, fetched only when the decision needs
  it. Chosen because the estate will hold twenty packs and no run
  should pay for nineteen it does not touch.
- **PatterTech_EOS (2026-08, argued)**: D for lane continuity. Each
  pack lane writes its own files under its claimed path and the
  integrator reads them, rather than passing state through a shared
  conversation.

## Notes

Memory stores are configuration, not agent logic: one interface, a
retrieval limit and an explicit trimming policy (EV-0117). Tools are
part of context too, so consolidate them around workflows and namespace
them rather than exposing one per endpoint (EV-0113). A resumed run
rehydrates its context from the checkpoint, which is why the checkpoint
store is a trust boundary (EV-0121).
