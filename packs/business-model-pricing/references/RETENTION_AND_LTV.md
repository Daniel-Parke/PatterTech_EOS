---
summary: Why cohort retention rises on its own, why blended churn gives a wrong lifetime value, and what to emit instead
type: foundation
tags: [money, data]
kind: fact
scope: estate
sources: [EV-0296, EV-0297, EV-0197]
volatility: stable
review: 2029-08
---

# Retention and lifetime value

Level three material behind default D4. Read this before writing any
number that claims to say what a customer is worth.

## The sorting effect

Customers differ in how likely they are to lapse. The ones most likely
to lapse do so first. Every period the surviving mix is made of better
retainers than the period before, so the observed retention rate of a
cohort rises with cohort age even when no individual customer changes
behaviour at all (EV-0296).

Two consequences follow, and both are unintuitive enough that they get
rediscovered every year.

1. A rising retention rate is not evidence that anything improved. It
   is what heterogeneity produces on its own. Note which quantity is
   rising: the share of the original cohort still present falls forever,
   while the period-over-period rate climbs.
2. A single average churn rate applied forward is the wrong projection.
   It understates the survivors and overstates the leavers, and the
   error compounds with every period projected.

## The formula the pack refuses

Lifetime value as average revenue per user divided by a blended churn
rate is wrong in a knowable direction. The blended rate is dominated by
early leavers, so the resulting figure understates the value of a cohort
that has already sorted itself. It is refused whatever spreadsheet it
arrives in.

The check is arithmetic: compute average revenue per user over blended
churn from the same inputs, and if the reported lifetime value lands
within one per cent of it, the reported number came from that formula.

## What to emit instead

**A curve, not a number.** Report one row per cohort age, and keep two
distinct columns, because conflating them is where the sorting effect
gets lost.

- **survivor_share**: how much of the original cohort is left. It is
  non-increasing by construction, because nobody comes back.
- **retention_rate**: survivors at this age divided by survivors at the
  age before. This is the number that rises, and it rises for the
  sorting reason alone.

The check that matters runs on retention_rate: a projected retention
rate that is flat, or falls with cohort age, means a single blended
churn rate was applied forward, and the projection is wrong. A
projected survivor_share that fails to decline means something worse
has happened to the arithmetic.

A minimal shape for the retention file:

```csv
cohort_age_months,surviving,survivor_share,retention_rate,basis
0,1000,1.000,,observed
1,780,0.780,0.780,observed
2,690,0.690,0.885,observed
3,634,0.634,0.919,observed
4,,0.593,0.936,fitted
5,,0.560,0.945,fitted
```

**A method name on every lifetime value.** Either cohort-curve,
fitted-heterogeneity, or not-computed. Not-computed is the honest answer
in a venture's first months, and it is a better answer than a number
built on three data points.

## When you cannot fit anything yet

Fitting heterogeneity needs several periods of contractual cohort data,
which a first-year venture does not have. Until then:

- Report the observed curve, however short it is.
- Set lifetime_value.method to not-computed and leave the value at zero
  rather than inventing one.
- Do not make a spend decision that only works if a projected lifetime
  value is right.

## Where this model stops

- It covers contractual settings with clean renew-or-lapse events.
  Non-contractual and metered revenue need a different model family,
  because expansion and contraction move inside a live account and there
  is no lapse event to observe
  (EV-0296, and see
  `packs/business-model-pricing/wargames/WG-BMP-002-charging-unit.md`).
- It says nothing about why customers churn, and nothing about what a
  price change would do to the curve.
- Revenue in the numerator is recognised revenue, not cash collected
  (EV-0297), and the cost side is the allocated
  cost to serve (EV-0197). A margin computed from cash receipts against
  unallocated cost is two errors compounding.

## The reporting rule that goes with it

Every retention or lifetime value number that leaves the venture carries
its formula next to it, and a definition change is stated in the report
where it happens. See
`packs/business-model-pricing/references/METRIC_DEFINITIONS.md`.
