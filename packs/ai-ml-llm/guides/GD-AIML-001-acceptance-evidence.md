---
summary: What evidence accepts or refuses a change to a model-backed feature, offline set, judge, human sample or production telemetry?
type: guide
tags: [testing, delivery, data]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [FRAG-AI-ML-LLM-01, FRAG-AI-ML-LLM-13, FRAG-AI-ML-LLM-14, FRAG-AI-ML-LLM-16, FRAG-AI-ML-LLM-17, FRAG-AI-ML-LLM-26, EV-0087]
review: 2026-11
review_by: 2026-11
---

# GD-AIML-001: What evidence accepts this change?

## The question

Someone wants to change the prompt, the model, the retriever or the
decoding settings, and they believe the new one is better. Something
has to decide whether that belief survives contact with measurement,
and it has to exist before the change is proposed. The fork is which
kind of evidence you build, and what it can and cannot settle.

## It depends on

- Can you state the acceptance condition as a score on items you can
  collect? A classifier can. An open-ended assistant reply is harder.
- Do you have labels, and who made them?
- Is the difference you care about large, or is it a few points?
- Does the failure you fear appear in your sample at all, or does it
  only appear in live traffic with a live corpus?
- Does the change touch a consequential action class, where the answer
  is not a score at all but an approval floor?

## Options

### A. Offline set with statistics

A fixed set of items with known answers, scored headlessly, reported
with an item count, an interval or standard error, and the template
hash and model id attached. Comparisons are paired over the same items
and carry a stated minimum detectable effect. Buys: a repeatable
verdict that can refuse a change, and the power gain that paired
differences give by removing item-difficulty variance
(FRAG-AI-ML-LLM-14). Costs: it can only measure what you thought to
collect, and the set ages as the product moves.

### B. Model judge over a rubric

A model grades output against written criteria, cheaply and at volume.
Buys: coverage of open-ended output where no gold answer exists, and
reference-free continuous measurement. Costs: the judge is an
instrument with its own error, and it is worthless until validated
against human labels. See
`packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md`.

### C. Human-labelled sample

A person grades a sample, and the labels become the reference
everything else is calibrated against. Buys: the only ground truth in
the building, and the discovery of criteria you could not state in
advance, which is how rubrics actually get written
(FRAG-AI-ML-LLM-13). Costs: slow, small, and expensive per item, so it
cannot be the routine gate.

### D. Production telemetry and online experiment

Measure the live system: failure reports, abstention rate, escalation
rate, groundedness sampling, and an experiment where traffic allows
one. Buys: the failure classes an offline set cannot contain, since
RAG failure distribution depends on the live corpus and live queries
(FRAG-AI-ML-LLM-01). Costs: it discovers a regression after users met
it, and most ventures have too little traffic for a powered
experiment.

## Decision rule

- Any change to prompt, model, retriever or decoding: A, always, and
  A is what accepts or refuses the change.
- Output is open-ended and no gold answer exists: B on top of A, with
  C as the calibration sample B is validated against.
- No rubric exists yet: C first, on a few dozen outputs, then derive
  the assertions from those grades (FRAG-AI-ML-LLM-13).
- Live system with real traffic: D continuously, feeding new items
  back into A. Offline evidence gates change, production telemetry
  discovers the next failure class.
- The change touches a consequential action class: B7 in the pack
  applies and no score substitutes for the approval.

## Default

A, with C supplying the labels and B extending coverage once
validated. Start at twenty to fifty tasks harvested from real failures
rather than waiting for a large clean set (EV-0087), and grow the set
every time production surprises you.

## The private set rule

The acceptance set is private and the tuning path never reads it.
Public benchmark scores are partly a memorisation artefact, with drops
of up to eight points on a fresh matched set (FRAG-AI-ML-LLM-16), and
a public scoreboard distorts under optimisation pressure
(FRAG-AI-ML-LLM-17). The public practice set and private official set
split of a published safety benchmark is the same design choice
applied to harm (FRAG-AI-ML-LLM-26). Practically: two files, one the
selection path may read, one it may not, and a check that greps the
selection code for the held-out filename.

## Evidence boundary

FRAG-AI-ML-LLM-14 assumes roughly independent items and a scalar
score, which fits pass-fail grading better than open-ended rubric
scoring or agent trajectories where the unit of observation is
ambiguous, and it does not model judge error, so intervals from that
method alone are too narrow when a model does the grading. The
contamination figure is grade-school arithmetic on retired models. Use
the method, not the numbers.

## Worked rulings

- **PatterTech EOS ai-ml-llm pack (2026-08, argued)**: A as the
  binding acceptance path, C as the label source, B permitted only
  after validation, D as a standing obligation rather than a gate.
  Argued from FRAG-AI-ML-LLM-14 for the statistics and
  FRAG-AI-ML-LLM-16 for the private set.
- **Support ticket classifier prompt swap (2026-08, argued)**: A, with
  the verdict on a three-point gap recorded as unresolved rather than
  as a win. Worked in full at
  `packs/ai-ml-llm/exemplars/EX-AIML-001-classifier-prompt-swap.md`.
- **Free-text summary quality (2026-08, inherited)**: C then B,
  inherited from the criteria-drift finding: nobody could write the
  rubric until they had read thirty bad summaries.
