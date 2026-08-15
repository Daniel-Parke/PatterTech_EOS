---
id: GD-SUPPORT-003
summary: Who declares a customer-visible incident, and on what signal?
kind: wargame
type: wargame
tags: [delivery, eos, ops, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-SUPPORT-004, DOC-SUPPORT-005]
applies_when: [has_customer_visible_incident]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: anecdotal
sources: [EV-0020, EV-0096, EV-0200]
review: 2028-08
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SUPPORT-003: Who declares a customer-visible incident, and on what signal?

## Decision question and stakes

Technical escalation and customer-facing declaration are two decisions,
and conflating them produces either silence during a real outage or a
status page that cries wolf. Nobody has outcome data on either route.
This guide exists to force the choice and record it, rather than to
pretend the evidence settles it.

## Doctrines or coverage gap under pressure

- `DOC-SUPPORT-004` (default): The severity ladder is written before the incident, and one band changes what the organisation does.
- `DOC-SUPPORT-005` (default): A customer-visible incident records a communication owner separately from the person changing the system.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **The cost of a late notice against the cost of a false alarm.** For
  a paid product with an operations audience, late is usually worse.
- **Whether an objective signal exists at all.** A burn alert needs a
  service level objective already defined and trusted.
- **Who is awake.** A manual page needs a reachable named person.
- **How visible the affected surface is.** The three-factor score
  below separates a core path from an ancillary one.
- **Whether the audience can act on the notice.** A notice nobody can
  use is noise dressed as transparency.

Applicability is `has_customer_visible_incident`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Manual page to a named person
Customer-facing declaration is a deliberate human act: a named person
is paged, and that person decides whether the business responds
(EV-0422). Buys a decision with a face on it and few
false alarms. Costs latency, and it fails outright when the named
person is unreachable.

### B. Automatic declaration on an objective trigger
Declaration fires from a burn alert against a stated objective, or from
one of the written triggers: a second person is needed, the failure is
customer-visible, or an hour of focused work has not closed it
(EV-0020, EV-0096, EV-0423). Buys speed and removes
the judgement that goes missing at three in the morning. Costs false
alarms, and it needs an objective good enough to trust, which most
young ventures do not have.

### C. Three-factor score, then declare
Score visibility (core service or ancillary), actual impact at the
current traffic level rather than potential impact, and duration so far
plus confidence of resolving within the hour. Write the formula down
before the incident (EV-0422). Buys a repeatable
customer-facing decision that a solo operator can apply, and it is the
part of the source that transfers to any size. Costs the discipline of
writing a formula while nothing is broken.

### D. Automatic trigger, human confirmation, fixed timeout
The trigger fires and pages; a named person may stand it down within a
stated window; if nobody answers, declaration proceeds. Buys B's floor
with A's judgement on top. Costs a working rota, a stand-down record,
and a timeout number that nobody has evidence for.

## Failure premises

### Premortem for A. Manual page to a named person

Assume `A. Manual page to a named person` was selected and the outcome failed. Test this option's stated failure mechanism first: latency, and it fails outright when the named person is unreachable.

### Premortem for B. Automatic declaration on an objective trigger

Assume `B. Automatic declaration on an objective trigger` was selected and the outcome failed. Test this option's stated failure mechanism first: false alarms, and it needs an objective good enough to trust, which most young ventures do not have.

### Premortem for C. Three-factor score, then declare

Assume `C. Three-factor score, then declare` was selected and the outcome failed. Test this option's stated failure mechanism first: the discipline of writing a formula while nothing is broken.

### Premortem for D. Automatic trigger, human confirmation, fixed timeout

Assume `D. Automatic trigger, human confirmation, fixed timeout` was selected and the outcome failed. Test this option's stated failure mechanism first: a working rota, a stand-down record, and a timeout number that nobody has evidence for.

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

## Safe default

C, with the formula written in
`packs/support-operations/refs/SEVERITY_AND_DECLARATION.md` and the
declaration triggers from PACK.md D6 alongside it. Declaration records
`declared_at` and `declared_by` at the moment it happens, plus the
separate communication and fix owners PACK.md B3 asks for, and a
postmortem due date is set at resolution under PACK.md D9 (EV-0200).
B3 is a default since the 2026-08 audit, so a venture that runs one
owner for both writes down why.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****The cost of a late notice against the cost of a false alarm.** For a paid product with an operations audience, late is usually worse.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C, with the formula written in `packs/support-operations/refs/SEVERITY_AND_DECLARATION.md` and the declaration triggers from PACK.md D6 alongside it. Declaration records `declared_at` and `declared_by` at the moment it happens, plus the separate communication and fix owners PACK.md B3 asks for, and a postmortem due date is set at resolution under PACK.md D9 (EV-0200). B3 is a default since the 2026-08 audit, so a venture that runs one owner for both writes down why.

**Exit condition:** Stop or roll back the selected branch when latency, and it fails outright when the named person is unreachable, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **The cost of a late notice against the cost of a false alarm.** For a paid product with an operations audience, late is usually worse.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
