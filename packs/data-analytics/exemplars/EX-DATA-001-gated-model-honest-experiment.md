---
summary: The data-analytics pack applied end to end to a raw event dump and an experiment whose assignment ratio is broken
type: example
tags: [data, testing, product]
kind: exemplar
scope: estate
---

# EX-DATA-001: The model that gated and the experiment that did not win

A worked run of the data-analytics pack against one concrete situation,
from the first look at the raw files to the written answer. Every pack
rule that fires is named where it fires.

## The situation

A repository holds two files and no pipeline.

- `raw/events.csv`: 200,000 rows of signup and checkout events, columns
  including `user_email`, `event`, `order_total`, `occurred_at`. One
  batch of rows has a null `order_total`.
- `raw/experiment.csv`: assignment and conversion rows for a two-variant
  test declared at 50/50. The observed split is 52.6 to 47.4. A lift for
  variant B was significant at one interim point during the run and is
  not significant at the end.

The request: model these events for analysis, and say whether variant B
won.

## Step 1: activation and routing

Four predicates trip. `defines_events`, because the taxonomy has to be
written down. `publishes_analytics_table`, because the models will be
read by somebody other than this session. `runs_experiment`, because a
metric is being read from an assignment. `handles_analytics_identifier`,
because `user_email` is sitting in the source.

`reads_for_decision` also trips, which is what makes the second half of
this a decision task rather than a query task.

## Step 2: the identifier decision, before anything else

B3 fires on `handles_analytics_identifier`. The question the request
asks is a conversion question, which the identifier ladder in
`packs/data-analytics/refs/PRIVACY_IN_ANALYTICS.md` answers at rung
three: a stable surrogate key. Nothing in the request needs an email
address, so `user_email` does not travel past staging. The staging model
mints `user_key` as a salted hash of the email and drops the email
column. No marts model has a column matching email, name or postcode.

The alternative, copying `user_email` forward because it is a convenient
join key, is the anti-pattern B3 names. It also has no recorded lawful
basis, and D8 gives a cheaper answer for free.

## Step 3: the event taxonomy

Guide `packs/data-analytics/guides/GD-DATA-005-event-contract.md` rules
option C for six events with one engineer: written convention plus an
owned tracking plan, no registry, because the collection path is a CSV
export nobody controls end to end.

The plan file lists the events as object then past-tense action:

```
Signup Started
Signup Completed
Checkout Started
Order Placed
Order Cancelled
Refund Issued
```

No name carries an identifier, a counter, a date or a variant. Variant
membership, order value and currency are properties (D1). The source
dump's raw event strings are mapped onto these six in staging rather
than being renamed in place, so the mapping is reviewable.

## Step 4: the model shape and the grain

Guide `packs/data-analytics/guides/GD-DATA-002-model-shape.md` rules B:
staging one to one with the source, an intermediate model joining
signups to orders, and two marts.

D11 fires before any column is written. The fact model documentation
opens with the grain in words:

> One row per completed checkout order, at the moment the order was
> placed.

That sentence is what makes every later count auditable. A uniqueness
rule on the declared grain goes into the contract in the next step,
which is only possible because the grain was stated first.

## Step 5: the contract, and running it

Guide
`packs/data-analytics/guides/GD-DATA-001-quality-gate-placement.md`
rules A on the published marts, with the metrics of option B deferred
because there is no history yet to compare against. Private staging and
intermediate models carry no contract (D6).

The contract on the order fact carries all five elements from
`packs/data-analytics/refs/DATA_CONTRACT.md`: schema, quality rules,
freshness, owner and support path. The quality rules include
`order_total` not null and within an accepted range, and one row per the
declared grain.

Then the part that matters. D10 says the gate blocks publication, so the
check is a step the build depends on and not a job that runs afterwards.
Run against the shipped data, the pipeline exits non-zero and names the
rule, the column and the offending row count. The seeded null batch does
not reach the marts layer. With the bad batch removed, the same command
exits zero and publishes.

Writing the contract and never running it is the failure mode
`packs/data-analytics/refs/DATA_CONTRACT.md` calls documentation wearing
a gate's clothes. It is worth noticing that this failure looks exactly
like success in a file listing.

## Step 6: the experiment, and what it is allowed to say

B4 fires first. No pre-declared randomisation unit, primary metric or
stopping rule exists in the repository, because nobody wrote one. That
is recorded as a gap rather than papered over. The analysis assumes a
fixed horizon, states that assumption in the answer, and therefore
cannot cite the interim significance point as evidence: under a
fixed-horizon rule the interim point is not a result, and citing it is
the peeking failure named in
`packs/data-analytics/guides/GD-DATA-003-experiment-stopping.md`.

B5 fires next, before any lift is computed. Assignment counts are taken
at the unit level and tested against the declared 50/50 split. The
chi-squared statistic over 200,000 assignments at an observed 52.6 to
47.4 split is far beyond any conventional threshold, and the p-value is
reported with the result.

The check fails. Under B5 the experiment is void. The search order in
`packs/data-analytics/refs/EXPERIMENT_STATS.md` gives the next actions:
inspect bucketing and variant weights, then whether one variant failed
to load, then whether log processing dropped rows unevenly, then
telemetry, then interference from an overlapping test.

## Step 7: the written answer

The answer says, in this order:

1. The sample ratio check failed, with the observed counts, the expected
   counts and the computed p-value.
2. Because it failed, the experiment result is not usable. No lift is
   reported and no winner is declared, in either direction. It is not a
   null result either.
3. The stopping rule assumed was a fixed horizon, stated as an
   assumption because none was declared in advance. The interim
   significance point is therefore not evidence and is not cited as any.
4. What to do next: fix the assignment, re-run, and this time write down
   the randomisation unit, the primary metric and the stopping rule
   before traffic starts.

The tempting sentence, "B looks promising but the check failed", is the
failure this pack exists to stop. There is no "but". A broken assignment
means whatever broke it probably also moved the metric, so "promising"
is not a claim the data supports at any confidence level.

## What fired and where

| Rule | Fired at | Consequence |
| --- | --- | --- |
| B3 | Step 2 | email dropped at staging, surrogate key minted |
| D9 | Step 5 | one contract document with a named owner |
| D10 | Step 5 | pipeline exits non-zero on the shipped data |
| D11 | Step 4 | grain declared in words before columns |
| B4 | Step 6 | missing pre-declaration recorded, assumption stated |
| B5 | Step 6 | check computed, reported, result voided |
| D1 | Step 3 | object-action names, variation in properties |
| D2 | Step 4 | staging, intermediate, marts |
| D5 | Step 4 | one managed warehouse, 200,000 rows |
| D6 | Step 5 | contract on marts only |
| D8 | Step 2 | hashed key rather than natural identifier |

## The three ways this run could have gone wrong

- **Contract written, never run.** Steps 5's first half done and its
  second half skipped. Looks like compliance in a diff.
- **Check computed, win reported anyway.** Step 6 done and step 7's
  second point softened. This is the one the pack was built for.
- **Email carried forward.** Step 2 skipped because the source had the
  column and the join was easy.
