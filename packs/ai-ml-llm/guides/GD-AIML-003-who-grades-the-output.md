---
id: GD-AIML-003
summary: Who grades model output, a deterministic scorer, a human, a validated model judge or the user, and what each can settle
kind: wargame
type: wargame
tags: [data, delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AIML-004, DOC-AIML-006, DOC-AGENT-003, DOC-COD-001]
applies_when: [calls_a_model]
engages_when: [evaluation_oracle_is_undecided]
consequence: high
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0265, EV-0087]
review: 2026-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-AIML-003: Who grades the output?

## Decision question and stakes

An eval is only as good as its scorer. The fork is who or what
produces the score, and the trap is that the cheapest scorer, a model,
is also the one with the most interesting biases. A judge is a
measuring instrument, and an uncalibrated instrument produces numbers
that look exactly like results.

## Doctrines or coverage gap under pressure

- `DOC-AIML-004` (binding): A judge is validated against human labels before its score decides anything.
- `DOC-AIML-006` (default): Grade a sample by hand before writing the rubric.
- `DOC-AGENT-003` (binding): Evaluation is separate from generation, and the evaluator holds external truth.
- `DOC-COD-001` (binding): The oracle that judges a change is authored independently of the implementation under test.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is there one right answer, or a family of acceptable ones?
- Can correctness be checked by code: a label, a number, a schema, a
  compile, a passing test?
- Is the score selecting between candidates, or just monitoring a
  trend? Selection is where bias does the damage.
- Does the grader need domain knowledge the judge model does not have?
- How often will you run it, and what does a run cost?

Applicability is `calls_a_model`. Engagement is `evaluation_oracle_is_undecided`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Deterministic scorer

Code checks the output: exact match, label equality, schema
validation, a unit test, a numeric tolerance. Buys: zero grader
variance, no bias to audit, and a run price near zero. Costs: only
works where correctness is checkable, and it says nothing about
whether a correct answer was well expressed.

### B. Human grader

A person scores against a rubric. Buys: the reference everything else
calibrates against, and the discovery of criteria you could not state
before seeing bad output (EV-0254). Costs: slow, small, and
subject to its own drift, so the labelling protocol has to be written
down and the same person cannot be both author and grader on anything
consequential.

### C. Model judge, validated

A model scores against criteria, after agreement with a human-labelled
sample has been measured and reported. Buys: coverage of open-ended
output at volume, and reference-free metrics that make continuous
measurement affordable (EV-0265). A strong judge reached
roughly eighty per cent agreement with human preference, about the
level two humans reach with each other (EV-0251). Costs:
position bias, verbosity bias, self-preference, and weak reasoning on
tasks needing calculation, all of which have to be measured rather
than assumed away.

### D. User signal

Thumbs, edits, retries, escalations, abandonment. Buys: the only
grader that knows what the user actually wanted, at no labelling cost.
Costs: sparse, biased towards the annoyed, confounded by interface
design, and unusable as a release gate.

## Failure premises

### Premortem for A. Deterministic scorer

Assume `A. Deterministic scorer` was selected and the outcome failed. Test this option's stated failure mechanism first: only works where correctness is checkable, and it says nothing about whether a correct answer was well expressed.

### Premortem for B. Human grader

Assume `B. Human grader` was selected and the outcome failed. Test this option's stated failure mechanism first: slow, small, and subject to its own drift, so the labelling protocol has to be written down and the same person cannot be both author and grader on anything consequential.

### Premortem for C. Model judge, validated

Assume `C. Model judge, validated` was selected and the outcome failed. Test this option's stated failure mechanism first: position bias, verbosity bias, self-preference, and weak reasoning on tasks needing calculation, all of which have to be measured rather than assumed away.

### Premortem for D. User signal

Assume `D. User signal` was selected and the outcome failed. Test this option's stated failure mechanism first: sparse, biased towards the annoyed, confounded by interface design, and unusable as a release gate.

## Decision rule

- Correctness is checkable by code: A. Do not reach for a judge
  because it feels more sophisticated.
- Output is open-ended: C, but only after B has produced the labels C
  is validated against, with the agreement number reported beside
  every result that judge produces.
- The score selects between candidates: the judge is never the same
  model as the one under test, and pairwise protocols run both
  orderings with order-inconsistent pairs reported as disagreement
  (EV-0252, EV-0253).
- A family-mate judge is unavoidable: report the self-preference
  offset measured on the human-labelled sample.
- The property is a safety property: B, and no judge score substitutes
  for it. Eighty per cent agreement is far too coarse for that job.
- D always, as a source of new eval items, never as a gate.

## Safe default

A where possible, C where not, B as the calibration underneath both.
Mix code graders, model graders and human transcript review rather
than picking one (EV-0087).

## Cheapest discriminating test

Calibrate each proposed judge against the same human-labelled sample. Report agreement, disagreement, order effects, abstention and cost before allowing any judge to decide the claimed behaviour.

## Fallback, exit and revisit

**Fallback `safe-default`:** A where possible, C where not, B as the calibration underneath both. Mix code graders, model graders and human transcript review rather than picking one (EV-0087).

**Exit condition:** Stop or roll back the selected branch when only works where correctness is checkable, and it says nothing about whether a correct answer was well expressed, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is there one right answer, or a family of acceptable ones?

## Counter-evidence and transfer limits

### Evidence boundary

The eighty per cent agreement figure is general chat preference on
retired models, not domain correctness, and it should never be
borrowed for a domain judge without measuring your own agreement
(EV-0251). Position bias results are pairwise only, so they
do not directly govern single-answer rubric scoring, which carries its
own biases. Self-preference was measured on summarisation with three
superseded models, and follow-up work argues some of the effect
reflects genuine quality differences human raters under-detect, so the
correction direction is contested even where the direction of the bias
is not.
### Preserved reasoning: Scoring abstention

Whatever the grader, the rubric gives explicit credit for a calibrated
refusal and the report carries the abstention rate beside accuracy. A
rubric that pays a guess the same as an admission of uncertainty
selects for confident error (EV-0250). Two numbers move
together: pushing abstention up buys fewer wrong answers and a system
that refuses more work, so the pair is watched, never one alone. The
evidence does not tell you where the threshold belongs, and the
product decides that.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
