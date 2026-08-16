---
id: WG-BMP-002
summary: What the buyer is charged per, and what each unit costs in accounting, forecasting and support
kind: wargame
type: wargame
tags: [eos, money, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-BMP-009]
applies_when: [sets_a_price]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0296, EV-0297, EV-0299, EV-0300, EV-0197]
review: 2028-01
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-BMP-002: what is the unit of charge?

## Decision question and stakes

Once you know what the price is anchored to, you have to say what the
buyer is charged per: per person, per account, per unit consumed, or per
period regardless. The unit decides how the revenue is recognised, how
predictable the bill feels, and how much support the pricing model
generates on its own.

## Doctrines or coverage gap under pressure

- `DOC-BMP-009` (default): Every commercial number travels with its definition.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can the buyer predict their own bill a month ahead?
- Can the buyer control the thing being counted?
- Does consumption track the benefit the buyer gets, or only your cost?
- Does the bundle decompose into distinct promises with defensible
  stand-alone prices (EV-0297)?
- Does the venture have the metering, and can it prove the count?

Applicability is `sets_a_price`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Flat per period

One price, everything included. Buys: the simplest thing to say, the
simplest thing to recognise, and a bill the buyer never has to think
about. Costs: heavy users are subsidised by light ones, and expansion
revenue has to come from a tier change rather than from growth.

### B. Per seat or per account

Charge per named user or per tenant. Buys: a unit the buyer already
understands and administers, forecastable to the buyer, and expansion
that follows their headcount. Costs: it tracks the buyer's staffing
rather than the value delivered, and it rewards seat-sharing, which then
becomes an enforcement problem you did not want.

### C. Metered on consumption

Charge per unit consumed. Buys: alignment where consumption really does
track benefit, and expansion without a renegotiation. Costs: the buyer
must be able to forecast and control the counted thing, or the model
turns into a support queue. Recognition gets harder, because variable
consideration and stand-alone selling prices for metered add-ons need
working out rather than asserting
(EV-0297). Cohort revenue also stops being a
clean renew-or-lapse event, which breaks the retention model the pack
otherwise relies on (EV-0296).

### D. Outcome or transaction share

Charge a proportion of a result the buyer can see. Buys: the tightest
link between price and delivered value, and an easy sale. Costs:
attribution disputes, revenue that swings with someone else's business,
and a measurement obligation that never ends.

## Failure premises

### Premortem for A. Flat per period

Assume `A. Flat per period` was selected and the outcome failed. Test this option's stated failure mechanism first: heavy users are subsidised by light ones, and expansion revenue has to come from a tier change rather than from growth.

### Premortem for B. Per seat or per account

Assume `B. Per seat or per account` was selected and the outcome failed. Test this option's stated failure mechanism first: it tracks the buyer's staffing rather than the value delivered, and it rewards seat-sharing, which then becomes an enforcement problem you did not want.

### Premortem for C. Metered on consumption

Assume `C. Metered on consumption` was selected and the outcome failed. Test this option's stated failure mechanism first: the buyer must be able to forecast and control the counted thing, or the model turns into a support queue. Recognition gets harder, because variable consideration and stand-alone selling prices for metered add-ons need working out rather than asserting (EV-0297). Cohort revenue also stops being a clean renew-or-lapse event, which breaks the retention model the pack otherwise relies on (EV-0296).

### Premortem for D. Outcome or transaction share

Assume `D. Outcome or transaction share` was selected and the outcome failed. Test this option's stated failure mechanism first: attribution disputes, revenue that swings with someone else's business, and a measurement obligation that never ends.

## Decision rule

- The buyer cannot forecast or control consumption: not C.
- Consumption tracks your cost but not the buyer's benefit: not C
  either; that is a cost recovery problem, and A with a fair-use
  boundary handles it more honestly.
- The buyer administers people and the benefit scales with people: B.
- The result is measurable by both sides and neither disputes
  attribution: D, and only then.
- Anything else, and the first release of anything: A.

Whatever the unit, every unavoidable component of it appears in the
headline price (EV-0299), and a tier built to
make another tier look better is on the regulator's harmful list
(EV-0300).

## Safe default

A, the simplest unit the buyer can forecast, until there is evidence
that heavy and light users differ enough to matter. Reason: the
accounting, the forecasting and the support cost are all lowest, and the
switch to B or C later is a repricing rather than a rebuild.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can the buyer predict their own bill a month ahead?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, the simplest unit the buyer can forecast, until there is evidence that heavy and light users differ enough to matter. Reason: the accounting, the forecasting and the support cost are all lowest, and the switch to B or C later is a repricing rather than a rebuild.

**Exit condition:** Stop or roll back the selected branch when heavy users are subsidised by light ones, and expansion revenue has to come from a tier change rather than from growth, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can the buyer predict their own bill a month ahead?

## Counter-evidence and transfer limits

### Evidence boundary

There is no causal evidence in this pack that any unit beats another on
retention or revenue. The claims in circulation that usage-based pricing
lifts net revenue retention trace to vendor surveys exposed to
survivorship, and none is carried here. What is carried is structural:
the recognition consequence
(EV-0297), the retention-modelling consequence
(EV-0296) and the allocation requirement
(EV-0197). Anyone presenting a unit-of-charge choice as settled by
evidence is asserting.
### Preserved reasoning: Related

The anchor for the number is
`packs/business-model-pricing/wargames/WG-BMP-001-price-anchor.md`. The
recognition and obligation detail is in
`packs/business-model-pricing/references/UK_OBLIGATIONS.md` and
`packs/business-model-pricing/references/DECISION_RECORD.md`.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
