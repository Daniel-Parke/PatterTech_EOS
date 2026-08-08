---
summary: Building on language models, evaluation before deployment, private held-out sets, pinned model ids and validated judges
type: playbook
tags: [delivery, testing, data, perf]
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model, changes_prompt_or_model, builds_retrieval, evaluates_model_output, ships_model_output]
volatility: fast
review: 2027-02
sources: [EV-0242, EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0255, EV-0256, EV-0257, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262, EV-0263, EV-0264, EV-0265, EV-0266, EV-0267, EV-0268, EV-0085, EV-0086, EV-0087, EV-0212, EV-0213, EV-0214, EV-0215]
---

# AI, ML and LLM pack

This pack covers building on language models: how a prompt, model,
retriever or judge change is accepted or refused on evidence. It
activates on any task that calls a model at runtime, changes a prompt
or a model id, builds retrieval, or decides how model output is
scored. Evaluation before deployment, a private held-out set, pinned
dated model ids and human review of consequential output bind. Which
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

- `calls_a_model`: code in the change sends a prompt to a language
  model at runtime.
- `changes_prompt_or_model`: the change edits a prompt template, a
  model identifier, decoding parameters or retrieval configuration.
- `builds_retrieval`: the change builds or alters a retrieval,
  chunking or embedding path.
- `evaluates_model_output`: the change defines or alters how model
  output is measured or accepted.
- `ships_model_output`: model output reaches a person or takes an
  action outside the process.

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

**Non-goals.** This pack does not own prompt injection, tool
permissions or agent containment, which sit in the security-privacy
pack (EV-0212, EV-0213). It does not own agent loop design, subagents
or harness shape, which sit in the agentic-development pack (EV-0085,
EV-0086). It does not own warehouse modelling or analytics pipelines,
which sit in the data-analytics pack. It does not own the interface
around an AI feature. It does not train foundation models, and it
takes no position on which evaluation library you use.

## Binding requirements

Seven requirements bind. A run that breaks one fails, whatever the
demo looked like.

**B1. No model-facing change ships without an eval run that a machine
can repeat.** A prompt, model, retriever or decoding change is
accepted only after a headless eval entry point at a recorded path has
run against the acceptance set and reported a result. Prevents the
demo-driven change: someone tries six examples by hand, likes the
sixth, and ships a regression nobody can name. Evaluation is an
experiment and has to be reported like one (EV-0255). See
`packs/ai-ml-llm/guides/GD-AIML-001-acceptance-evidence.md`.

**B2. Every eval result carries the prompt template identity and the
model identifier.** The report records the template path and a content
hash of the template, plus the exact model id used. A comparison run
under two different templates is not a comparison. Changing only the
single character separating in-context examples moved MMLU by up to
twenty-three points, enough to reorder a ranking, and the brittleness
did not shrink with scale (EV-0256). Scope note: that was
few-shot multiple choice on open-weight families, so the magnitude is
population-bound and the discipline is not.

**B3. A private held-out set exists, and the tuning path never reads
it.** The venture holds an acceptance set the providers have never
seen, split so that the portion used to select prompts is separate
from the portion used to accept them, and no prompt-selection or
optimiser code reads the held-out file. Prevents scoring your own
homework: accuracy dropped by up to eight points on a fresh set
matched for style and difficulty, with systematic overfitting across
whole model families (EV-0257), and a public leaderboard
distorts under the same pressure, with relative gains of up to 112 per
cent on the arena distribution from modest arena-shaped data
(EV-0258). The same split is the design choice behind the
public practice set and private official set of a published safety
benchmark (EV-0267). Scope note: the eight-point figure is
grade-school arithmetic on 2024 models.

**B4. Model identifiers are dated and pinned, with the retirement date
recorded beside the call site.** No moving alias, no "latest". The
pinned id and its published retirement date live next to the code that
calls it, and a migration eval runs on the candidate before the switch.
Prevents both silent drift and a hard outage: the same endpoint name
changed behaviour substantially inside months, one task falling from
84 per cent to 51 per cent between two snapshots (EV-0259,
whose arithmetic result is contested as partly a formatting artefact),
while the provider lifecycle gives sixty days' notice as a floor and
retired models fail outright (EV-0260). Scope note:
EV-0260 is one vendor's policy, and platform resellers run
their own clocks. See
`packs/ai-ml-llm/guides/GD-AIML-005-model-lifecycle-and-cost.md`.

**B5. A judge is validated against human labels before its score
decides anything.** Where a model grades output and the score selects
between candidates or gates a release, the judge is never the same
model as the one under test, pairwise protocols run both orderings
with order-inconsistent pairs reported as disagreement, and agreement
against a human-labelled sample is measured and reported. Where a
family-mate judge is unavoidable, the measured self-preference offset
is reported rather than assumed to be zero. Prevents a scoreboard that
moves with slot position and family loyalty: position bias varies by
judge and by task and is largest where the answers are close
(EV-0252), and self-recognition causally drives models to
score their own output above others' that humans rate equal
(EV-0253). The roughly eighty per cent judge-human agreement
that makes judging defensible at all is a general-chat number and does
not transfer to domain correctness (EV-0251). See
`packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md`.

**B6. Abstention is scored, and the abstention rate is reported beside
accuracy.** A rubric that pays a guess the same as an admission of
uncertainty selects for confident error, which is the actionable half
of the hallucination argument (EV-0250). The output contract
of a model-backed component includes a way to decline, and the eval
report carries the abstention rate as a first-class field. Prevents
optimising a system into fluent wrongness. Scope note:
EV-0250 is a theoretical argument from a model vendor, not
an experiment, and it does not tell you the right threshold.

**B7. Consequential model output is reviewed by a person before it
takes effect.** Where output moves money, changes access, contacts a
customer, alters production data or produces a legal, medical or
safety claim, a person approves it before it lands. The action classes
and their floors are ruled by `kernel/GUARD_SPEC.md` and
`kernel/POLICY_SPEC.md`, and no eval score lowers them. Prevents
treating an aggregate pass rate as permission for each individual
case: judge-human agreement around eighty per cent is far too coarse
to gate a safety property (EV-0251), a good safety grade is
evidence about one prompt distribution (EV-0267), and
adaptive attackers break defences that pass static evaluation
(EV-0214, EV-0215). This requirement rests on the guard decision as
much as on the measurements.

## Defaults

Each applies unless the venture's lock-book overrides it with a
recorded reason.

**D1. Grade a sample by hand before writing the rubric.** Criteria are
discovered by grading outputs, not declared in advance: practitioners
cannot say what good looks like until they have seen concrete bad
outputs, so requirements and evaluator co-evolve (EV-0254).
Reason: a rubric fixed up front measures the wrong thing with great
rigour. Override only where an external standard already defines the
criteria.

**D2. Report paired differences with a stated minimum detectable
effect.** Compare two variants on the same items, name the pairing in
the report, cluster the standard error where items share a source, and
state what difference the set can detect at its size
(EV-0255). Reason: a gate that cannot say what it can detect
is a coin flip in a suit. Override with a recorded reason only where
the item set genuinely differs between arms.

**D3. Retrieval before fine-tuning for anything that is a fact.**
Retrieval beat unsupervised fine-tuning in almost every
knowledge-injection condition tested, including for facts the base
model had never seen (EV-0248). Fine-tuning is for form,
task shape and format adherence. Reason: facts move faster than
training runs. Scope note: seven-billion-parameter open models and
multiple-choice evaluation, and parameter-efficient tuning is a real
trade rather than a free lunch (EV-0249). See
`packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md`.

**D4. Lexical retrieval first, embeddings earn their place.** Start
with BM25 or a hybrid, and make a dense retriever beat it on your own
corpus before adopting it. Out of domain, BM25 remains a hard baseline
and dense bi-encoders that win in-domain often lose zero-shot
(EV-0246). Reason: the cheapest baseline is also the one
that generalises. Scope note: BEIR predates modern instruction-tuned
embedding models, so the ranking is stale and the discipline of
measuring against the baseline is not.

**D5. Split retrieval metrics by stage.** Measure context precision
and recall for the retriever separately from faithfulness and answer
relevance for the generator (EV-0265), and measure
groundedness against the retrieved context separately from answer
correctness, because a system can be right and ungrounded or grounded
and wrong (EV-0247). Reason: a single end-to-end score
cannot tell you whether to fix the retriever or the prompt.

**D6. Keep dataset, solver and scorer as separate versioned things.**
The decomposition a national safety institute settled on lets you swap
the model without rewriting the eval and swap the scorer without
rewriting the dataset (EV-0264). Reason: model churn is the
one certainty in this domain. Scope note: that framework is built for
model evaluation rather than end-to-end product evaluation, and the
alternatives encode different decompositions (EV-0265,
EV-0266), so the split is one defensible shape rather than
a standard.

**D7. Order every prompt stable prefix first, variable suffix last,
and assert the cache hit rate.** Cached prefix reads are charged at a
tenth of base input while writes cost more, minimum cacheable length
varies by model, and short prompts fail to cache with no error, so the
only reliable check is reading the cache token counts back from the
response (EV-0261). Reason: cost is decided in prompt layout
before it is decided in model choice. This default fights the evidence
placement rule in EV-0243 and the conflict is resolved per
prompt in `packs/ai-ml-llm/refs/CONTEXT_LAYOUT.md`.

**D8. An eval run is reproducible without the network.** Two runs over
the same tree give the same accuracy and the same item count, achieved
by pinning the model id, fixing decoding parameters, recording the
seed, and holding recorded or stubbed responses for the offline path.
Reason: this one is a decision rather than a measured finding. A
number nobody can reproduce cannot be argued about, and a gate that
costs real money per run gets skipped. Override where the acceptance
condition genuinely needs live sampling, and report the run-to-run
variance instead.

## Preferences

Taste. Record them, do not gate on them, and override them without
asking.

- **Compiled prompt optimisation against hand-written legible
  context.** An optimiser that searches instructions and
  demonstrations against a metric answers the brittleness problem
  directly (EV-0266, EV-0256). Direct legible
  context optimises instead for a person reading the transcript and
  seeing why the model did what it did (EV-0086). Nobody has run the
  controlled comparison.
- **Trained cascade routing against model self-assessment routing.** A
  trained confidence scorer and a cheap first model is one shape
  (EV-0262); asking the model whether the retrieved context
  suffices is another (EV-0245). Both work in their own
  papers, on retired models.
- **Which evaluation framework, and where the eval lives.** The
  abstractions matter, the tool does not, and either repository is
  defensible as long as the acceptance set is versioned with the code
  it gates.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| What evidence accepts or refuses this change? | `packs/ai-ml-llm/guides/GD-AIML-001-acceptance-evidence.md` | Private held-out set, paired comparison, stated detectable effect |
| Where does the knowledge come from? | `packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md` | Retrieval, lexical first, with per-query escalation |
| Who grades the output? | `packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md` | Deterministic scorer where possible, model judge only once validated against human labels |
| How is the prompt maintained? | `packs/ai-ml-llm/guides/GD-AIML-004-prompt-maintenance.md` | Hand-written and versioned, with the template hash in every result |
| Which model, and what happens when it retires? | `packs/ai-ml-llm/guides/GD-AIML-005-model-lifecycle-and-cost.md` | One pinned dated model per task, retirement date recorded, migration eval ready |

Level three detail sits in `packs/ai-ml-llm/refs/EVAL_REPORT.md`,
`packs/ai-ml-llm/refs/CONTEXT_LAYOUT.md` and
`packs/ai-ml-llm/refs/MODEL_MIGRATION.md`. A full worked run is at
`packs/ai-ml-llm/exemplars/EX-AIML-001-classifier-prompt-swap.md`.

## Failure modes and anti-patterns

- **The bare percentage.** A number with no interval, no item count
  and no template hash cannot accept or refuse anything
  (EV-0255, EV-0256).
- **Declaring a winner the sample cannot resolve.** Two variants a few
  points apart on a small set are a tie until the arithmetic says
  otherwise.
- **Tuning against the acceptance set.** The moment prompt selection
  reads the held-out file, the held-out file is training data
  (EV-0257).
- **Choosing a model from a leaderboard.** Public position is a
  shortlist generator (EV-0258). The arena operators dispute
  parts of that audit, and the usable conclusion survives the dispute.
- **A model grading itself.** Self-recognition drives self-preference
  (EV-0253), so a family-mate judge selecting between
  candidates is a rigged comparison.
- **Filling the context window because it is there.** Reliability
  falls as input grows even on tasks trivially easy at short length,
  modulated by distractors and by needle-question similarity, so the
  advertised window is a capacity limit rather than a working limit
  (EV-0244, EV-0243).
- **Fine-tuning to teach the model your documents**
  (EV-0248).
- **A single end-to-end RAG score.** It cannot attribute failure to
  retriever or generator (EV-0265), and RAG failure clusters
  at named seams that only production traffic reveals
  (EV-0242).
- **Assuming retrieval solved hallucination.** Models still contradict
  the context they were handed, at rates differing sharply between
  generators on identical retrieved input (EV-0247).
- **Emitting JSON straight out of a reasoning step without measuring
  it.** Format restriction cost reasoning accuracy in one study, worse
  under constrained decoding than under a plain instruction, with
  reason-then-convert as the mitigation (EV-0263). The
  library maintainers dispute the comparison, so this is a
  must-measure rather than a rule.
- **Reading a safety grade as robustness** (EV-0267,
  EV-0214, EV-0215).

## Open questions and counter-evidence

**Long context against retrieval is unresolved.** Long-context
prompting beat retrieval on average quality when the tokens were
affordable, and retrieval's advantage was cost (EV-0245).
Position effects and context rot say average quality hides a worse
tail (EV-0243, EV-0244). Both can hold at once:
an average win with a worse tail. The resolution both sides support is
per-query routing with a measured escalation rate. Do not let a
venture settle this by preference.

**Caching order fights evidence order.** Caching wants the invariant
material first (EV-0261); position evidence wants the
load-bearing evidence at the edges (EV-0243). These pull on
the same bytes, and the conflict is resolved per prompt with a
measurement, never by picking a camp.

**Compiled against legible prompts has no controlled comparison.** It
is a preference in this pack for that reason, and the first credible
head-to-head study is a trigger to re-argue.

**Judge validity for domain correctness is largely unmeasured.** The
eighty per cent agreement figure is general chat preference
(EV-0251). Borrowing it for domain-specific grading is the
most common quiet error in this domain.

**Agentic trajectory evaluation has no validated method.** Nobody has
a good answer for grading a twenty-step run where the final artefact
is correct and the path was wasteful (EV-0264, EV-0087).

**Cost and latency management is the weakest-evidenced area here.**
The best primary source is three years old and predates prompt caching
and batch pricing (EV-0262), which is why cost sits in
defaults and preferences and never in the binding set.

**Every controlled number in this pack was measured on models that are
now retired.** Direction of effect probably transfers, magnitude
almost certainly does not. Treat each figure as carrying a
re-measurement trigger rather than a citation.

**Provider obligations are moving.** The EU code of practice binds
model providers rather than downstream builders, and the transparency
chapter defines what documentation you are entitled to receive about a
dependency (EV-0268). The UK position diverges (EV-0041,
EV-0225), so a UK venture selling into the EU carries two regimes.

**Refresh triggers.** Re-argue this pack on: a replication of the
position and context-rot effects on a current frontier model class; a
judge-human agreement study on domain correctness; a controlled
comparison of compiled against hand-written prompts; a current-model
replication of the structured-output penalty; the first Commission
enforcement decision under the GPAI code.

## Evidence pointer

The twenty-seven primary rows behind this pack, each with version or
commit, licence, access date, population, applicability limits and a
review trigger, are frozen at
`packs/ai-ml-llm/research/sources.fragment.json` and cited above by
their fragment ids. The integrator imports that fragment into
`registry/evidence.json`, at which point each row takes its final EV
id and the citations here are rewritten in one pass. Rows already in
the ledger (EV-0085, EV-0086, EV-0087, EV-0212 to EV-0215) are cited
by their EV ids directly. The maintained implementations among them
are Inspect (MIT, inspected 2026-08-03, EV-0264), Ragas
(Apache-2.0, EV-0265) and DSPy (MIT, EV-0266),
each a published repository with its own row and its own review
trigger.
