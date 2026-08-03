---
summary: Adaptive testing law template, timing by change class, the test map, quality signals
type: template
tags: [eos]
template: true
---

# TESTING · The adaptive law

Tests exist to catch harm at the cheapest moment, so timing follows
the change class and the ruled tier. The router and the capability
profile may tighten any default here; nothing may loosen one below
this floor.

## Timing by change class

| Change | When tests land |
| --- | --- |
| Bug fix | Reproduce first with a failing test; the repro is kept forever |
| Invariants, money, security, public contracts | Executable acceptance authored independently before implementation, then frozen |
| Ordinary feature | Alongside implementation |
| Spike | Later, behind the hardening gate; a spike merges nothing |
| Refactor | Characterisation proportional to tier, pinned before the change |
| Docs | No behavioural tests by default; link resolution, executable snippet checks, schema validation and generated-doc drift checks still apply |
| Generated change | Verify the generator, not each output |

## The test map

In-loop verification runs the affected tests named by the queryable
test map, a derived artefact whose generator the stack profile names.
Every mapping row carries a confidence score built from generator
freshness, coverage of the touched paths and recent miss history. Low
or unknown confidence widens the run to the module's broader suite
and logs a finding; the map is never trusted blind. Full suites run
at integration and at release, by tier.

## Verification by mode

- Express: targeted checks only, the affected tests plus lint and
  types on the touched scope.
- Standard: affected tests via the map; sampled review.
- Exploration: checks may wait, inside the spike only; the hardening
  gate runs everything the ruling demands before anything merges.
- High-assurance: the frozen acceptance oracle, the full affected
  surface, independent review at acceptance.
- Parallel: per lane before merge, affected plus shared contract
  tests; rolling integration checks after each merge; the full suite
  at release.

## Quality signals

- Requirements coverage: acceptance criteria ids map to test ids,
  enforced at High-assurance.
- Mutation strength on protected modules, measured at hardening.
- Pass-to-pass regression rate across the suite.

Coverage percentage is never a universal gate. A project may ratchet
a specific number only with recorded evidence and a written reason,
and the ratchet is revisited at retro.

## Timing defaults

Neither test-first nor end-stage testing is mandated universally. The
capability profile carries the timing defaults, set by the EOS
test-timing ablation and kept conservative where its cells were
inconclusive; a mode dial of per-profile defers to those defaults.

## The floor

A failing check is never weakened, skipped or deleted to pass, in any
mode, at any tier. A check believed wrong is escalated through the
oracle amendment workflow or a question, with the reasoning on
record.

## Measured, 2026-08

The timing matrix above was a default set until the ablation ran. Eighteen
runs across three tasks, three timings, six runs each: every arm passed six
of six, so timing did not separate quality on this work. Cost did separate,
clearly. Implement-then-harden spent 3.8M tokens and 313 seconds against
2.3M and 208 seconds for alongside, and 2.4M and 217 seconds for
acceptance-first.

So the matrix stands as written, and the reason is now evidence rather than
assertion: acceptance-first where a gate depends on the oracle, alongside
for ordinary features, and harden-last kept for spikes where deferring the
oracle is the entire point. The sample is small and every arm passed, so
this ranks cost and says nothing about which timing catches more faults.
