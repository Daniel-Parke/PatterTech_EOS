---
id: GD-NAT-003
summary: How does a fix reach a user, given that no release can be taken back?
kind: wargame
type: wargame
tags: [ci, delivery, eos, ops, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-NAT-004, DOC-NAT-010]
applies_when: [distributes_via_app_store]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0026, EV-0204, EV-0372, EV-0373, EV-0374, EV-0375, EV-0376, EV-0377]
review: on-change-of:play-staged-rollout-mechanics
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-NAT-003: How does a fix reach a user?

## Decision question and stakes

On the web, a bad deploy is undone by deploying the previous one. On a
client, neither store can take a version back. Apple ramps automatic
updates on a fixed 1, 2, 5, 10, 20, 50 then 100 per cent schedule over
seven days, the percentages are not developer-selectable, the cohort is
not steerable, there is no automatic halt on a metric, and anyone can
fetch the new build manually at any moment (EV-0374). Play gives
the percentage dial and a halt button, but the halt only stops further
delivery: users who already took the update keep it, and the documented
remedy for a bad build is to ship a fixed one (EV-0375).

So the question is not how to roll back. It is which containment levers
you build into the binary before you need them.

## Doctrines or coverage gap under pressure

- `DOC-NAT-004` (binding): Release is forward-only.
- `DOC-NAT-010` (default): A one per cent first slice on Play with the halt trigger written down before the release starts, and phased release left on for Apple.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Blast radius of the worst plausible bug** in this release.
- **How fast a fixed build can clear review.** Roughly one submission
  in four was rejected in 2025, the largest bucket by a wide margin
  being Performance (EV-0373).
- **Whether the change is presentation or capability**, which decides
  whether the over-the-air path is even lawful (EV-0377,
  EV-0372).
- **Whether this is an update or a first launch.** Play's staged
  rollout applies to updates only, so a new app gets no gradual
  exposure at all.
- **Whether your telemetry can decide a halt** within the ramp window.

Applicability is `distributes_via_app_store`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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
without a store round trip (EV-0377). Buys a same-day fix for
the class of defect that is only presentation. Costs a fleet fragmented
by runtime version, a manifest you must prove cannot carry native code
or permissions, and a hard rule that it never changes capability
(EV-0372).

## Failure premises

### Premortem for A. Store release, nothing else

Assume `A. Store release, nothing else` was selected and the outcome failed. Test this option's stated failure mechanism first: the whole user base as the first cohort. Named here as the practice this pack rejects for anything with users.

### Premortem for B. Staged rollout with a halt trigger

Assume `B. Staged rollout with a halt trigger` was selected and the outcome failed. Test this option's stated failure mechanism first: a person watching a dashboard during the ramp, and it does not help the users who already updated.

### Premortem for C. B plus a kill switch in the binary

Assume `C. B plus a kill switch in the binary` was selected and the outcome failed. Test this option's stated failure mechanism first: flag hygiene, a retirement discipline, and the old path staying alive until the flag is removed.

### Premortem for D. C plus an over-the-air channel for presentation

Assume `D. C plus an over-the-air channel for presentation` was selected and the outcome failed. Test this option's stated failure mechanism first: a fleet fragmented by runtime version, a manifest you must prove cannot carry native code or permissions, and a hard rule that it never changes capability (EV-0372).

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

## Safe default

C. Staged rollout, halt trigger named in advance, and a kill switch for
every new behaviour, with the previous path still passing its tests
while the flag is off.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Blast radius of the worst plausible bug** in this release.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. Staged rollout, halt trigger named in advance, and a kill switch for every new behaviour, with the previous path still passing its tests while the flag is off.

**Exit condition:** Stop or roll back the selected branch when the whole user base as the first cohort. Named here as the practice this pack rejects for anything with users, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Blast radius of the worst plausible bug** in this release.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
