---
summary: Who grades model output, a deterministic scorer, a human, a validated model judge or the user, and what each can settle
type: guide
tags: [testing, delivery, data]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0265, EV-0087]
review: 2026-12
---

# GD-AIML-003: Who grades the output?

## The question

An eval is only as good as its scorer. The fork is who or what
produces the score, and the trap is that the cheapest scorer, a model,
is also the one with the most interesting biases. A judge is a
measuring instrument, and an uncalibrated instrument produces numbers
that look exactly like results.

## It depends on

- Is there one right answer, or a family of acceptable ones?
- Can correctness be checked by code: a label, a number, a schema, a
  compile, a passing test?
- Is the score selecting between candidates, or just monitoring a
  trend? Selection is where bias does the damage.
- Does the grader need domain knowledge the judge model does not have?
- How often will you run it, and what does a run cost?

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

## Default

A where possible, C where not, B as the calibration underneath both.
Mix code graders, model graders and human transcript review rather
than picking one (EV-0087).

## Scoring abstention

Whatever the grader, the rubric gives explicit credit for a calibrated
refusal and the report carries the abstention rate beside accuracy. A
rubric that pays a guess the same as an admission of uncertainty
selects for confident error (EV-0250). Two numbers move
together: pushing abstention up buys fewer wrong answers and a system
that refuses more work, so the pair is watched, never one alone. The
evidence does not tell you where the threshold belongs, and the
product decides that.

## Evidence boundary

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

## Worked rulings

- **PatterTech EOS ai-ml-llm pack (2026-08, argued)**: A where
  checkable, C only after validation, B as the calibration set, D as
  an item source. Argued from EV-0252 and
  EV-0253 for the selection restriction.
- **Ticket classifier (2026-08, argued)**: A. Labels exist, so a judge
  would add variance and cost for nothing.
- **Retrieval groundedness (2026-08, argued)**: C with a standing
  human sample, because span-level support is not checkable by code
  and the metric is reference-free by construction.
