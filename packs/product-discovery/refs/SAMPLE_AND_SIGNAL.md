---
summary: How many people to talk to, when an experiment can be powered, and what to do below the power floor
type: foundation
tags: [product, testing]
kind: fact
scope: estate
sources: [EV-0059]
volatility: slow
review: 2028-07
---

# Samples, power and the low-traffic case

Level-three material behind defaults D5 and D7 in
`packs/product-discovery/PACK.md` and behind
`packs/product-discovery/guides/GD-DISC-002-user-evidence-source.md`.
Everything here is bounded by its source population, which is stated
each time.

## Talking to people: reason about the worst case

The resampling study drew random subsets from sixty participants tested
on one interface and measured the spread rather than the mean
(`EV-0407`).

| Participants | Worst-case share of known problems found |
| --- | --- |
| Five | about 55 per cent, best case 99 |
| Ten | floor about 80 per cent |
| Twenty | floor about 95 per cent |

How to read this table. The denominator is problems found by the full
sixty, so problems nobody found are invisible to the analysis. It is one
2003 web application and one problem set, and it measures usability
defect detection in a moderated lab task. It says nothing about whether
a demand exists or whether anyone would pay. Do not carry the exact
percentages to another interface class; carry the shape, which is that a
five-person sample has a wide spread and you cannot tell which draw you
got.

The competing convention argues that on a fixed budget three rounds of
five beat one round of fifteen, because each round changes the design
and so changes the problem set (`EV-0408`). That is a
different objective function rather than a contradicted result. Its own
caveats are the part most often dropped: a single participant can
mislead, and distinct user groups need their own participants. It is
twenty-six years old, never revised, and it models defect finding rather
than problem validation.

The rule this pack takes: plan the sample against the worst case, and
spend any spare budget on another round rather than another participant
in the same round. The recruitment frame matters more than either
(`EV-0404`).

## Experiments: the power floor

An experiment is evidence only if the stopping rule, the metric and the
segmentation were fixed before the data arrived
(`EV-0406`). Below the traffic needed to detect the
effect you care about, that discipline does not save you, because the
test cannot resolve the question at all.

No source located says at what traffic level experimentation stops being
theatre for a venture with hundreds rather than millions of users. That
gap is real and this pack does not paper over it. What follows is a
working rule, labelled as such, not a finding.

**The working rule.** Before running a test, write down the metric's
current rate and the smallest change that would alter your decision. If
you cannot state both, the test is not ready. If the number of exposures
you can gather in the window you are prepared to wait is not enough to
tell that change from noise, do not run a test. Run the change with a
named signal read by hand instead, and say in the record that you are
reading a signal rather than measuring an effect.

**Signs the test is theatre.** The metric is a conversion rate on a
surface with tens of visits a week. The effect you are hoping for is a
few per cent. The window is "until we see something". Any of the three
alone is enough to stop.

**The failure modes that get worse without a platform.** Stopping when
the result first crosses significance, treating a small-sample result as
directional, and reading a surprisingly large effect as a discovery
rather than as an instrumentation bug
(`EV-0406`). A venture running one manual test a
quarter has none of the automated protection that paper assumes, so
these get more likely rather than less.

## What to do below the floor

- Ship behind a flag to a named group and read what they do, then say
  what you read.
- Pick a signal that is a count of events rather than a rate, because
  counts are readable at low volume and rates are not.
- Accept a longer window and write it down before you start, per B7.
- Use the asymmetric gate shape anyway: the goal signal drives the
  decision, and a guardrail only blocks on clear harm (EV-0059). The
  thresholds in that source are vendor conventions, not validated
  optima, so pick your own and record them.
- State in the record that the result is a signal, not a measurement.
  The word matters, because a signal read by hand cannot later be quoted
  as though a test had produced it.

## Why any of this beats ranking harder

Across a large corpus of randomised online experiments, roughly a third
of ideas moved the target metric positively, a third were flat and a
third were negative, and expert judgement inside the team did not
predict which (`EV-0405`). The population is very
high-traffic consumer search and portal surfaces, so the base rate is a
prior rather than a measurement of your product. The prior is still
worth acting on: if the team cannot sort ideas, spending the effort on
throughput and on reading results honestly beats spending it on a better
ranking formula. Nobody has measured whether the same base rate holds
for agent-generated ideas, and the paper predates model-assisted
ideation entirely.
