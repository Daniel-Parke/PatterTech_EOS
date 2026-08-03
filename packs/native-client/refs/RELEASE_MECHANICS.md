---
summary: Store release mechanics side by side, the over-the-air envelope, the kill-switch contract and the distribution clock
kind: fact
scope: estate
sources: [EV-0026, EV-0204]
volatility: fast
review: on-change-of:play-staged-rollout-mechanics
type: implementation
tags: [delivery, ops, ci]
review_by: 2027-08
---

# Release mechanics

Reference for PACK.md B4 and B5, and for GD-NAT-003. Mechanics as
documented by the two store operators at the 2026-08-03 cutoff, in our
own words. Both sources are living pages with no version stamp, so
re-read before relying on a detail.

## The two stores are not symmetric

| Property | Apple | Play |
| --- | --- | --- |
| Ramp shape | fixed 1, 2, 5, 10, 20, 50, 100 per cent over seven days | developer chooses each percentage |
| Who is in the cohort | users with automatic updates only | staged fraction of update-eligible users |
| Manual fetch during ramp | anyone can take the new build at any time | rollout fraction governs |
| Halt | pause allowed, up to thirty days total across any number of pauses | halt stops further delivery only |
| Metric-driven automatic halt | not documented, assume not | not described, trigger comes from your telemetry |
| Rollback | none, only a new version | none, documented remedy is a fixed bundle |
| First launch | phasing is for updates | staged rollout is for updates, a new app gets none |
| Scope narrowing mid-rollout | removing from sale ends phasing permanently for that version | country scope cannot be narrowed once started |

Two consequences. A cross-platform release runbook needs two sections,
because a single procedure cannot describe both. And neither ramp is
progressive delivery in the sense EV-0204 describes: there is no
analysis step and no automatic promotion or abort.

## The kill switch contract

The only containment lever that works after a user has updated.

- Every new behaviour ships behind a remotely evaluated flag
  (EV-0026), with the previous path present in the binary.
- The previous path keeps passing its tests while the flag is off. A
  flag that guards a path nobody tests is not a lever.
- The flag has a named owner and a removal date. Flags that outlive
  their release become permanent branches nobody understands.
- Flag evaluation must work when the sync path is blocked. A kill
  switch behind the stalled queue is not a kill switch.
- The runbook names the flag, the metric that trips it, and who may
  trip it. It contains no rollback step, because the step does not
  exist.

## The over-the-air envelope

Where an over-the-air channel exists, two lines matter and they are in
different places.

The technical line: the runtime can replace JavaScript, styling,
assets, copy and translations without a store round trip, and cannot
replace native code, native dependencies, permissions or SDK levels
(FRAG-NATIVE-08). Runtime version pinning is what makes it safe, and it
fragments the fleet by binary.

The review line, which is narrower: downloaded code may not introduce
or change features (FRAG-NATIVE-03). Rule 4.7 permits whole classes of
non-embedded software under conditions, which contradicts a naive
reading of the first rule, and the two are in visible tension. This
pack takes the narrower reading.

The check that makes the rule real: diff the over-the-air manifest
against the binary manifest on every publish, and fail on any
permission delta or native module delta. Neither vendor draws that line
for you.

## The distribution clock

Play raises the target API floor annually. At the cutoff: from 31
August 2026 new submissions and updates must target API 36, and an
existing app must target API 35 to stay visible to new users on current
devices, with an extension to 1 November 2026 available on request
(FRAG-NATIVE-07). Sideloaded and enterprise-private distribution is
exempt, and the consequence is reduced visibility rather than removal,
so an app with a stable installed base degrades slowly rather than
failing outright. Deadlines shift each year and differ for Wear, TV,
Automotive and XR.

Put the bump on the roadmap as fixed work, dated from the published
deadline, not from when someone notices.

## Calendar risk

Roughly one submission in four was rejected in the 2025 reporting year,
across 9,100,620 submissions, and the largest bucket by a wide margin
was Performance (FRAG-NATIVE-04). Plan one rejection cycle into every
release.

Scope this honestly. It is a vendor census of its own moderation
decisions, self-categorised, with no published method and no external
audit. Counts are submissions rather than distinct apps, so a
repeatedly resubmitted app inflates the number. The Performance bucket
mixes crashes, bugs, broken links and placeholder content and cannot be
decomposed into engineering actions. It sizes a calendar risk. It is
not a defect model, and it says nothing about Play.
