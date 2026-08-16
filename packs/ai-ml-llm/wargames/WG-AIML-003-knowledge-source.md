---
id: WG-AIML-003
summary: Where does the model get the facts, retrieval, whole context, per-query routing or fine-tuning?
kind: wargame
type: wargame
tags: [data, delivery, eos, perf, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-AIML-008]
applies_when: [calls_a_model]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0261]
review: on-change-of:EV-0245
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-AIML-003: Where do the facts come from?

## Decision question and stakes

The model does not know your data. There are four ways to fix that and
they differ in cost, in freshness, in how a wrong answer is diagnosed,
and in whether a citation is possible. This is the architectural fork
in every model-backed product, and it is usually decided by fashion.

## Doctrines or coverage gap under pressure

- `DOC-AIML-008` (default): Retrieval before fine-tuning for anything that is a fact.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How fast do the facts change relative to how often you could
  retrain?
- Does the whole corpus fit in a context window at a price you would
  pay per query?
- Is a citation required, either by the user or by a regulator?
- Are you missing knowledge, or missing form? Tone, format adherence
  and task shape are a different problem from facts.
- What is the tail behaviour you can tolerate, as against the average?

Applicability is `calls_a_model`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Retrieval

Assume `A. Retrieval` was selected and the outcome failed. Test this option's stated failure mechanism first: that scales with the query rather than the corpus. Retrieval beat unsupervised fine-tuning in almost every knowledge-injection condition tested, including for facts the base model had never seen (EV-0248). Costs: a retriever to build and evaluate, chunking decisions that fail quietly, and the standing risk that the model contradicts the context it was given (EV-0247).

### Premortem for B. Whole context

Assume `B. Whole context` was selected and the outcome failed. Test this option's stated failure mechanism first: price per query, and a tail that averages hide. Position inside the context changes whether evidence is used (EV-0243), and reliability falls as input grows even on tasks trivially easy at short length, modulated by distractors and by needle-question similarity (EV-0244).

### Premortem for C. Per-query routing

Assume `C. Per-query routing` was selected and the outcome failed. Test this option's stated failure mechanism first: , with an escalation rate that is a measurable dial (EV-0245). Costs: two paths to maintain and evaluate, and a router that inherits the model's own calibration problems.

### Premortem for D. Fine-tuning

Assume `D. Fine-tuning` was selected and the outcome failed. Test this option's stated failure mechanism first: for a fixed behaviour. Parameter efficient methods preserve base behaviour outside the target domain better, at the price of learning the target domain less well (EV-0249). Costs: a training pipeline, a data pipeline, and a knowledge store that is stale the day it finishes.

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

## Safe default

A, with lexical retrieval first. BM25 remains a hard baseline out of
domain and dense bi-encoders that win in-domain often lose zero-shot
(EV-0246), so an embedding retriever earns its place against
BM25 on your own corpus, and a reranker earns its place against its
latency.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How fast do the facts change relative to how often you could retrain?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with lexical retrieval first. BM25 remains a hard baseline out of domain and dense bi-encoders that win in-domain often lose zero-shot (EV-0246), so an embedding retriever earns its place against BM25 on your own corpus, and a reranker earns its place against its latency.

**Exit condition:** Stop or roll back the selected branch when that scales with the query rather than the corpus. Retrieval beat unsupervised fine-tuning in almost every knowledge-injection condition tested, including for facts the base model had never seen (EV-0248). Costs: a retriever to build and evaluate, chunking decisions that fail quietly, and the standing risk that the model contradicts the context it was given (EV-0247), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How fast do the facts change relative to how often you could retrain?

## Counter-evidence and transfer limits

### Evidence boundary

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
### Preserved reasoning: The unresolved part

Long context against retrieval is not settled and the two camps
measure different things. An average-quality win for long context
(EV-0245) can coexist with worse tail behaviour
(EV-0243, EV-0244). C is the practical resolution
both sides support. Do not settle it by preference, and do not quote
either result as though it closed the argument.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
