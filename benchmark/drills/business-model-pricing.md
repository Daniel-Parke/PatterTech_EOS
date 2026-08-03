---
summary: Single-run cold-agent acceptance drill for the business model and pricing pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# DRILL-BMP-001: a priced offer that survives the law and the maths

## Scenario

A cold agent gets the pack and a repo holding `inputs/costs.csv`
(twelve months of unit costs), `inputs/cohorts.csv` (eighteen monthly
signup cohorts with retained counts) and `inputs/brief.md` naming a UK
consumer subscription product. One prompt: "Produce the pricing
decision: the offer, the tiers, the price, the evidence behind it, and
the finance and legal obligations it creates. Write machine-readable
outputs where the pack asks for them."

Single run, no follow-ups. Pass needs all ten criteria, each a file
check, a schema check or an exit code.

## Deterministic criteria

1. `pricing/decision.json` exists and parses.
2. It validates against the pack's pricing decision schema, with a
   `practice` field of `value-informed`, `competition-informed` or
   `cost-informed` and a non-empty `condition` justifying it.
3. It contains `headline_price_includes` listing every unavoidable
   charge, and no entry in `optional_charges` is marked
   `mandatory: true`.
4. `pricing/retention.csv` exists with one row per cohort age, and
   projected retention is non-decreasing in cohort age (the sorting
   effect; a flat blended-churn projection fails).
5. The lifetime value in `decision.json` is not within one per cent of
   `arpu / blended_churn` computed from the inputs.
6. Every metric named in `decision.json` appears in
   `pricing/definitions.md` with a formula; the name diff is empty.
7. `pricing/obligations.md` contains `VAT`, `Making Tax Digital`,
   `cooling-off` and `renewal reminder`.
8. `pricing/obligations.md` states 30 days as the commercial default
   payment term.
9. `pricing/evidence.md` cites at least three fragment or EV ids and
   every cited id resolves in the ledger.
10. The harness injects a fifteen per cent unit cost rise and re-runs
    the agent's own repricing script; it exits 0 and emits a new price
    with a stated cause of type `cost`.

## Fail conditions worth logging separately

- Criterion 5 fails: the pack taught the lifetime value formula that
  the evidence says is wrong.
- Criterion 3 fails: the pack failed to carry the drip pricing ban.
- Criterion 10 emits a price rise with cause `demand`: the pack failed
  to carry the dual entitlement rule.
- A fixed trial length appears with no test plan: the pack taught a
  number where the evidence supports only a measurement rule.

## Freeze note

Criteria 1 to 10 are frozen before content authoring. The three input
files, the injected cost rise in criterion 10 and the schema used in
criterion 2 are fixed inputs stored with the drill.
