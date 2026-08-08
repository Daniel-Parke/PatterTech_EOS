---
summary: How is a prompt maintained over time, hand-written and versioned, few-shot, compiled by an optimiser, or replaced by fine-tuning?
type: guide
tags: [delivery, testing, content]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0243, EV-0249, EV-0256, EV-0261, EV-0263, EV-0266, EV-0086]
review: 2026-12
---

# GD-AIML-004: How is the prompt maintained?

## The question

A prompt starts as a string somebody typed and ends as the most
load-bearing untested artefact in the system. Changing the single
character separating in-context examples moved MMLU by up to
twenty-three points, enough to reorder a leaderboard, and the
brittleness did not shrink with scale (EV-0256). If a
character matters that much, the question of how the text is produced
and kept is an engineering question rather than a writing one.

## It depends on

- Do you have a metric and a labelled set yet? Nothing that optimises
  can run without one.
- How many tuned variants have you already been through by hand?
- Will you need to read a transcript and explain a bad output to
  somebody?
- How often does the model underneath change?
- Who maintains it in a year, and will they be able to debug an
  artefact nobody wrote?

## Options

### A. Hand-written, versioned, hashed

The template is a file in the repository, its content hash travels
with every eval result, and changes go through the same acceptance
path as code. Buys: legibility, a diff a person can argue with, and
the ability to read the context and see why the model did what it did
(EV-0086). Costs: tuning is folklore, and folklore does not transfer
between models.

### B. Few-shot demonstrations

The prompt carries selected examples, chosen and maintained by hand.
Buys: a cheap and effective lift on format adherence and edge cases.
Costs: the demonstrations are now training data with no version
discipline, formatting choices inside them are load-bearing
(EV-0256), and they consume the context budget the evidence
also wants.

### C. Compiled by an optimiser

Declare the signature and the metric, let an optimiser search
instructions and demonstrations, and version the program and the
metric rather than the prompt text (EV-0266). Buys: the
formatting choices stop being guesses, and the artefact is
reproducible from the program plus the metric. Costs: it needs a
metric and a labelled set before it can do anything, the compiled
artefact is tied to a library version and a model version and must be
recompiled when either moves, and a small team ends up debugging text
nobody wrote.

### D. Fine-tune the behaviour in

Move the instruction into the weights. Buys: shorter prompts, lower
per-query cost, and stable behaviour. Costs: a training pipeline, and
a trade between target-domain fit and preserved general behaviour
(EV-0249). See
`packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md`.

## Decision rule

- Always, under every option: the template is a versioned file and its
  content hash is attached to every eval result. A comparison run
  under two templates is no comparison.
- No metric and no labelled set yet: A. C can do nothing here.
- A metric exists and you have hand-tuned more than a handful of
  variants: C is the cheaper option from that point on, and the team
  has to accept a compiled artefact.
- Debuggability by a person is the dominant requirement: A, and accept
  that you are trading measured optimality for legibility.
- Instruction is stable, high-volume and cost-sensitive: consider D,
  and evaluate it against A on the same set.
- Output must be structured: measure schema-constrained generation
  against reason-then-convert rather than assuming either
  (EV-0263).

## Default

A. Most ventures here are one person directing agents, the metric
arrives after the first prompt, and the ability to read a transcript
and explain a failure is worth more than the last few points. This is
a default and not a finding: nobody has run the controlled comparison
between compiled and hand-written prompts, and the first credible one
should reopen this guide.

## Layout, and the conflict inside it

Prompt layout is part of the artefact. Caching wants the invariant
material first, since cached reads are charged at a tenth of base
input and short prompts fail to cache with no error
(EV-0261). Position evidence wants the load-bearing evidence
at the edges (EV-0243). The resolution is per prompt, and
the mechanics are in `packs/ai-ml-llm/refs/CONTEXT_LAYOUT.md`.

## Evidence boundary

The delimiter result is few-shot multiple choice on open-weight
families, so it is evidence that formatting is load-bearing rather
than a theory of which formatting choices matter, and the effect size
on zero-shot instruction-following chat models is not established
there. The structured-output penalty was measured on 2024 models and
its constrained-decoding comparison is disputed by the library
maintainers as unrepresentative of correct usage, which is why the
rule here is to measure rather than to prefer.

## Worked rulings

- **PatterTech EOS ai-ml-llm pack (2026-08, argued)**: A as default,
  C as a legitimate alternative once a metric exists, with the choice
  recorded as a preference rather than dressed as evidence.
- **Ticket classifier (2026-08, argued)**: A with the template hash in
  the eval report, which is what made the A against B comparison
  meaningful at all.
- **Structured extraction endpoint (2026-08, argued)**: A, with an
  eval comparing direct JSON emission against reason-then-convert on
  the same items, because the penalty is contested and cheap to
  measure locally.
