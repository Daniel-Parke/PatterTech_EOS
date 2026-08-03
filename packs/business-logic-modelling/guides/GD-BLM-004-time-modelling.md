---
summary: How much time does this fact carry, which temporal type and how many dimensions?
kind: guide
authority: binding
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0275, EV-0281, EV-0282]
review: on-change-of:RFC-9557
type: guide
tags: [data, arch, product]
review_by: 2027-11
---

# GD-BLM-004: How much time does this fact carry?

## The question

Two forks sit on top of each other. Which temporal type holds this
fact, and how many time dimensions the domain needs. Getting the first
wrong produces bugs twice a year; getting the second wrong produces a
question you cannot answer at all, or a model every reader has to
understand.

## It depends on

- **Whether the fact has a zone at all.** A birthday does not. A
  meeting does. A log line has an instant and nothing else.
- **Whether the value will be compared or advanced.** Storage is easy,
  arithmetic is where zones matter (EV-0281).
- **Whether the rule is wall-clock or elapsed.** "Thirty minutes from
  now" and "9am tomorrow" behave differently when the clocks change,
  and the domain has to say which it means.
- **Whether facts get corrected after the event.** If yes, somebody
  will eventually ask what we believed at the time (EV-0275).
- **Whether the future time can be moved by a political decision.** A
  future local time is not a fixed instant, because a government can
  change the offset.

## Options

### A. One instant, stored in UTC
A single point on the timeline, no zone attached. Buys simplicity and
correct ordering. Costs every calendar question: it cannot tell you
what day it was for the customer, and it cannot advance by a day across
a clock change.

### B. The narrowest type that holds the fact
At least seven distinct temporal types exist: instant, zoned
date-time, plain date, wall-clock time, date-time with no zone,
year-month, month-day, plus durations (EV-0282). Choose the narrowest
one that holds the fact. Buys the impossibility of silently inventing a
zero, a zone or a UTC assumption for a value that is genuinely unknown.
Costs a vocabulary the team has to learn.

### C. B, plus a zone identifier wherever arithmetic happens
A zoned value carries the identifier, not the offset, because an offset
is a number while an identifier is a function from instants to offsets
(EV-0281). Buys a right answer for "one day later" and for expiry
across a daylight-saving change. Costs a current time-zone database in
every runtime that does the arithmetic.

### D. C, plus a second time dimension
Record when the fact was true and when the system came to believe it,
with an escalation ordered by cost: audit log, effectivity dating,
temporal property, fully versioned object (EV-0275). Buys answers to
correction, dispute and reprocessing questions. Costs complication for
every reader of the model, which the source concedes.

## Decision rule

C for anything compared or advanced, which binds as B2 in PACK.md. B
for everything else, and B is not optional either: choosing a wide type
is how the assumption gets made silently. Move to D only when somebody
has already asked a two-dimensional question and the answer was not
available, and when you do, take valid time and transaction time
together or neither.

State whether a duration is wall-clock or elapsed at the point it is
declared. A thirty-minute hold is elapsed time and survives a clock
change unchanged; a 9am reminder is wall-clock and moves with the zone.
Both are legitimate and the domain has to choose.

## Default

B plus C, one time dimension, and durations declared as elapsed unless
the rule is explicitly a wall-clock rule. Serialise with the zone
identifier attached rather than the offset alone (EV-0281). Never store
a naive local datetime in a domain that touches more than one zone, and
never store an offset where a zone was meant.

## Worked rulings

- **The hold that expires across a clock change (estate, argued)**: a
  thirty-minute hold created at 01:40 in Europe/London on the morning
  the clocks go back is still held twenty wall-clock minutes later and
  expired after forty. Elapsed time, zoned value, arithmetic on the
  instant. A naive datetime gets this wrong in the direction of
  expiring things early.
- **Renewal date (2026-08, argued)**: a monthly renewal is a calendar
  operation in the customer's zone, not an addition of thirty days to
  an instant, so the renewal instant is computed by adding one month in
  the zone and then resolving to an instant. See
  `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`.
- **Birthday is a plain date (estate, argued)**: no zone, no time, no
  midnight. Storing it as a timestamp is how somebody's birthday lands
  on the wrong day for half the world.

## Counter-evidence

The serialisation standard covers the wire format, not storage or
arithmetic, and it is only as good as the time-zone database revision
each runtime carries (EV-0281). It explicitly does not cover future
local times whose offset a government may change, so a far-future
appointment is stored as a local time plus a zone and resolved late.
The type taxonomy comes from a language proposal whose stage was not
verified at access, so it is cited as a modelling idea rather than as a
shipped API (EV-0282). The two-dimension source is twenty-one years old
and gives no rule for when the second dimension is worth its cost,
which is the decision that actually matters (EV-0275).
