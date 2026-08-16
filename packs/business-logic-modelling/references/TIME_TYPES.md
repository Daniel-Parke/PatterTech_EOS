---
summary: The temporal type table, zone against offset, elapsed against wall-clock rules, and the two-dimension escalation
kind: fact
scope: estate
sources: [EV-0275, EV-0281, EV-0282]
volatility: slow
review: on-change-of:RFC-9557
type: implementation
tags: [data, arch, tooling]
---

# Time types

Reference for PACK.md B2, D4 and D5, and for WG-BLM-004.

## The type table

At least seven distinct temporal kinds exist, and conflating them is
where date bugs come from (EV-0282). Choose the narrowest that holds
the fact.

| Kind | Holds | Typical fact |
| --- | --- | --- |
| Instant | a point on the timeline | when a row was written |
| Zoned date-time | an instant plus the zone it was expressed in | a booking, a deadline, an expiry |
| Plain date | a calendar date, no time, no zone | a birthday, an invoice date |
| Wall-clock time | a time of day, no date, no zone | an opening time, a daily cutoff |
| Local date-time | date and time, no zone | a template for a recurring event |
| Year-month | a month in a year | a billing period, a card expiry |
| Duration | an amount of time | a hold length, a retention window |

A wide type silently invents a zero, a UTC assumption or the local zone
for a value that is genuinely unknown. That is the whole argument for
the table.

## Zone against offset

An offset is a single number. A zone identifier such as Europe/London
is a function from instants to offsets, and only the second answers
what one day later means across a daylight-saving change (EV-0281). So:

- Store the zone identifier wherever the value will be compared or
  advanced. Storing the offset alone is correct for ten months of the
  year.
- Serialise with the zone identifier attached, alongside the instant
  and the offset. The serialisation standard also marks each suffix
  critical or elective, so a reader knows which it must understand
  (EV-0281).
- A trailing Z means the UTC offset is known and the local offset is
  not. That is a different fact from "this value is in UTC" and it
  should not be treated as a zone.
- A far-future local time is stored as a local date-time plus a zone
  and resolved to an instant late, because a government can change the
  offset between now and then. The standard says it does not cover this
  case (EV-0281).
- Every runtime doing zone arithmetic carries a time-zone database, and
  the answers are only as good as its revision.

## Elapsed against wall-clock

Declare which one a rule means at the point the rule is written:

- **Elapsed.** "Thirty minutes from now" is arithmetic on the instant.
  A clock change does not affect it. A hold created at 01:40 in
  Europe/London on the morning the clocks go back is still held at
  02:00 wall-clock, twenty minutes later, and expired forty minutes
  later, whatever the wall clock says.
- **Wall-clock.** "9am tomorrow" is arithmetic on the local calendar
  and then a resolution to an instant. On a clock-change day the
  elapsed distance is twenty-three or twenty-five hours.
- Both are legitimate. The bug is not choosing.

Two local times are ambiguous or non-existent on clock-change days.
Declare the resolution policy once, the same way you declare a rounding
mode, and never let a library default decide it silently.

## The two-dimension escalation

Where a fact can be corrected after the event, one dimension cannot
answer what we thought was true when we ran the payroll (EV-0275). The
escalation, ordered by cost:

1. **Audit log.** Cheap to record, expensive to reconstruct from.
2. **Effectivity dating.** Validity is explicit on the record, and
   every reader now knows about time.
3. **Temporal property.** The date sits behind an accessor, so most
   readers do not see it.
4. **Fully versioned object.** The whole thing is versioned.

Per D4, stay at one dimension until somebody has actually asked a
two-dimensional question. When you move, take valid time and
transaction time together. Storage engines now offer system-versioned
tables, which changes the economics since the source was written and is
worth checking before hand-rolling step four.

## What this reference does not settle

Recurrence rules, calendar systems other than the proleptic Gregorian,
leap seconds, and clock skew between machines. The sources here cover
none of them.
