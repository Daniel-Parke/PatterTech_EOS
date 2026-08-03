---
summary: The written severity ladder, the tie-break, the mode-changing band, the three-factor declaration score and the objective triggers
kind: fact
scope: estate
sources: [EV-0200, EV-0211]
volatility: slow
review: 2027-08
type: implementation
tags: [ops, delivery]
---

# Severity ladder and declaration

Reference for PACK.md B2 and D6, and for
`packs/support-operations/guides/GD-SUPPORT-003-declaration-route.md`.
The ladder is written before an incident, kept in the repository, and
read during one.

## What a ladder must contain

- Three or more ordered bands, most urgent first, each with a written
  impact criterion a stranger could apply.
- The tie-break, stated in the ladder itself: when the call is unclear,
  take the higher band.
- At least one named band that changes the response mode, not only the
  wording. The mode change is what makes the label a decision rather
  than a report field.
- A statement that the band is not argued during the incident and that
  the argument belongs in the postmortem.

## A three-band starting ladder

| Band | Impact criterion | What changes |
| --- | --- | --- |
| S1 | a core path is unusable, or data or money is at risk, for people outside the venture | mode change: declare, open a communication channel, stop other work, comms owner named separately from fix owner |
| S2 | a core path is degraded, or an ancillary path is unusable, for people outside the venture | respond now, tell affected customers, no stop-work |
| S3 | visible to few, workaround exists, or ancillary and cosmetic | normal queue, no declaration |

Five bands become worth writing once there is a rota (PACK.md D2).
Until then the extra rungs are five ways to write the same sentence.

## The three-factor declaration score

Customer-facing declaration is scored, not felt. Score three factors
and write the combining rule before the incident
(FRAG-SUPPORT-OPERATIONS-02):

1. **Visibility.** Core service or an ancillary one.
2. **Actual impact now.** At the current traffic level, not the
   potential impact at peak.
3. **Duration so far and confidence.** How long it has run, and
   whether resolution within the hour is likely.

A worked combining rule: declare when visibility is core and actual
impact is present, or when duration has passed twenty minutes with low
confidence at any visibility. Ventures may write a different rule; they
may not leave it unwritten.

## Objective declaration triggers

Independently of the score, declare when any of these holds
(FRAG-SUPPORT-OPERATIONS-03):

- A second person is needed.
- The failure is visible to people outside the venture.
- An hour of focused work has not closed it.

Scope note: the one-hour trigger comes from a very large service estate
and is a starting number to argue with, not evidence for any threshold
here.

## The incident record

Fields recorded, all of them, at the times they become true:

`severity` (a band defined in the ladder), `declared_at`,
`declared_by`, `comms_owner`, `fix_owner`, `customers_affected`,
`resolved_at`, `postmortem_due`.

`comms_owner` and `fix_owner` are separate fields and both are filled
even when the values are the same name (PACK.md B3). `postmortem_due`
is set at resolution, no more than five days after `resolved_at`, with
a named owner (PACK.md D9, EV-0200).

## Duration reporting

Incident durations are reported as raw figures or at stated
percentiles. No band carries a time target and no report carries an
average of a duration: the distribution is positively skewed, and the
corpus that looked found no correlation between duration and severity
(EV-0211, PACK.md B5).
