---
summary: How a buyer experiences the product before paying, and why the evidence gives a measurement rule rather than a trial length
type: guide
tags: [money, product]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0294, EV-0295, EV-0298, EV-0300, EV-0059]
review: on-change-of:multi-firm-trial-length-replication
---

# GD-BMP-003: how does someone try this before paying?

## The question

Between first contact and first payment there is a gap, and the fork is
what fills it. This guide covers the shape of that gap. It does not
cover what the price is, which is
`packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md`.

## It depends on

- How long does it take a new buyer to reach the first useful result?
- Does the value only appear after a full cycle of the buyer's own data?
- Can you afford to serve people who will never pay?
- Is the buyer an individual deciding alone, or a committee with
  procurement?
- Can you measure adoption, immediate conversion and delayed conversion
  separately?

## Options

### A. No trial, buy outright

Money first, with a refund window. Buys: no free-tier cost, no
conversion funnel to maintain, and every user is a customer. Costs: the
buyer has to believe you on nothing, so it only works where the price is
low enough to risk or the reputation is already made.

### B. Time-boxed free trial

Full product, fixed window, then it stops. Buys: the buyer learns
whether it works on their own material, which is the mechanism the
evidence identifies (EV-0294). Costs: the window
is a real variable that has to be tested, and a badly chosen one loses
buyers who never reached the first useful result.

### C. Freemium, a permanently free tier

A limited version that never expires. Buys: no clock, a large top of
funnel, and word of mouth. Costs: you pay to serve people indefinitely,
and the boundary between free and paid becomes the hardest product
decision you own.

### D. Paid pilot with a money-back window

A short, priced engagement with an exit. Buys: qualification, because
the buyer has committed something, and it fits committee purchasing.
Costs: it is a sales motion, and a one-person venture may not have the
time it takes.

## Decision rule

- Consumer, self-serve, and value visible within days: B.
- Value only appears after a full billing cycle of the buyer's own data:
  B with a longer window, and say so in the test plan, because the
  evidence below does not cover that case.
- Marginal cost of a free user is near zero and the product spreads by
  being used: C.
- Business buyer with procurement: D.
- Low price, strong reputation, or a product that demonstrates itself in
  a screenshot: A.

## Default

B, starting near a week, shipped with a test plan and never as a fixed
number on its own.

## The measurement rule that replaces a number

Two randomised field experiments point in opposite directions on
duration and agree on method.

- A seven-day trial beat fourteen and thirty at one SaaS firm, raising
  subscriptions by about 5.6 per cent, with consumer learning as the
  mechanism and end-of-trial inactivity predicting non-conversion
  (EV-0294).
- Extending from three to seven days at a different firm raised trial
  adoption by about eleven per cent and delayed conversion by about
  forty-two per cent, with no significant movement in immediate
  conversion and overall subscriptions up about twenty-one per cent
  (EV-0295).

Together they support an interior optimum around a week rather than a
direction, and they kill any sentence of the form "use an N day trial".
The rule that survives is procedural.

1. Treat trial length as a variable with a pre-registered decision rule,
   in the shape the experiment framework sets out (EV-0059).
2. Measure trial adoption, immediate conversion and delayed conversion
   separately. A test judged on immediate conversion alone would have
   read as a null and been abandoned in the second study.
3. Instrument time to first useful result, because that is what the
   trial is actually selling.
4. Record the length you shipped, the test that set it, and the date it
   is next re-run.

## Evidence boundary

Both studies are single firms in consumer-facing self-serve SaaS. The
5.6 per cent and the eleven, forty-two and twenty-one per cent figures
belong to those firms and those funnels, and quoting them as a general
effect size is a misuse. Neither covers B2B pilots with procurement, and
the second study's authors state that external generalisability remains
to be validated. Nothing here says what a free tier costs you.

## Obligations the trial creates

A consumer trial that rolls into a paid subscription is a subscription
contract. The renewal reminder, the express acknowledgement of the
payment obligation, the online exit route and cooling-off apply
(EV-0298), and a trial designed so that the
easiest path is to keep paying by accident is on the regulator's
almost-always-harmful list (EV-0300).

## Worked rulings

- **PatterTech EOS business-model-pricing pack (2026-08, argued)**: B,
  near a week, with a test plan required before the number ships.
  Argued from EV-0294 and
  EV-0295 read as a pair.
- **First UK consumer subscription, composed (2026-08, inherited)**:
  B at seven days, carrying test plan TP-01 with a three-stage funnel
  readout. See
  `packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md`.
