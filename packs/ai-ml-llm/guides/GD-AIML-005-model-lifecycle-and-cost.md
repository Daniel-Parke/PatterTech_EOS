---
summary: Which model backs this feature and what happens when it retires, one pinned model, a cascade, self-assessed routing or a portfolio?
type: guide
tags: [perf, delivery, ops]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [FRAG-AI-ML-LLM-04, FRAG-AI-ML-LLM-17, FRAG-AI-ML-LLM-18, FRAG-AI-ML-LLM-19, FRAG-AI-ML-LLM-20, FRAG-AI-ML-LLM-21, FRAG-AI-ML-LLM-27]
review: 2027-03
review_by: 2027-03
---

# GD-AIML-005: Which model, and what happens when it goes?

## The question

The component at the centre of the product is a dependency you do not
control, whose behaviour moves inside its own name and whose end date
is published by somebody else. The fork is how many models you run,
how requests are routed between them, and what the migration looks
like when the clock runs out.

## It depends on

- Is the quality difference between the cheap and the expensive model
  visible on your own set, or only on public benchmarks?
- What does the feature cost per thousand calls today, and does that
  number matter yet?
- Is latency part of the product, or is it a background job?
- How much evaluation would a migration have to re-run?
- How many providers are you willing to hold open, given each carries
  its own retirement clock?

## Options

### A. One pinned model

A single dated model id for the task. Buys: one thing to evaluate, one
migration to plan, and behaviour you can reason about. Costs: you pay
frontier prices for trivial requests, and one retirement date moves
the whole feature.

### B. Trained cascade

Try the cheap model, score its answer with a learned confidence
function, escalate on low confidence. Buys: a large cost saving in the
reported settings, up to 98 per cent at matched accuracy
(FRAG-AI-ML-LLM-21). Costs: a trained scorer, labelled data to train
it, added latency on escalated queries, and a second failure mode when
the scorer is wrong.

### C. Self-assessed routing

Ask the model whether what it has is enough, and escalate when it says
no (FRAG-AI-ML-LLM-04). Buys: comparable routing benefit with no
trained scorer, and an escalation rate you can watch. Costs: the
router inherits the model's own calibration problems, so the
escalation rate has to be validated against outcomes rather than
trusted.

### D. Portfolio by task

Different models for different tasks, chosen per task on your own
evaluation. Buys: the right instrument per job, and provider
concentration risk spread. Costs: several evaluation suites, several
retirement clocks, and prompts that do not transfer between families.

## Decision rule

- Under every option: dated model ids only, never a moving alias, with
  the published retirement date recorded next to the call site
  (FRAG-AI-ML-LLM-19).
- Default to A until the cost line is a number somebody complains
  about.
- Cost matters and you have no labels for a scorer: C.
- Cost matters, labels exist, and the volume justifies the machinery:
  B.
- The tasks genuinely differ in difficulty and the suites are already
  separate: D.
- Before adopting any cost machinery, take the cheap levers first:
  prompt caching with the hit rate asserted in telemetry
  (FRAG-AI-ML-LLM-20), shorter contexts, fewer demonstrations.
- Never choose a model from a leaderboard position alone. Public
  ranking is a shortlist generator (FRAG-AI-ML-LLM-17).

## Default

A, with a stable-prefix-first prompt layout and cache hit rate
asserted, escalating to C when the cost line matters. Caching and
context discipline capture part of the saving a cascade promises, with
far less machinery to maintain.

## The migration drill

A model retirement is a scheduled outage you have been warned about.
Sixty days is the published notice floor, tentative retirement dates
sit a year or more out, and a usage export exists so you can audit
which keys still call a deprecated model (FRAG-AI-ML-LLM-19). The drill
is in `packs/ai-ml-llm/refs/MODEL_MIGRATION.md`. Behaviour also moves
inside a name's lifetime, with one task falling from 84 per cent to 51
per cent between two snapshots of the same endpoint
(FRAG-AI-ML-LLM-18), so the regression suite runs on a schedule and
not only at migration.

## Evidence boundary

The cascade savings figure is dataset-specific on a 2023 model
line-up and 2023 tariffs, and it predates prompt caching and batch
pricing, which now capture part of the same saving. This is the
weakest-evidenced area in the pack, which is why none of it binds.
FRAG-AI-ML-LLM-19 is one vendor's published policy, and platform
resellers set their own schedules, so a multi-cloud deployment carries
several clocks. The drift study is two snapshots of one vendor in
2023, and its arithmetic result is contested as partly a formatting
artefact.

## Provenance record

The model your product depends on carries a provenance row alongside
its pin: provider, dated id, published retirement date, documented
capability limits, and the model documentation the provider publishes
under the transparency obligations that now apply to general-purpose
model providers in the EU (FRAG-AI-ML-LLM-27). That belongs in the
dependency record, not in a compliance folder opened once a year.

## Worked rulings

- **PatterTech EOS ai-ml-llm pack (2026-08, argued)**: A as default,
  pinning binding, cost machinery held at preference because the
  evidence is three years old.
- **Ticket classifier (2026-08, argued)**: A. Volume is small, the
  cost line is not yet a number anybody notices, and a cascade would
  add a second failure mode for no measured gain.
- **Bulk document summarisation (2026-08, inherited)**: C, inherited
  from the Self-Route result, with the escalation rate reported weekly
  and the sample audited against outcomes.
