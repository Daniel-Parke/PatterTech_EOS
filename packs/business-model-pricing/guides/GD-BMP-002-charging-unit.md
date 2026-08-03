---
summary: What the buyer is charged per, and what each unit costs in accounting, forecasting and support
type: guide
tags: [money, product]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [FRAG-BUSINESS-MODEL-PRICING-10, FRAG-BUSINESS-MODEL-PRICING-11, FRAG-BUSINESS-MODEL-PRICING-13, FRAG-BUSINESS-MODEL-PRICING-14, EV-0197]
review: 2028-01
review_by: 2028-01
---

# GD-BMP-002: what is the unit of charge?

## The question

Once you know what the price is anchored to, you have to say what the
buyer is charged per: per person, per account, per unit consumed, or per
period regardless. The unit decides how the revenue is recognised, how
predictable the bill feels, and how much support the pricing model
generates on its own.

## It depends on

- Can the buyer predict their own bill a month ahead?
- Can the buyer control the thing being counted?
- Does consumption track the benefit the buyer gets, or only your cost?
- Does the bundle decompose into distinct promises with defensible
  stand-alone prices (FRAG-BUSINESS-MODEL-PRICING-11)?
- Does the venture have the metering, and can it prove the count?

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
(FRAG-BUSINESS-MODEL-PRICING-11). Cohort revenue also stops being a
clean renew-or-lapse event, which breaks the retention model the pack
otherwise relies on (FRAG-BUSINESS-MODEL-PRICING-10).

### D. Outcome or transaction share

Charge a proportion of a result the buyer can see. Buys: the tightest
link between price and delivered value, and an easy sale. Costs:
attribution disputes, revenue that swings with someone else's business,
and a measurement obligation that never ends.

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
headline price (FRAG-BUSINESS-MODEL-PRICING-13), and a tier built to
make another tier look better is on the regulator's harmful list
(FRAG-BUSINESS-MODEL-PRICING-14).

## Default

A, the simplest unit the buyer can forecast, until there is evidence
that heavy and light users differ enough to matter. Reason: the
accounting, the forecasting and the support cost are all lowest, and the
switch to B or C later is a repricing rather than a rebuild.

## Evidence boundary

There is no causal evidence in this pack that any unit beats another on
retention or revenue. The claims in circulation that usage-based pricing
lifts net revenue retention trace to vendor surveys exposed to
survivorship, and none is carried here. What is carried is structural:
the recognition consequence
(FRAG-BUSINESS-MODEL-PRICING-11), the retention-modelling consequence
(FRAG-BUSINESS-MODEL-PRICING-10) and the allocation requirement
(EV-0197). Anyone presenting a unit-of-charge choice as settled by
evidence is asserting.

## Worked rulings

- **PatterTech EOS business-model-pricing pack (2026-08, argued)**: A as
  the default, C only where the buyer can both forecast and control the
  counted unit. Argued from the recognition and retention consequences,
  with the marketing benchmarks refused.
- **First UK consumer subscription, composed (2026-08, inherited)**:
  A, monthly flat, with storage above a fair-use line treated as an
  optional charge and named as optional in the decision record. See
  `packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md`.

## Related

The anchor for the number is
`packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md`. The
recognition and obligation detail is in
`packs/business-model-pricing/refs/UK_OBLIGATIONS.md` and
`packs/business-model-pricing/refs/DECISION_RECORD.md`.
