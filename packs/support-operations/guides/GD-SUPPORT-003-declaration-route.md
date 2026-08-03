---
summary: Who declares a customer-visible incident, and on what signal?
kind: guide
authority: default
basis: decision
evidence_grade: anecdotal
scope: estate
sources: [EV-0020, EV-0096, EV-0200]
review: 2027-08
type: guide
tags: [ops, delivery]
review_by: 2027-08
---

# GD-SUPPORT-003: Who declares a customer-visible incident, and on what signal?

## The question

Technical escalation and customer-facing declaration are two decisions,
and conflating them produces either silence during a real outage or a
status page that cries wolf. Nobody has outcome data on either route.
This guide exists to force the choice and record it, rather than to
pretend the evidence settles it.

## It depends on

- **The cost of a late notice against the cost of a false alarm.** For
  a paid product with an operations audience, late is usually worse.
- **Whether an objective signal exists at all.** A burn alert needs a
  service level objective already defined and trusted.
- **Who is awake.** A manual page needs a reachable named person.
- **How visible the affected surface is.** The three-factor score
  below separates a core path from an ancillary one.
- **Whether the audience can act on the notice.** A notice nobody can
  use is noise dressed as transparency.

## Options

### A. Manual page to a named person
Customer-facing declaration is a deliberate human act: a named person
is paged, and that person decides whether the business responds
(FRAG-SUPPORT-OPERATIONS-02). Buys a decision with a face on it and few
false alarms. Costs latency, and it fails outright when the named
person is unreachable.

### B. Automatic declaration on an objective trigger
Declaration fires from a burn alert against a stated objective, or from
one of the written triggers: a second person is needed, the failure is
customer-visible, or an hour of focused work has not closed it
(EV-0020, EV-0096, FRAG-SUPPORT-OPERATIONS-03). Buys speed and removes
the judgement that goes missing at three in the morning. Costs false
alarms, and it needs an objective good enough to trust, which most
young ventures do not have.

### C. Three-factor score, then declare
Score visibility (core service or ancillary), actual impact at the
current traffic level rather than potential impact, and duration so far
plus confidence of resolving within the hour. Write the formula down
before the incident (FRAG-SUPPORT-OPERATIONS-02). Buys a repeatable
customer-facing decision that a solo operator can apply, and it is the
part of the source that transfers to any size. Costs the discipline of
writing a formula while nothing is broken.

### D. Automatic trigger, human confirmation, fixed timeout
The trigger fires and pages; a named person may stand it down within a
stated window; if nobody answers, declaration proceeds. Buys B's floor
with A's judgement on top. Costs a working rota, a stand-down record,
and a timeout number that nobody has evidence for.

## Decision rule

If a trusted service level objective exists and there is a rota, take
D. If there is a rota but no trusted objective, take C and page under
A. If there is one responder, take C: the score is the whole mechanism,
and the manual page is a page to yourself, which is a note in a
record rather than a phone call. Take B alone only where the objective
has survived at least one quarter without a false alarm nobody could
explain.

Whichever route is chosen, the severity band comes from the ladder
under PACK.md B2, the higher band is taken when the call is unclear,
and the band is not argued during the incident.

## Default

C, with the formula written in
`packs/support-operations/refs/SEVERITY_AND_DECLARATION.md` and the
declaration triggers from PACK.md D6 alongside it. Declaration records
`declared_at` and `declared_by` at the moment it happens, plus the
separate communication and fix owners required by PACK.md B3, and a
postmortem due date is set at resolution under PACK.md D9 (EV-0200).

## Worked rulings

- **support-operations exemplar (2026-08, argued)**: a solo responder
  scored the outage at item 17 as core-path, impacting customers now,
  and past twenty minutes with no confidence of a fix within the hour.
  It declared as the band that switches response mode. The same person
  held both owner fields, and both were filled, because the record has
  to show the decision was taken. See
  `packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`.
- **No route is evidenced (external, inherited)**: the manual-page
  position and the auto-declare position both come from practice with
  no measured comparison. The estate's ruling is that the choice must
  be recorded per venture, so that a later argument has something to
  argue with.
