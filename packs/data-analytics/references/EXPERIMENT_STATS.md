---
summary: Experiment mechanics behind B4 and B5, the sample ratio check, power arithmetic, variance reduction and the interpretation errors that produce false conclusions
type: foundation
tags: [data, testing, product]
kind: fact
scope: estate
sources: [EV-0059, EV-0313, EV-0315, EV-0316]
volatility: stable
review: 2029-08
---

# Experiment statistics reference

Level-three material behind binding requirements B4 and B5 and Wargame
`packs/data-analytics/wargames/WG-DATA-006-experiment-stopping.md`. Read
this when running or reading an experiment, not before.

## The sample ratio mismatch check

**What it is.** A test of whether the observed split between variants
matches the split you asked for. It is a goodness-of-fit test, usually
chi-squared with one degree of freedom for two variants, over the counts
of assigned units.

**Procedure.**

1. Take the count of units assigned to each variant. Units, not events,
   and at the randomisation unit declared under B4.
2. Compute expected counts from the declared ratio and the observed
   total.
3. Compute the chi-squared statistic and its p-value.
4. Report the p-value with the result, always, whether it passes or not.
5. Below a conventional threshold, the experiment is void. Do not
   analyse it, do not report a lift, and do not report it as a null
   result either. It is not a result.

**Why voiding is the right response.** A deviation from the assignment
ratio means something interfered between assignment and measurement, and
whatever interfered almost certainly also moved the metric. There is no
confidence level at which the number becomes usable (EV-0316).

**The search order when it fails.** Causes sort by where they arise, and
this ordering is the useful part:

| Layer | Look for |
| --- | --- |
| Assignment | bucketing bug, unequal variant weights in configuration, a variant that fails to load |
| Execution | one variant redirecting, timing out, or crashing before the assignment event fires |
| Log processing | joins that drop rows, deduplication that hits one variant harder, bot filters applied after assignment |
| Telemetry | assignment events lost for one variant, different SDK paths per variant |
| Interference | another experiment overlapping, or units moving between variants |

**Its limit.** The check needs enough units for a ratio deviation to be
detectable. A small experiment can pass while badly broken. A pass is
weak evidence of health, a failure is strong evidence of illness.

## Power arithmetic, before traffic starts

The four quantities are the baseline rate, the minimum effect worth
detecting, the significance level and the power. Fix three and the
fourth follows. The order of operations that matters:

1. State the minimum effect worth acting on. Not the effect you hope
   for, the smallest one that would change what you do.
2. Compute the required sample size per variant.
3. Divide by the units per week you can actually assign.
4. Compare that to the window in which the answer still matters.
5. If step 4 fails, you are in option D of WG-DATA-006. Say so and stop.

Doing this after the test has started is not power analysis, it is
justification.

## Variance reduction

Using each unit's pre-experiment behaviour as a covariate removes the
part of the metric that has nothing to do with the treatment. On one
large search product this cut variance by roughly half, which is the
same power at half the users or half the duration (EV-0315).

Preconditions, all of them required: a stable randomisation unit, that
unit observed before the experiment started, and a pre-period metric
that predicts the in-period metric. For new users, first-session funnels
and anonymous traffic none of these hold, and the variance reduction is
zero. For rare conversion events the correlation can be near zero even
when the unit is stable.

## The interpretation errors that produce false conclusions

Each of these is an error of reading, not of computation (EV-0313).

- **The p-value read as the probability the result is chance.** It is
  not. It is the probability of data at least this extreme if there were
  no effect.
- **Continuous monitoring of a fixed-horizon test.** The false positive
  rate leaves its nominal five per cent behind, and the more often you
  look the further it goes.
- **The prior ignored.** With a low base rate of ideas that move the
  metric, a bare significant result is more likely false than a naive
  reading suggests. Scope note: the base rate figure is measured on
  mature products at scale.
- **Twyman's law forgotten.** A surprisingly large effect is evidence of
  a bug before it is evidence of a win. Check the instrumentation before
  celebrating.
- **Guardrails treated as goals.** Goal metrics decide the ship,
  guardrails block only on statistically significant harm (EV-0059).
  Treating every guardrail wobble as a veto means nothing ever ships.
- **The null result read as proof of no effect.** A test that failed to
  reach significance says the effect was not detectable at this sample
  size, which is a different sentence.

## What is observational and what is not

Randomised assignment supports a causal claim. Everything else in a
product analytics stack (funnels, cohorts, before-and-after charts,
segment comparisons) is observational and supports a descriptive claim
only. The discipline is in the verb: "changed alongside" rather than
"caused". Quasi-experimental designs exist and are outside the scope of
this pack; none of the sources here supports one.
