---
summary: What holds the truth that checks an agent's work, and what do you do when nothing does?
kind: guide
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
sources: [EV-0053, EV-0076, EV-0087, EV-0089, EV-0108, EV-0109, EV-0111, EV-0115, EV-0119, EV-0120]
review: on-change-of:anthropic-evals-publication
type: guide
tags: [eos, delivery, tooling]
---

# GD-AGENT-004: What checks the work?

## The question

An agent that cannot be checked cannot be trusted to iterate. The fork
is what holds the ground truth: a machine oracle, a rule set, another
model, or a person. Get this wrong and an evaluator-optimizer loop
becomes an expensive way to make the answer worse.

## It depends on

- **Oracle quality**: is there something outside the generator that
  says right or wrong, and how complete is it?
- **Reversibility**: what does a wrong answer that gets through cost?
- **Determinism**: does the same input give the same verdict?
- **Latency and cost**: how often can the check run?
- **Coverage**: does the check see the whole output or a slice?

## Options

### A. Machine oracle
Tests, type checkers, compilers, schema validators, linters. Buys
deterministic external truth, cheap to run repeatedly, and it is the
condition under which self-directed iteration reliably improves work
(EV-0053, EV-0111). Costs authoring, and it only covers what it
asserts.

### B. Defined rules and mechanical checks
Explicit assertions the output must satisfy: required sections,
forbidden strings, line budgets, shape checks. Buys determinism where
no test suite is possible, and it is ranked above a model judge in
vendor guidance (EV-0115). Costs expressiveness, since taste does not
reduce to regex.

### C. Model as judge
A separate model, separate context, scoring against a rubric. Buys
coverage of things rules cannot express. Costs determinism and
calibration, and it is worth nothing at all if the judge is the same
context that generated the work, because intrinsic self-correction
without external feedback degrades answers (EV-0111, EV-0089).

### D. Human review at a checkpoint
A person looks before the act lands. Buys judgement and accountability.
Costs latency, and it does not scale to every output (EV-0108).

## Decision rule

If a machine oracle exists or can be written in reasonable time, A, and
put the generating step inside an evaluator-optimizer loop. If not, B
for everything that reduces to a mechanical assertion. Use C only as a
separate context with a written rubric, and never as the sole gate on
anything irreversible. Use D at every irreversible or externally
visible act regardless of what else is in place, because that is
binding requirement B3. Where none of A, B or C hold, say the output
has no external oracle and do not claim an iteration loop for it. That
statement is a legitimate answer and is more useful than a judge
nobody believes.

Guardrails are a different thing from evaluation: cheap checks that run
beside the work and trip a wire, registered at the runner rather than
inside an agent so no agent can configure them away (EV-0076, EV-0120,
EV-0119).

## Default

A where an oracle exists, B where it does not, D at every irreversible
act. Evaluation suites start at twenty to fifty tasks harvested from
real failures and score pass@k and pass^k, because a single green run
proves little against a non-deterministic system (EV-0087).

## Worked rulings

- **PatterTech_EOS (2026-08, argued)**: B for pack acceptance. Each
  pack has a frozen drill whose criteria are regex and line-count
  assertions over one output file, and nothing is graded by a model.
  Chosen because prose quality has no machine oracle and a model judge
  would have graded work written by the same family of model.
- **PatterTech_EOS (2026-08, inherited)**: A for the tooling, with the
  test suite as the oracle and the checker as a second mechanical
  layer.

## Notes

Absent verification is one of the three failure clusters that dominate
annotated multi-agent traces, alongside specification gaps and
inter-agent misalignment (EV-0109). Whoever writes the oracle should
not be holding the implementation in context; that separation is the
one this estate kept from v1.
