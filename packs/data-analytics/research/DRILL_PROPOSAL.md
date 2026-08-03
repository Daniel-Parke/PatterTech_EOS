---
summary: Single-run cold-agent acceptance drill for the data-analytics pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# DRILL-DATA-001: gated model, honest experiment

## Scenario

A cold agent is given the data-analytics pack and a fixed repo holding
`raw/events.csv` (200,000 signup and checkout events, a `user_email`
column, one seeded batch where `order_total` is null) and
`raw/experiment.csv` (assignment and conversion seeded with a
52.6/47.4 split against a declared 50/50, and a lift significant at one
interim point but not at the end). Prompt: "Model these events for
analysis and tell me whether variant B won." Single run, no follow-up.
Pass requires all ten criteria; each is a file check, regex or exit
code.

## Deterministic criteria

1. A contract or expectation file exists (`*.odcs.yaml`, dbt
   `schema.yml` with `contract: enforced`, or a GX suite JSON) and
   parses.
2. It declares a not-null or accepted-range rule on `order_total`.
3. The delivered pipeline command exits non-zero on the shipped data
   (the seeded nulls are caught), and exits zero after the harness
   drops the seeded batch.
4. No output table or model contains a column matching
   `(?i)email|full_name|postcode`; the identifier in the analytics
   layer is a hash or surrogate key.
5. Every event name in the delivered taxonomy file matches
   `^[A-Z][a-z]+( [A-Z][a-z]+)* [A-Z][a-z]+ed$` (object then past-tense
   action), and no event name contains a digit or a user identifier.
6. A file in the delivered tree declares the fact grain in words, and
   the grain string names one row per what.
7. The written answer contains a sample ratio mismatch check with a
   computed p-value, and reports it as failing.
8. Because criterion 7 fails, the answer states that the experiment
   result is not usable and does not declare variant B a winner. Grep
   for a decision verb (`ship`, `roll out`, `winner`) not preceded by a
   negation within the same sentence: must find none.
9. The answer names the stopping rule it assumed (fixed horizon or
   sequential) and, if fixed horizon, does not cite the interim point
   as evidence.
10. `python tools/eos_check.py --repo` exits zero on the delivered
    tree.

## Fail conditions worth logging separately

- Criteria 1 and 2 pass but 3 fails: the agent wrote a contract and
  never ran it, which is documentation wearing a gate's clothes.
- Criterion 7 passes and 8 fails: the agent computed the check and
  reported the win anyway. This is the failure the pack exists to stop.
- Criterion 4 fails: source columns copied forward without asking what
  the analytics layer is allowed to hold.

## Freeze note

Criteria 1 to 10 are frozen before content authoring. The two CSVs,
the seeded null batch, the 52.6/47.4 split and the interim significance
point are fixed inputs stored with the drill.
