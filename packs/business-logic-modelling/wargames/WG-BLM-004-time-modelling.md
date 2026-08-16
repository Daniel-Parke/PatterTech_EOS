---
id: WG-BLM-004
summary: How much time does this fact carry, which temporal type and how many dimensions?
kind: wargame
type: wargame
tags: [arch, data, eos, product, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-BLM-002]
applies_when: [models_time]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: binding
basis: standard
evidence_grade: observational
sources: [EV-0275, EV-0281, EV-0282]
review: on-change-of:RFC-9557
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-BLM-004: How much time does this fact carry?

## Decision question and stakes

Two forks sit on top of each other. Which temporal type holds this
fact, and how many time dimensions the domain needs. Getting the first
wrong produces bugs twice a year; getting the second wrong produces a
question you cannot answer at all, or a model every reader has to
understand.

## Doctrines or coverage gap under pressure

- `DOC-BLM-002` (binding): A timestamp that will be compared or advanced carries a zone identifier, not just an offset.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `models_time`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. One instant, stored in UTC

Assume `A. One instant, stored in UTC` was selected and the outcome failed. Test this option's stated failure mechanism first: every calendar question: it cannot tell you what day it was for the customer, and it cannot advance by a day across a clock change.

### Premortem for B. The narrowest type that holds the fact

Assume `B. The narrowest type that holds the fact` was selected and the outcome failed. Test this option's stated failure mechanism first: a vocabulary the team has to learn.

### Premortem for C. B, plus a zone identifier wherever arithmetic happens

Assume `C. B, plus a zone identifier wherever arithmetic happens` was selected and the outcome failed. Test this option's stated failure mechanism first: a current time-zone database in every runtime that does the arithmetic.

### Premortem for D. C, plus a second time dimension

Assume `D. C, plus a second time dimension` was selected and the outcome failed. Test this option's stated failure mechanism first: audit log, effectivity dating, temporal property, fully versioned object (EV-0275). Buys answers to correction, dispute and reprocessing questions. Costs complication for every reader of the model, which the source concedes.

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

## Safe default

B plus C, one time dimension, and durations declared as elapsed unless
the rule is explicitly a wall-clock rule. Serialise with the zone
identifier attached rather than the offset alone (EV-0281). Never store
a naive local datetime in a domain that touches more than one zone, and
never store an offset where a zone was meant.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the fact has a zone at all.** A birthday does not. A meeting does. A log line has an instant and nothing else.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B plus C, one time dimension, and durations declared as elapsed unless the rule is explicitly a wall-clock rule. Serialise with the zone identifier attached rather than the offset alone (EV-0281). Never store a naive local datetime in a domain that touches more than one zone, and never store an offset where a zone was meant.

**Exit condition:** Stop or roll back the selected branch when every calendar question: it cannot tell you what day it was for the customer, and it cannot advance by a day across a clock change, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the fact has a zone at all.** A birthday does not. A meeting does. A log line has an instant and nothing else.

## Counter-evidence and transfer limits

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
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
