---
summary: The product-discovery pack applied end to end to a feature request for an approvals inbox, ending in a TEST verdict
type: example
tags: [product, testing]
kind: example
scope: estate
---

# EX-DISC-001: The approvals inbox nobody asked for

A worked run of `packs/product-discovery/PACK.md` against one concrete
request, from the note landing to the record being written. Every rule
that fires is named where it fires.

## The situation

The commercial lead sends a note: "We keep losing deals on this. We need
an approvals inbox so managers can see everything waiting on them in one
place. Can we get it in this month?" No problem is stated. The note
names a solution and a deadline.

The venture is a small B2B tool. Available material: a support export of
240 tickets covering the last quarter, a metrics file recording 412
weekly active users, and a personas document with three named personas
and no interview notes behind any of them.

Activation: the task proposes new capability, so `proposes_capability`
is true, and it cites a claim about users, so `cites_user_claim` is
true. The pack loads.

## Step one, refuse the framing

B2 says the problem section may not name the requested feature. Writing
"users need an approvals inbox" would restate the solution and end the
investigation before it started. So the first question is what a person
cannot do today.

Reading the tickets by hand rather than by keyword: 19 of the 240
describe somebody waiting on a decision they could not see the state of,
and 4 mention an inbox or a queue by name. The gap between 19 and 4 is
the whole finding. The problem is about not knowing where a request sits
and who is holding it. An inbox is one answer to that and not the only
one.

Note the filter, per B5 and the evidence rules in
`packs/product-discovery/references/DISCOVERY_RECORD.md`: 19 is a count from a
read-and-classify pass, not from a search term. The record says so,
because a search-term count is a different claim.

## Step two, refuse the personas

The personas document has no interview provenance. B6 governs anything
about a population that did not come from a person. Two of the three
personas are plausible and none is evidenced, so they enter the record
labelled `unverified` and carry nothing. This is the rule that keeps a
model-shaped guess from becoming a segment decision, and the reason for
it is that on segment targeting, simulated respondents inflate
between-segment gaps and point teams at the wrong segment often enough
to be worse than useless (`EV-0413`).

## Step three, decide the depth

`packs/product-discovery/wargames/WG-DISC-001-discovery-depth.md`. The
change is reversible, no regulatory boundary is touched, and there are
412 weekly active users. That is far below the traffic needed to power a
test on a conversion-style metric inside a month, so option D, ship and
instrument, is refused as a measurement and kept as a signal read by
hand. Option A, a gated phase, is refused because the commitment is
reversible. The ruling is C then a hand-read signal.

## Step four, the risks, viability first

`EV-0416` and B4. Viability is written first because
it is the one a solo operator skips. The requested inbox needs a
permissions model, which is a support surface and a recurring cost. That
is the fact that changes the answer, and nothing in the original note
mentioned it.

## Step five, options, and the sequencing ruling

`packs/product-discovery/wargames/WG-DISC-003-choosing-between-opportunities.md`.
Three candidates: a status line on the existing request view, an email
digest of pending items, and the requested inbox. Ranked by
reversibility rather than by a score, the inbox goes last, because it is
the only one that forecloses the others by setting a permissions model
they do not need.

## The record

```
## Problem

People raising a request cannot see whether a decision has been made,
who is holding it, or how long it has sat there, so they chase by email
and the chase itself becomes the delay.

## Evidence

- support_export.csv, quarter to date: 240 tickets read and classified
  by hand; 19 describe waiting on a decision with no visible state.
  Filter: full read, not a keyword match.
- support_export.csv: 4 tickets name a queue or inbox directly.
- metrics.json: 412 weekly active users.
- personas.md: three personas, no interview notes, unverified, used for
  question wording only and carrying no part of this decision.

## Signal

- signal: repeat chase messages on a single request | threshold: fewer
  than half the rate of the quarter to date | source: support_export.csv
- signal: requests reaching a decision without any chase message |
  threshold: any sustained rise over four weeks | source:
  support_export.csv

## Risks

- value: 19 of 240 tickets describe the problem directly, which is real
  but narrow, and nobody has asked for a specific shape of answer.
- usability: a status line sits inside a view people already open, so
  there is nothing new to learn; the inbox would be a new place to go.
- feasibility: a status line is a field and a render, buildable in a
  day with no schema change.
- viability: the status line adds no permissions model, no new support
  surface and no recurring cost, and is reversible in an afternoon. The
  requested inbox adds all three, which is the reason it is not first.

## Options

- Status line on the existing request view. Buys the cheapest read of
  the problem. Costs: shows state, does not gather work.
- Email digest of pending items. Buys reach to people who do not log
  in. Costs: a sending schedule and an unsubscribe surface.
- Approvals inbox as requested. Buys a single place for a manager.
  Costs: a permissions model, and it forecloses the cheaper two.

## Decision

TEST

Ship the status line to the whole user base behind a flag and read the
chase rate by hand. The inbox is not refused, it is sequenced: it is
the only option that sets a permissions model, so it goes last and only
if the status line moves nothing.

- stopping rule: read the chase rate after four full weeks, once, and
  do not read it early. Rate down against the quarter to date, keep the
  status line and stop here. Rate flat, run the digest next. Rate up or
  ticket volume up, revert and reopen the problem.
- sample: 412
```

## What the pack changed

Without it, the month would have gone on an approvals inbox, a
permissions model and a support surface, on the strength of a note that
named a solution and four tickets that agreed with it. The three rules
that did the work were B2, which stopped the solution becoming the
problem statement, B4, which surfaced the recurring cost before the
build, and B6, which kept three invented personas out of the decision.

The verdict was TEST rather than BUILD, and the sample line is the
whole user base rather than an aspiration, because a sample larger than
the population is the clearest sign a record was written without reading
the numbers.
