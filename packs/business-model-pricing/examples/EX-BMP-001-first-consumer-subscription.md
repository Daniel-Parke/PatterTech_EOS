---
summary: A worked run of the pack, pricing a first UK consumer subscription and repricing it when unit costs rise
kind: example
scope: estate
type: example
tags: [money, product, data]
---

# EX-BMP-001: a first consumer subscription, priced and then repriced

A composed example, not a venture record. It shows the pack applied end
to end on one decision, including the parts where the honest answer is
that the evidence does not reach.

## The situation

A one-person venture is about to charge for a consumer web product in
the UK. Twelve months of infrastructure and support cost sit in the
books. Eighteen monthly signup cohorts exist from the free period, with
retained counts. There is no comparable product the buyer could line it
up against, and nobody has ever paid for it.

## Step 1: the anchor, and the condition

Following `packs/business-model-pricing/wargames/WG-BMP-001-price-anchor.md`.

Value-informed is refused, not on principle but on capability: there is
no measured before-and-after in any buyer's world, and nobody to build
one this month. Competition-informed is refused because there is no
comparable. That leaves cost-informed, and the condition is written down
as exactly that: no comparable product and no purchase history at the
decision point.

The FinOps allocation gives an allocated cost to serve of 1.40 pounds
per active account per month. A target contribution margin of sixty per
cent puts the floor at 3.50. A price sensitivity survey run earlier
suggested a range topping out near nine pounds; under default D6 that is
recorded as an upper bracket and not as the decision. The price is set
at 6.00 pounds a month, inside the band, with the reasoning stated.

The revisit date is set six months out, at which point either purchase
evidence exists or the practice is re-argued.

## Step 2: the unit, the tiers and the unavoidable set

Following `packs/business-model-pricing/wargames/WG-BMP-002-charging-unit.md`.

Flat per period, one tier. Metering is rejected because the buyer cannot
forecast the counted thing, which under the Wargame's decision rule ends
the argument. A second tier is considered and dropped: nothing in the
evidence sets a tier count, and a tier added to make the other one look
better is a decoy, which sits on the regulator's harmful list and mostly
fails to work anyway.

Payment processing is unavoidable, so it is inside the 6.00. Storage
beyond a fair-use line is genuinely declinable and is listed as an
optional charge with a written note on how a buyer avoids it. VAT is not
yet chargeable, and the rolling twelve-month turnover figure goes on the
dashboard as a watch metric rather than a year-end surprise.

## Step 3: the trial

Following `packs/business-model-pricing/wargames/WG-BMP-003-try-before-paying.md`.

Seven days, because the evidence supports an interior optimum near a
week and gives no better number. The seven ships with test plan TP-01,
which reads out trial adoption, immediate conversion and delayed
conversion separately, and which is scheduled to re-run at the revisit
date. Writing seven days without TP-01 would have been the failure the
Wargame names: a number the evidence does not support.

## Step 4: retention and lifetime value

Following `packs/business-model-pricing/references/RETENTION_AND_LTV.md`.

The eighteen cohorts are collapsed into a retention curve, one row per
cohort age, observed rows marked observed. With eighteen periods there
is enough to fit heterogeneity, so ages beyond the observed window are
projected and marked fitted. The survivor share falls throughout, while
the period-over-period retention rate climbs from 0.78 toward 0.94,
because the sorting effect makes it climb.

The tempting number is 6.00 divided by a blended monthly churn of 0.09,
which gives about 67 pounds and is wrong in a knowable direction. The
lifetime value in the decision record is computed from the curve against
contribution rather than price, comes out lower, and carries the method
name fitted-heterogeneity.

## Step 5: the obligations the price created

Following `packs/business-model-pricing/references/UK_OBLIGATIONS.md`.

The obligations file names, with dates and refresh triggers: the
headline price completeness duty and the drip pricing ban; the DMCC
subscription duties including renewal reminders, the online exit route
and cooling-off, marked as enacted and awaiting commencement; the
30 day commercial payment default; VAT registration at ninety
thousand pounds rolling turnover; and Making Tax Digital for Income Tax
from 6 April 2026 above fifty thousand pounds.

Two product consequences fall straight out. The cancellation route is
built in the first release rather than the third, because retrofitting
it costs more. The renewal reminder is a scheduled job from day one.

## Step 6: the repricing trigger, written before it fires

Following `packs/business-model-pricing/wargames/WG-BMP-004-repricing-trigger.md`.

Cost-indexed, threshold at plus or minus ten per cent movement in
allocated unit cost over a rolling quarter, cause types limited to cost
and value. The script that recomputes the price is committed beside the
decision record and is executable.

## What happens when the cost rises

Unit costs rise fifteen per cent, from 1.40 to 1.61. The threshold is
crossed, the script runs, and it emits a new headline of 6.50 with a
cause of type cost. The announcement says what moved, by how much, from
when, and that the trial and the fair-use line are unchanged. Existing
customers are held at 6.00 for their current term, which is recorded as
a deliberate cost rather than a kindness that nobody priced.

The announcement that was drafted first said the product had become more
popular. That draft was refused: a demand cause is refused at the schema
level, and the fairness evidence says a demand-framed rise reads as
exploitation. The evidence for that is 1986 survey judgement rather than
observed churn, which is why the Wargame holds it as a default and why the
venture is instrumenting its own cohorts to check.

## What this run could not do

- It could not show that a flat price beats metering, because no causal
  evidence exists in this pack for that comparison.
- It could not set the trial at seven days on evidence from this product.
  The seven is borrowed from two single firms in a different category
  and holds only until TP-01 reports.
- It could not build a control against the venture's own bookkeeping.
  With one person, segregation of duties is unavailable, and the written
  dated definitions are a weaker substitute that is named as weaker.
