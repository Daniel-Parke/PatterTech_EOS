---
summary: Activation, outcomes and decision map for the ai-ml-llm Doctrine and Wargames
type: pack
tags: [delivery, testing, data, perf]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [calls_a_model, changes_prompt_or_model, builds_retrieval, evaluates_model_output, ships_model_output]
activation_paths: [**/prompts/**, **/evals/**, **/eval/**, **/retrieval/**, **/embeddings/**, **/*model*.py, **/*llm*.py, **/*judge*.py, **/*.prompt, **/*.prompt.md]
volatility: fast
review: none
sources: [EV-0242, EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0255, EV-0256, EV-0257, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262, EV-0263, EV-0264, EV-0265, EV-0266, EV-0267, EV-0268, EV-0041, EV-0085, EV-0086, EV-0087, EV-0212, EV-0213, EV-0214, EV-0215, EV-0225]
display_name: AI Systems and Evaluation
category: data-ai
id_namespace: AIML
depends_on: [data-analytics, security-privacy]
---


# AI Systems and Evaluation

This pack covers building on language models: how a prompt, model,
retriever or judge change is accepted or refused on evidence. It
activates on any task that calls a model at runtime, changes a prompt or
a model id, builds retrieval, or decides how model output is scored.
Result identity, an unread held-out set, pinned model ids, a validated
judge and a person in front of consequential output bind. Which
philosophy you build under does not.

## Activation

Load this pack when any of the following is true.

**Paths touched.** Prompt and template files, eval sets and eval
runners, retrieval and embedding configuration, model client wrappers,
judge and scorer definitions, fine-tuning or adapter configuration,
anything holding a model identifier.

**Task types.** Adding or changing a model-backed feature. Swapping a
prompt, a model, a retriever or a decoding setting. Designing or
changing how model output is scored or accepted. Diagnosing wrong,
ungrounded or overconfident output. Migrating off a deprecated model.

**Keywords, fallback only.** Prompt, eval, RAG, retrieval, embedding,
hallucination, judge, rubric, fine-tune, temperature, context window,
token cost. Keywords are the weakest signal and never override the
predicates.

**Applicability predicates.**

- `calls_a_model`: code in the change sends a prompt to a language model
  at runtime.
- `changes_prompt_or_model`: the change edits a prompt template, a model
  identifier, decoding parameters or retrieval configuration.
- `builds_retrieval`: the change builds or alters a retrieval, chunking
  or embedding path.
- `evaluates_model_output`: the change defines or alters how model
  output is measured or accepted.
- `ships_model_output`: model output reaches a person or takes an action
  outside the process.

Do not load this pack for a task that only reads model documentation,
for agent harness and orchestration work, which is the
agentic-development pack, or for a copy edit to a prompt's user-facing
wording that no eval covers and no user sees.

## Outcomes and non-goals

**Outcomes.** Any change to the model-facing surface is accepted or
refused against a stated acceptance condition, measured on items the
provider has never seen, reported with the exact prompt template and
model id attached. A result nobody can reproduce is not accepted. The
system can say it does not know, and how often it does so is a number
somebody watches. When a person is on the receiving end of a
consequential answer, a person has looked at it first.

**Non-goals.** This pack does not own prompt injection, tool permissions
or agent containment, which sit in the security-privacy pack (EV-0212,
EV-0213). It does not own agent loop design, subagents or harness shape,
which sit in the agentic-development pack (EV-0085, EV-0086). It does
not own warehouse modelling or analytics pipelines, which sit in the
data-analytics pack. It does not own the interface around an AI feature.
It does not train foundation models, and it takes no position on which
evaluation library you use.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B2"></a>
- `B2` to [DOC-AIML-001](doctrines/DOC-AIML-001-every-eval-result-carries-the-prompt-template-identity-and.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-AIML-002](doctrines/DOC-AIML-002-a-private-held-out-set-exists-and-the-tuning-path-never.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-AIML-003](doctrines/DOC-AIML-003-model-identifiers-are-pinned-to-a-version-the-provider-has.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-AIML-004](doctrines/DOC-AIML-004-a-judge-is-validated-against-human-labels-before-its-score.md) (binding)
<a id="B7"></a>
- `B7` to [DOC-AIML-005](doctrines/DOC-AIML-005-consequential-model-output-is-reviewed-by-a-person-before.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-AIML-006](doctrines/DOC-AIML-006-grade-a-sample-by-hand-before-writing-the-rubric.md) (default)
<a id="D2"></a>
- `D2` to [DOC-AIML-007](doctrines/DOC-AIML-007-report-paired-differences-with-a-stated-minimum-detectable.md) (default)
<a id="D3"></a>
- `D3` to [DOC-AIML-008](doctrines/DOC-AIML-008-retrieval-before-fine-tuning-for-anything-that-is-a-fact.md) (default)
<a id="D4"></a>
- `D4` to [DOC-AIML-009](doctrines/DOC-AIML-009-lexical-retrieval-first-embeddings-earn-their-place.md) (default)
<a id="D5"></a>
- `D5` to [DOC-AIML-010](doctrines/DOC-AIML-010-split-retrieval-metrics-by-stage.md) (default)
<a id="D6"></a>
- `D6` to [DOC-AIML-011](doctrines/DOC-AIML-011-keep-dataset-solver-and-scorer-as-separate-versioned-things.md) (default)
<a id="D7"></a>
- `D7` to [DOC-AIML-012](doctrines/DOC-AIML-012-order-every-prompt-stable-prefix-first-variable-suffix-last.md) (default)
<a id="D8"></a>
- `D8` to [DOC-AIML-013](doctrines/DOC-AIML-013-an-eval-run-is-reproducible-without-the-network.md) (default)
<a id="D9"></a>
- `D9` to [DOC-AIML-014](doctrines/DOC-AIML-014-run-a-machine-repeatable-eval-before-a-model-facing-change.md) (default)
<a id="D10"></a>
- `D10` to [DOC-AIML-015](doctrines/DOC-AIML-015-score-abstention-and-report-the-abstention-rate-beside.md) (default)
- source `preferences:001` to [DOC-AIML-016](doctrines/DOC-AIML-016-compiled-prompt-optimisation-against-hand-written-legible.md) (preference)
- source `preferences:002` to [DOC-AIML-017](doctrines/DOC-AIML-017-trained-cascade-routing-against-model-self-assessment.md) (preference)
- source `preferences:003` to [DOC-AIML-018](doctrines/DOC-AIML-018-which-evaluation-framework-and-where-the-eval-lives.md) (preference)

### Later evidence-led admissions

These records were admitted after the frozen source migration.
Their own metadata is canonical; this map does not restate it.

- [WG-AIML-001](wargames/WG-AIML-001-model-hosting.md) (Wargame)

## Decision map

| Fork | Wargame | Default |
| --- | --- | --- |
| What evidence accepts or refuses this change? | `packs/ai-ml-llm/wargames/WG-AIML-002-acceptance-evidence.md` | Private held-out set, paired comparison, stated detectable effect |
| Where does the knowledge come from? | `packs/ai-ml-llm/wargames/WG-AIML-003-knowledge-source.md` | Retrieval, lexical first, with per-query escalation |
| Who grades the output? | `packs/ai-ml-llm/wargames/WG-AIML-004-who-grades-the-output.md` | Deterministic scorer where possible, model judge only once validated against human labels |
| How is the prompt maintained? | `packs/ai-ml-llm/wargames/WG-AIML-005-prompt-maintenance.md` | Hand-written and versioned, with the template hash in every result |
| Which model, and what happens when it retires? | `packs/ai-ml-llm/wargames/WG-AIML-006-model-lifecycle-and-cost.md` | One pinned model per task, retirement date recorded, migration eval ready |

Level three detail sits in `packs/ai-ml-llm/references/EVAL_REPORT.md`,
`packs/ai-ml-llm/references/CONTEXT_LAYOUT.md` and
`packs/ai-ml-llm/references/MODEL_MIGRATION.md`. A full worked run is at
`packs/ai-ml-llm/examples/EX-AIML-001-classifier-prompt-swap.md`.

## Failure modes and anti-patterns

- **The bare percentage.** A number with no interval, no item count and
  no template hash cannot accept or refuse anything (EV-0255, EV-0256).
- **Declaring a winner the sample cannot resolve.** Two variants a few
  points apart on a small set are a tie until the arithmetic says
  otherwise.
- **Tuning against the acceptance set.** The moment prompt selection
  reads the held-out file, the held-out file is training data (EV-0257).
- **Choosing a model from a leaderboard.** Public position is a
  shortlist generator (EV-0258). The arena operators dispute parts of
  that audit, and the usable conclusion survives the dispute.
- **A model grading itself.** Self-recognition drives self-preference
  (EV-0253), so a family-mate judge selecting between candidates is a
  rigged comparison.
- **Filling the context window because it is there.** Reliability falls
  as input grows even on tasks trivially easy at short length, modulated
  by distractors and by needle-question similarity, so the advertised
  window is a capacity limit rather than a working limit (EV-0244,
  EV-0243).
- **Fine-tuning to teach the model your documents** (EV-0248).
- **A single end-to-end RAG score.** It cannot attribute failure to
  retriever or generator (EV-0265), and RAG failure clusters at named
  seams that only production traffic reveals (EV-0242).
- **Assuming retrieval solved hallucination.** Models still contradict
  the context they were handed, at rates differing sharply between
  generators on identical retrieved input (EV-0247).
- **Emitting JSON straight out of a reasoning step without measuring
  it.** Format restriction cost reasoning accuracy in one study, worse
  under constrained decoding than under a plain instruction, with
  reason-then-convert as the mitigation (EV-0263). The library
  maintainers dispute the comparison, so this is a must-measure rather
  than a rule.
- **Reading a safety grade as robustness** (EV-0267, EV-0214, EV-0215).

## Open questions and counter-evidence

**Long context against retrieval is unresolved.** Long-context prompting
beat retrieval on average quality when the tokens were affordable, and
retrieval's advantage was cost (EV-0245). Position effects and context
rot say average quality hides a worse tail (EV-0243, EV-0244). Both can
hold at once: an average win with a worse tail. The resolution both
sides support is per-query routing with a measured escalation rate. Do
not let a venture settle this by preference.

**Caching order fights evidence order.** Caching wants the invariant
material first (EV-0261); position evidence wants the load-bearing
evidence at the edges (EV-0243). These pull on the same bytes, and the
conflict is resolved per prompt with a measurement, never by picking a
camp.

**Compiled against legible prompts has no controlled comparison.** It is
a preference in this pack for that reason, and the first credible
head-to-head study is a trigger to re-argue.

**Judge validity for domain correctness is largely unmeasured.** The
eighty per cent agreement figure is general chat preference (EV-0251).
Borrowing it for domain-specific grading is the most common quiet error
in this domain.

**Agentic trajectory evaluation has no validated method.** Nobody has a
good answer for grading a twenty-step run where the final artefact is
correct and the path was wasteful (EV-0264, EV-0087).

**Cost and latency management is the weakest-evidenced area here.** The
best primary source is three years old and predates prompt caching and
batch pricing (EV-0262), which is why cost sits in defaults and
preferences and never in the binding set.

**Every controlled number in this pack was measured on models that are
now retired.** Direction of effect probably transfers, magnitude almost
certainly does not. Treat each figure as carrying a re-measurement
trigger rather than a citation.

**Provider obligations are moving.** The EU code of practice binds model
providers rather than downstream builders, and the transparency chapter
defines what documentation you are entitled to receive about a
dependency (EV-0268). The UK position diverges (EV-0041, EV-0225), so a
UK venture selling into the EU carries two regimes.

**Refresh triggers.** Re-argue this pack on: a replication of the
position and context-rot effects on a current frontier model class; a
judge-human agreement study on domain correctness; a controlled
comparison of compiled against hand-written prompts; a current-model
replication of the structured-output penalty; the first Commission
enforcement decision under the GPAI code.

## Evidence pointer

The twenty-seven primary rows behind this pack were frozen at
`packs/ai-ml-llm/research/sources.fragment.json` and have since been
imported into `registry/evidence.json` as EV-0242 to EV-0268. Every
`EV-` id cited above resolves to a row there carrying version or commit,
licence, access date, population, applicability limits and a review
trigger. The fragment file stays as the frozen record of what the
research pass found. The maintained implementations among the rows are
Inspect (MIT, inspected 2026-08-03, EV-0264), Ragas (Apache-2.0,
EV-0265) and DSPy (MIT, EV-0266), each a published repository with its
own row and its own review trigger. The synthesis and the
disagreements behind this file are in
`packs/ai-ml-llm/research/NOTES.md`, and the licence and quotation
sweep over these rows is at
`packs/ai-ml-llm/research/provenance.fragment.json`.
