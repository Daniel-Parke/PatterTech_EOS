---
summary: How does a fix reach a user, given that no release can be taken back?
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0026, EV-0204]
review: on-change-of:play-staged-rollout-mechanics
type: guide
tags: [delivery, ops, ci]
review_by: 2028-05
---

# GD-NAT-003: How does a fix reach a user?

## The question

On the web, a bad deploy is undone by deploying the previous one. On a
client, neither store can take a version back. Apple ramps automatic
updates on a fixed 1, 2, 5, 10, 20, 50 then 100 per cent schedule over
seven days, the percentages are not developer-selectable, the cohort is
not steerable, there is no automatic halt on a metric, and anyone can
fetch the new build manually at any moment (FRAG-NATIVE-05). Play gives
the percentage dial and a halt button, but the halt only stops further
delivery: users who already took the update keep it, and the documented
remedy for a bad build is to ship a fixed one (FRAG-NATIVE-06).

So the question is not how to roll back. It is which containment levers
you build into the binary before you need them.

## It depends on

- **Blast radius of the worst plausible bug** in this release.
- **How fast a fixed build can clear review.** Roughly one submission
  in four was rejected in 2025, the largest bucket by a wide margin
  being Performance (FRAG-NATIVE-04).
- **Whether the change is presentation or capability**, which decides
  whether the over-the-air path is even lawful (FRAG-NATIVE-08,
  FRAG-NATIVE-03).
- **Whether this is an update or a first launch.** Play's staged
  rollout applies to updates only, so a new app gets no gradual
  exposure at all.
- **Whether your telemetry can decide a halt** within the ramp window.

## Options

### A. Store release, nothing else
Submit, ship at 100 per cent, fix forward. Buys simplicity. Costs the
whole user base as the first cohort. Named here as the practice this
pack rejects for anything with users.

### B. Staged rollout with a halt trigger
Small first slice on Play, phased release left on for Apple, and a halt
trigger written down against a named metric before the release starts.
Buys a bounded first cohort on one store and a weakly bounded one on
the other. Costs a person watching a dashboard during the ramp, and it
does not help the users who already updated.

### C. B plus a kill switch in the binary
Every new behaviour ships behind a remotely evaluated flag with the old
path still present and still tested (EV-0026). Buys the only real
rollback a client has: turn the behaviour off for everyone in minutes,
including for users who already updated. Costs flag hygiene, a
retirement discipline, and the old path staying alive until the flag
is removed.

### D. C plus an over-the-air channel for presentation
Adds an update channel that ships copy, styling, assets and layout
without a store round trip (FRAG-NATIVE-08). Buys a same-day fix for
the class of defect that is only presentation. Costs a fleet fragmented
by runtime version, a manifest you must prove cannot carry native code
or permissions, and a hard rule that it never changes capability
(FRAG-NATIVE-03).

## Decision rule

Take C for anything with users. Take D on top only where the
architecture already supports it and a presentation-only defect class
is a real cost, and only with the manifest check in
`packs/native-client/CHECKS.md` in place. Never rely on the store ramp
as your containment lever: Apple's is not progressive delivery in the
sense EV-0204 describes, because there is no analysis step and no
automatic halt. Write the runbook with no rollback step in it, because
the step does not exist.

The two stores are not symmetric, so one cross-platform runbook needs
two release sections. Country scope on Play cannot be narrowed once a
rollout starts, and removing an app from sale on Apple terminates
phasing permanently for that version.

## Default

C. Staged rollout, halt trigger named in advance, and a kill switch for
every new behaviour, with the previous path still passing its tests
while the flag is off.

## Worked rulings

- **native-client pack exemplar (2026-08, argued)**: C, with the
  booking reservation path behind a flag and a release document
  containing no rollback wording. See
  `packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`.
- **The calendar ruling (2026-08, argued)**: every release plan carries
  one rejection cycle by default (FRAG-NATIVE-04). Scope note: that is
  Apple's self-reported census of its own decisions, counting
  submissions rather than apps, with no published method. It sizes a
  calendar risk and nothing else.
- **The distribution clock (external, inherited)**: the annual target
  API deadline (FRAG-NATIVE-07) is a release-train obligation, not
  upkeep. An app that stops shipping goes invisible to new users on
  current devices rather than failing outright, so the decay is quiet.
