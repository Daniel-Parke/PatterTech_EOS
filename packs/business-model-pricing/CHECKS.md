---
summary: What a reviewer or a script can verify about a pricing decision, split into executable today and judgement
type: checks
tags: [money, product, ci]
kind: record
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0296, EV-0297, EV-0299, EV-0300, EV-0301]
review: 2028-05
---

# business-model-pricing pack checks

The evaluation criteria for work under
`packs/business-model-pricing/PACK.md`. Each row names what is verified,
how, and whether a machine can do it today. A check that needs a person
is still a check.

The artefacts these run against are the five files and the repricing
script in `packs/business-model-pricing/references/DECISION_RECORD.md`.

## Executable today

These run against the pricing artefacts in the venture repository and
need no human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | The decision exists and parses | decision.json loads as JSON | B4, D1 |
| C-02 | A practice is named with a condition | Validate decision.json against `packs/business-model-pricing/references/pricing-decision.schema.json`: practice is one of the three enum values and condition is a non-empty string | D1 |
| C-03 | The headline price is complete | headline_price_includes is non-empty and no entry in optional_charges has mandatory true | B1 |
| C-04 | Retention is a curve | retention.csv has one row per cohort age; the projected retention_rate column is non-decreasing in cohort age, and survivor_share is non-increasing | D4 |
| C-05 | Lifetime value did not come from blended churn | Recompute average revenue per account over blended churn from the inputs; the reported lifetime value must not land within one per cent of it | D4 |
| C-06 | Every metric is defined | The set of metric names in decision.json minus the names defined in definitions.md is empty, and every definition carries a formula | D5 |
| C-07 | Obligations are named | obligations.md contains VAT, Making Tax Digital, cooling-off and renewal reminder | B2, B5 |
| C-08 | Payment terms are stated | obligations.md states 30 days as the commercial default, in numerals, and payment_terms.days is at most 60 | D9 |
| C-09 | Evidence resolves | evidence.md cites at least three EV ids and every cited id resolves in `registry/evidence.json` | Whole pack |
| C-10 | The repricing trigger runs | Inject a unit cost rise above the trigger band, run the venture's repricing script; it exits zero and emits a new price with a cause of type cost | D8 |
| C-11 | Unit cost is allocated | unit_cost_allocated is present and above zero for every charged unit | D7 |
| C-12 | A trial number carries a test plan | If trial.days is present and above zero, trial.test_plan is a non-empty reference | D3 |
| C-13 | The reporting framework is declared | reporting_framework is one of the four enum values | B4 |
| C-14 | The revisit date exists and is in the future | revisit_date parses as a month and is later than the decision date | D1 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The condition justifying the practice is actually true of this venture | Reviewer | D1 |
| J-02 | The unavoidable and optional split is honest, and each optional charge really is declinable | Reviewer, because the boundary is where enforcement disputes sit (EV-0299) | B1 |
| J-03 | The value case is quantified for a named segment, where the practice is value-informed | Reviewer | D1 |
| J-04 | The stated cause of a price change is the real cause | Reviewer, because a schema can refuse a demand label and cannot detect a demand motive | D2 |
| J-05 | No pattern from the almost-always-harmful list appears in the pricing or checkout flow | Reviewer, walking the flow (EV-0300) | D10 |
| J-06 | The metered unit is one the buyer can forecast and control | Reviewer | WG-BMP-002 |
| J-07 | The bundle decomposes into distinct performance obligations with defensible stand-alone selling prices under the declared framework | Reviewer, or an accountant (EV-0297) | B4 |
| J-08 | A survey-derived number was treated as a bracket rather than a decision | Reviewer | D6 |
| J-09 | An agreed payment term longer than thirty days is fair to both parties | Reviewer (EV-0301) | D9 |
| J-10 | The cancellation route works, end to end, without contacting anyone | Person, doing it | B2 |
| J-11 | The trial test plan reads out all three funnel stages | Reviewer | D3 |

## How to read a failing check

C-01 to C-03 and C-07 to C-09 are the legal and evidential floor and
carry no override. C-04, C-05, C-06, C-11 and C-12 sit under defaults,
so a venture may override them with a recorded lock-book reason; the
override is recorded, the check still runs, and it still reports.

Three failures are worth logging separately because each says the pack
itself failed rather than the work.

- C-05 failing means the lifetime value formula the evidence rejects was
  taught anyway.
- C-03 failing means the drip pricing ban was not carried.
- C-10 emitting a price rise with a demand cause means the dual
  entitlement rule was not carried.

A J-row that nobody performed is a J-row that failed.

## Wiring note

C-05, C-10 and C-11 are the three a venture has to configure before this
pack has teeth, because each needs the venture's own inputs: the cohort
and revenue files for C-05, an executable repricing script for C-10, and
a FinOps cost allocation for C-11. The rest are schema and text checks
that run from the artefacts alone.

## What this pack deliberately does not check

- Whether the price is right. No check in this pack can tell you that,
  and any that claimed to would be lying.
- Tier count, tier names or price endings. Preferences, per the pack.
- Conversion rate against any benchmark. The benchmarks in circulation
  for usage-based pricing come from vendor surveys and are refused.
- Anything an accountant should be looking at. C-13 records the
  framework; it does not audit against it.
