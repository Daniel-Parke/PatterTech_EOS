---
summary: The artefacts a pricing decision has to emit, the decision record schema, and what each field is for
type: foundation
tags: [money, product]
kind: fact
scope: estate
sources: [EV-0288, EV-0297, EV-0299, EV-0301]
volatility: slow
review: 2026-12
---

# The pricing decision record

Level three material behind the whole pack. Read this when producing a
pricing decision, and when checking one.

A pricing decision is not finished when a number exists. It is finished
when the number, the practice behind it, the obligations it creates and
the evidence for it are all written where a machine and a stranger can
read them.

## The five artefacts

A pricing decision emits five files, under a pricing directory in the
venture repository.

| File | Holds | Checked by |
| --- | --- | --- |
| decision.json | The decision itself, machine-readable, to the schema below | C-01, C-02, C-03, C-05, C-13, C-14 |
| retention.csv | One row per cohort age, observed and projected | C-04 |
| definitions.md | Every metric named anywhere in the decision, with its formula | C-06 |
| obligations.md | The legal, tax and payment duties this price creates | C-07, C-08 |
| evidence.md | The evidence cited, by EV id from `registry/evidence.json` | C-09 |

A repricing script sits beside them and is executable, because the
repricing trigger has to be runnable rather than remembered. See
`packs/business-model-pricing/wargames/WG-BMP-004-repricing-trigger.md`.

## The decision record schema

The schema is a file, not a listing, so a validator can be pointed at
it: `packs/business-model-pricing/references/pricing-decision.schema.json`.
Draft 2020-12. What it requires, in one table.

| Field | Shape | Why it is required |
| --- | --- | --- |
| offer | non-empty string | The thing being sold, named |
| practice | value-informed, competition-informed or cost-informed | The anchor, per WG-BMP-001 |
| condition | non-empty string | What makes that anchor right here |
| revisit_date | YYYY-MM | When the practice is re-argued |
| currency, headline_price | ISO code, number above zero | The number itself |
| headline_price_includes | non-empty array of strings | The unavoidable set, per B1 |
| optional_charges | objects with name, mandatory false, avoidable_how | Every optional charge says how it is declined |
| tiers | array of name and price | Whatever packaging exists, including one tier |
| unit_of_charge | flat-period, per-seat, metered or outcome-share | Per WG-BMP-002 |
| unit_cost_allocated | number at or above zero | The FinOps allocation, per D7 |
| reporting_framework | IFRS, FRS102, FRS105 or ASC606 | Recognition rules differ, per B4 |
| payment_terms | days from 1 to 60, and a basis | Per D9 |
| metrics | non-empty array of names | Each must appear in definitions.md |
| lifetime_value | value and a method name | Per D4 |
| trial | days and a test_plan, where a trial exists | Per D3 |
| repricing_trigger | type, threshold and cause_types | Per D8 |
| price_changes | date, from, to, cause and cause_type | The history, one row per change |
| evidence | at least three ids | Per the pack's evidence pointer |

## Why each awkward field is there

- **practice and condition together.** The three practices pay off under
  different conditions, so a practice with no condition beside it is not
  a decision anyone can argue with later
  (EV-0288).
- **headline_price_includes and optional_charges.** The unavoidable set
  has to be in the advertised number, and the optional set has to state
  how it is avoided, because that boundary is where disputes sit
  (EV-0299). A charge marked mandatory in the
  optional list is a schema failure by construction.
- **cause_types limited to cost and value.** A demand cause is refused
  at the schema level. See
  `packs/business-model-pricing/wargames/WG-BMP-004-repricing-trigger.md`.
- **lifetime_value.method.** Naming the method forces the cohort
  question into the open. See
  `packs/business-model-pricing/references/RETENTION_AND_LTV.md`.
- **reporting_framework.** The recognition rules differ, and the bundle
  decomposition has to be defensible under whichever one applies
  (EV-0297).
- **payment_terms.days capped at sixty.** Longer is possible between
  businesses only where it is fair to both, which is a judgement a
  schema should not wave through (EV-0301).
