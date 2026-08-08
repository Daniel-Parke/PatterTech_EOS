---
summary: Where does the model get the facts, retrieval, whole context, per-query routing or fine-tuning?
type: guide
tags: [data, perf, delivery]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0261]
review: on-change-of:EV-0245
---

# GD-AIML-002: Where do the facts come from?

## The question

The model does not know your data. There are four ways to fix that and
they differ in cost, in freshness, in how a wrong answer is diagnosed,
and in whether a citation is possible. This is the architectural fork
in every model-backed product, and it is usually decided by fashion.

## It depends on

- How fast do the facts change relative to how often you could
  retrain?
- Does the whole corpus fit in a context window at a price you would
  pay per query?
- Is a citation required, either by the user or by a regulator?
- Are you missing knowledge, or missing form? Tone, format adherence
  and task shape are a different problem from facts.
- What is the tail behaviour you can tolerate, as against the average?

## Options

### A. Retrieval

Keep the model ignorant and feed it the relevant documents at request
time. Buys: freshness, citations, and a cost that scales with the
query rather than the corpus. Retrieval beat unsupervised fine-tuning
in almost every knowledge-injection condition tested, including for
facts the base model had never seen (EV-0248). Costs: a
retriever to build and evaluate, chunking decisions that fail quietly,
and the standing risk that the model contradicts the context it was
given (EV-0247).

### B. Whole context

Put the corpus in the prompt. Buys: no retrieval stack, and on average
better quality than retrieval when the tokens are affordable
(EV-0245). Costs: price per query, and a tail that averages
hide. Position inside the context changes whether evidence is used
(EV-0243), and reliability falls as input grows even on
tasks trivially easy at short length, modulated by distractors and by
needle-question similarity (EV-0244).

### C. Per-query routing

Retrieve first, ask whether the retrieved context suffices, and
escalate to the full context only when it does not. Buys: close to
long-context quality at close to retrieval cost, with an escalation
rate that is a measurable dial (EV-0245). Costs: two paths
to maintain and evaluate, and a router that inherits the model's own
calibration problems.

### D. Fine-tuning

Train the weights. Buys: form, tone, format adherence and task shape,
and lower per-query token cost for a fixed behaviour. Parameter
efficient methods preserve base behaviour outside the target domain
better, at the price of learning the target domain less well
(EV-0249). Costs: a training pipeline, a data pipeline, and
a knowledge store that is stale the day it finishes.

## Decision rule

- The answer depends on facts that change, or a citation is required:
  A.
- The corpus is small, static and fits in a window you would pay for
  every time: B, with the usable context length measured rather than
  assumed.
- Query mix is mixed and cost matters: C, with the escalation rate
  reported in telemetry.
- The gap is tone, format or task shape rather than facts: D, and
  only then.
- Someone proposes D to teach the model your documents: refuse it and
  ask for the A comparison first (EV-0248).
- Under A or C, groundedness against the retrieved context is measured
  separately from correctness (EV-0247).

## Default

A, with lexical retrieval first. BM25 remains a hard baseline out of
domain and dense bi-encoders that win in-domain often lose zero-shot
(EV-0246), so an embedding retriever earns its place against
BM25 on your own corpus, and a reranker earns its place against its
latency.

## The unresolved part

Long context against retrieval is not settled and the two camps
measure different things. An average-quality win for long context
(EV-0245) can coexist with worse tail behaviour
(EV-0243, EV-0244). C is the practical resolution
both sides support. Do not settle it by preference, and do not quote
either result as though it closed the argument.

## Evidence boundary

EV-0245 measured public corpora that fit in a window at all,
priced at 2024 tariffs and before prompt caching changed the
arithmetic (EV-0261). EV-0248 tested
seven-billion-parameter open models with unsupervised continued
pretraining, which is a different intervention from supervised
instruction tuning on curated pairs. EV-0244 comes from a
retrieval vendor whose product benefits if long context looks
unreliable, and its toolkit is open for replication. BEIR predates
modern embedding models, so its ranking is stale while its baseline
discipline is not.

## Worked rulings

- **PatterTech EOS ai-ml-llm pack (2026-08, argued)**: A as the
  default with lexical retrieval first, C where the query mix
  justifies two paths, D restricted to form. Argued from
  EV-0248 and EV-0246.
- **Product documentation assistant (2026-08, argued)**: A. The corpus
  changes weekly and every answer needs a link back to a page, which
  rules out B and D on freshness and on citation.
- **House writing voice (2026-08, inherited)**: D, because the gap is
  form rather than fact, with the knowledge still arriving by
  retrieval.
