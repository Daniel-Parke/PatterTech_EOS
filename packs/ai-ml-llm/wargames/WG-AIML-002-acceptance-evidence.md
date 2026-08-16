---
id: WG-AIML-002
summary: What evidence accepts or refuses a change to a model-backed feature, offline set, judge, human sample or production telemetry?
kind: wargame
type: wargame
tags: [data, delivery, eos, testing, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-AIML-005]
applies_when: [calls_a_model]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0242, EV-0254, EV-0255, EV-0257, EV-0258, EV-0267, EV-0087]
review: 2026-11
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-AIML-002: What evidence accepts this change?

## Decision question and stakes

Someone wants to change the prompt, the model, the retriever or the
decoding settings, and they believe the new one is better. Something
has to decide whether that belief survives contact with measurement,
and it has to exist before the change is proposed. The fork is which
kind of evidence you build, and what it can and cannot settle.

## Doctrines or coverage gap under pressure

- `DOC-AIML-005` (binding): Consequential model output is reviewed by a person before it takes effect.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can you state the acceptance condition as a score on items you can
  collect? A classifier can. An open-ended assistant reply is harder.
- Do you have labels, and who made them?
- Is the difference you care about large, or is it a few points?
- Does the failure you fear appear in your sample at all, or does it
  only appear in live traffic with a live corpus?
- Does the change touch a consequential action class, where the answer
  is not a score at all but an approval floor?

Applicability is `calls_a_model`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Offline set with statistics

A fixed set of items with known answers, scored headlessly, reported
with an item count, an interval or standard error, and the template
hash and model id attached. Comparisons are paired over the same items
and carry a stated minimum detectable effect. Buys: a repeatable
verdict that can refuse a change, and the power gain that paired
differences give by removing item-difficulty variance
(EV-0255). Costs: it can only measure what you thought to
collect, and the set ages as the product moves.

### B. Model judge over a rubric

A model grades output against written criteria, cheaply and at volume.
Buys: coverage of open-ended output where no gold answer exists, and
reference-free continuous measurement. Costs: the judge is an
instrument with its own error, and it is worthless until validated
against human labels. See
`packs/ai-ml-llm/wargames/WG-AIML-004-who-grades-the-output.md`.

### C. Human-labelled sample

A person grades a sample, and the labels become the reference
everything else is calibrated against. Buys: the only ground truth in
the building, and the discovery of criteria you could not state in
advance, which is how rubrics actually get written
(EV-0254). Costs: slow, small, and expensive per item, so it
cannot be the routine gate.

### D. Production telemetry and online experiment

Measure the live system: failure reports, abstention rate, escalation
rate, groundedness sampling, and an experiment where traffic allows
one. Buys: the failure classes an offline set cannot contain, since
RAG failure distribution depends on the live corpus and live queries
(EV-0242). Costs: it discovers a regression after users met
it, and most ventures have too little traffic for a powered
experiment.

## Failure premises

### Premortem for A. Offline set with statistics

Assume `A. Offline set with statistics` was selected and the outcome failed. Test this option's stated failure mechanism first: it can only measure what you thought to collect, and the set ages as the product moves.

### Premortem for B. Model judge over a rubric

Assume `B. Model judge over a rubric` was selected and the outcome failed. Test this option's stated failure mechanism first: the judge is an instrument with its own error, and it is worthless until validated against human labels. See `packs/ai-ml-llm/wargames/WG-AIML-004-who-grades-the-output.md`.

### Premortem for C. Human-labelled sample

Assume `C. Human-labelled sample` was selected and the outcome failed. Test this option's stated failure mechanism first: slow, small, and expensive per item, so it cannot be the routine gate.

### Premortem for D. Production telemetry and online experiment

Assume `D. Production telemetry and online experiment` was selected and the outcome failed. Test this option's stated failure mechanism first: it discovers a regression after users met it, and most ventures have too little traffic for a powered experiment.

## Decision rule

- Any change to prompt, model, retriever or decoding: A, always, and
  A is what accepts or refuses the change.
- Output is open-ended and no gold answer exists: B on top of A, with
  C as the calibration sample B is validated against.
- No rubric exists yet: C first, on a few dozen outputs, then derive
  the assertions from those grades (EV-0254).
- Live system with real traffic: D continuously, feeding new items
  back into A. Offline evidence gates change, production telemetry
  discovers the next failure class.
- The change touches a consequential action class: B7 in the pack
  applies and no score substitutes for the approval.

## Safe default

A, with C supplying the labels and B extending coverage once
validated. Start at twenty to fifty tasks harvested from real failures
rather than waiting for a large clean set (EV-0087), and grow the set
every time production surprises you.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can you state the acceptance condition as a score on items you can collect? A classifier can. An open-ended assistant reply is harder.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with C supplying the labels and B extending coverage once validated. Start at twenty to fifty tasks harvested from real failures rather than waiting for a large clean set (EV-0087), and grow the set every time production surprises you.

**Exit condition:** Stop or roll back the selected branch when it can only measure what you thought to collect, and the set ages as the product moves, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can you state the acceptance condition as a score on items you can collect? A classifier can. An open-ended assistant reply is harder.

## Counter-evidence and transfer limits

### Evidence boundary

EV-0255 assumes roughly independent items and a scalar
score, which fits pass-fail grading better than open-ended rubric
scoring or agent trajectories where the unit of observation is
ambiguous, and it does not model judge error, so intervals from that
method alone are too narrow when a model does the grading. The
contamination figure is grade-school arithmetic on retired models. Use
the method, not the numbers.
### Preserved reasoning: The private set rule

The acceptance set is private and the tuning path never reads it.
Public benchmark scores are partly a memorisation artefact, with drops
of up to eight points on a fresh matched set (EV-0257), and
a public scoreboard distorts under optimisation pressure
(EV-0258). The public practice set and private official set
split of a published safety benchmark is the same design choice
applied to harm (EV-0267). Practically: two files, one the
selection path may read, one it may not, and a check that greps the
selection code for the held-out filename.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
