---
summary: The field set that makes an aggregate boundary reviewable, what each field is diagnostic of, and the questions that decide a boundary
kind: fact
scope: estate
sources: [EV-0098, EV-0099, EV-0100, EV-0157, EV-0269, EV-0270, EV-0286]
volatility: slow
review: on-change-of:aggregate-design-canvas-major
type: implementation
tags: [arch, data, product]
---

# Boundary write-up

Reference for PACK.md D2 and for GD-BLM-001 option C. The field set
below is adapted from a CC-BY-4.0 workshop canvas (EV-0270) and
paraphrased rather than reproduced.

## When a boundary is even in question

Only when you can write one sentence of the form "X and Y must never be
observed inconsistent". If the sentence needs an "ideally" or a
"usually", it is not an invariant and it does not justify a boundary
(EV-0269). Most rules in most venture software fail this test, and
that is the expected outcome.

## The fields

Write these down before writing code. A boundary that cannot be
written down has not been decided.

| Field | What it records |
| --- | --- |
| Name | what the cluster is called in the domain's own words |
| Enforced invariants | the statements that must never be observed false |
| Corrective policies | what happens when something outside is found inconsistent |
| Handled commands | what a caller may ask this boundary to do |
| Created events | what the boundary announces to the world |
| State transitions | which statuses follow which |
| Throughput | expected concurrent writes and contention |
| Size | how many rows or child entities, and how it grows |

## What each field is diagnostic of

- **No enforced invariant.** There is no boundary. Split it or drop it.
- **A long list of corrective policies.** Logic that belongs inside the
  boundary has leaked into compensating handlers (EV-0270). Move the
  rule in, or accept that the boundary is drawn in the wrong place.
- **High throughput and large size together.** Every write contends
  with every other. This is the god aggregate, the failure the source
  names as most common (EV-0269).
- **Unbounded growth in size.** The cluster will not load or archive
  cleanly. Reference by identity instead.
- **State transitions that nobody can enumerate.** The lifecycle is
  implicit, which is what D3 in PACK.md refuses.

The throughput and size prompts assume an event-emitting store, so for
a plainly state-stored cluster they are estimates rather than measured
figures (EV-0270).

## The rules that follow

1. Modify one aggregate per transaction. Everything else in the same
   operation is reconciled afterwards (EV-0269).
2. Reference other aggregates by identity, never by holding the object.
3. Everything outside the boundary is eventually consistent, and the
   change record says what may be stale and for how long.
4. Any state change with an outbound message goes through the outbox,
   and every consumer is idempotent (EV-0157). This is B4 in PACK.md
   and it is what makes rule 3 honest.

## Boundaries are provisional

The same source that gives these rules spends its third part on first
designs being wrong and superseded through discovery (EV-0269). A
boundary is revisited when the invariant changes. It is not defended
because it is written down, and the write-up is dated so the next
reader knows what it was reacting to.

## Related discovery aids

Bounded context canvas, context mapping and the starter modelling
process (EV-0098, EV-0099, EV-0100) are preferences in this pack, not
requirements. Their own maintainers warn against institutionalising the
process, and the strongest review of the method reports onboarding cost
and scarce expertise as recurring problems (EV-0286). Use them as
thinking aids and drop them without ceremony.
