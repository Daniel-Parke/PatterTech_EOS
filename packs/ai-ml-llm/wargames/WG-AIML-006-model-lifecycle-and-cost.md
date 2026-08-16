---
id: WG-AIML-006
summary: Which model backs this feature and what happens when it retires, one pinned model, a cascade, self-assessed routing or a portfolio?
kind: wargame
type: wargame
tags: [delivery, eos, ops, perf, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AIML-003, DOC-AIML-017]
applies_when: [calls_a_model]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0245, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262, EV-0268]
review: 2027-03
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-AIML-006: Which model, and what happens when it goes?

## Decision question and stakes

The component at the centre of the product is a dependency you do not
control, whose behaviour moves inside its own name and whose end date
is published by somebody else. The fork is how many models you run,
how requests are routed between them, and what the migration looks
like when the clock runs out.

## Doctrines or coverage gap under pressure

- `DOC-AIML-003` (binding): Model identifiers are pinned to a version the provider has undertaken not to move, with the retirement date recorded beside the call site.
- `DOC-AIML-017` (preference): Trained cascade routing against model self-assessment routing.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the quality difference between the cheap and the expensive model
  visible on your own set, or only on public benchmarks?
- What does the feature cost per thousand calls today, and does that
  number matter yet?
- Is latency part of the product, or is it a background job?
- How much evaluation would a migration have to re-run?
- How many providers are you willing to hold open, given each carries
  its own retirement clock?

Applicability is `calls_a_model`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. One pinned model

A single pinned model id for the task. Buys: one thing to evaluate, one
migration to plan, and behaviour you can reason about. Costs: you pay
frontier prices for trivial requests, and one retirement date moves
the whole feature.

### B. Trained cascade

Try the cheap model, score its answer with a learned confidence
function, escalate on low confidence. Buys: a large cost saving in the
reported settings, up to 98 per cent at matched accuracy
(EV-0262). Costs: a trained scorer, labelled data to train
it, added latency on escalated queries, and a second failure mode when
the scorer is wrong.

### C. Self-assessed routing

Ask the model whether what it has is enough, and escalate when it says
no (EV-0245). Buys: comparable routing benefit with no
trained scorer, and an escalation rate you can watch. Costs: the
router inherits the model's own calibration problems, so the
escalation rate has to be validated against outcomes rather than
trusted.

### D. Portfolio by task

Different models for different tasks, chosen per task on your own
evaluation. Buys: the right instrument per job, and provider
concentration risk spread. Costs: several evaluation suites, several
retirement clocks, and prompts that do not transfer between families.

## Failure premises

### Premortem for A. One pinned model

Assume `A. One pinned model` was selected and the outcome failed. Test this option's stated failure mechanism first: you pay frontier prices for trivial requests, and one retirement date moves the whole feature.

### Premortem for B. Trained cascade

Assume `B. Trained cascade` was selected and the outcome failed. Test this option's stated failure mechanism first: saving in the reported settings, up to 98 per cent at matched accuracy (EV-0262). Costs: a trained scorer, labelled data to train it, added latency on escalated queries, and a second failure mode when the scorer is wrong.

### Premortem for C. Self-assessed routing

Assume `C. Self-assessed routing` was selected and the outcome failed. Test this option's stated failure mechanism first: the router inherits the model's own calibration problems, so the escalation rate has to be validated against outcomes rather than trusted.

### Premortem for D. Portfolio by task

Assume `D. Portfolio by task` was selected and the outcome failed. Test this option's stated failure mechanism first: several evaluation suites, several retirement clocks, and prompts that do not transfer between families.

## Decision rule

- Under every option: pinned model ids only, never a moving alias,
  with the published retirement date recorded next to the call site
  (EV-0260). Pinned means the id keeps resolving to the same
  weights. Read the provider's scheme rather than looking for a date:
  a dated snapshot and an undated version-numbered id can both be
  pinned, and at least one major vendor's current ids carry no date.
- Default to A until the cost line is a number somebody complains
  about.
- Cost matters and you have no labels for a scorer: C.
- Cost matters, labels exist, and the volume justifies the machinery:
  B.
- The tasks genuinely differ in difficulty and the suites are already
  separate: D.
- Before adopting any cost machinery, take the cheap levers first:
  prompt caching with the hit rate asserted in telemetry
  (EV-0261), shorter contexts, fewer demonstrations.
- Never choose a model from a leaderboard position alone. Public
  ranking is a shortlist generator (EV-0258).

## Safe default

A, with a stable-prefix-first prompt layout and cache hit rate
asserted, escalating to C when the cost line matters. Caching and
context discipline capture part of the saving a cascade promises, with
far less machinery to maintain.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is the quality difference between the cheap and the expensive model visible on your own set, or only on public benchmarks?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with a stable-prefix-first prompt layout and cache hit rate asserted, escalating to C when the cost line matters. Caching and context discipline capture part of the saving a cascade promises, with far less machinery to maintain.

**Exit condition:** Stop or roll back the selected branch when you pay frontier prices for trivial requests, and one retirement date moves the whole feature, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the quality difference between the cheap and the expensive model visible on your own set, or only on public benchmarks?

## Counter-evidence and transfer limits

### Evidence boundary

The cascade savings figure is dataset-specific on a 2023 model
line-up and 2023 tariffs, and it predates prompt caching and batch
pricing, which now capture part of the same saving. This is the
weakest-evidenced area in the pack, which is why none of it binds.
EV-0260 is one vendor's published policy, and platform
resellers set their own schedules, so a multi-cloud deployment carries
several clocks. The drift study is two snapshots of one vendor in
2023, and its arithmetic result is contested as partly a formatting
artefact.
### Preserved reasoning: The migration drill

A model retirement is a scheduled outage you have been warned about.
Sixty days is the published notice floor, tentative retirement dates
sit a year or more out, and a usage export exists so you can audit
which keys still call a deprecated model (EV-0260). The drill
is in `packs/ai-ml-llm/references/MODEL_MIGRATION.md`. Behaviour also moves
inside a name's lifetime, with one task falling from 84 per cent to 51
per cent between two snapshots of the same endpoint
(EV-0259), so the regression suite runs on a schedule and
not only at migration.
### Preserved reasoning: Provenance record

The model your product depends on carries a provenance row alongside
its pin: provider, pinned id, published retirement date, documented
capability limits, and the model documentation the provider publishes
under the transparency obligations that now apply to general-purpose
model providers in the EU (EV-0268). That belongs in the
dependency record, not in a compliance folder opened once a year.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
