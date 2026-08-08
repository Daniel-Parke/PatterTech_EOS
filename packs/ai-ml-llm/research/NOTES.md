---
summary: Research synthesis for the AI, ML and LLM pack, four philosophies of building on models, and what should bind
type: example
tags: [eos, testing]
---

# AI, ML and LLM pack research notes

Cutoff 2026-08-03. Twenty-seven new sources in `sources.fragment.json`,
plus ledger records cited by EV id. The domain question is not "how do
you prompt well". It is: when the component at the centre of your
product is non-deterministic, undocumented, changes under you and will
be retired on a published date, what does engineering discipline
actually consist of.

## Four philosophies, and when each fits

These are materially different answers to where quality comes from.
They are not stages of one maturity ladder.

**1. Evaluation-first.** The eval set is the primary artefact and the
prompt, model and retrieval are all variables tuned against it. The
strongest technical case is FRAG-AI-ML-LLM-14: an eval is an
experiment, a bare percentage is not a result, paired differences on
the same questions remove question-difficulty variance and sharply
raise power, and a gate that has not stated its minimum detectable
effect is a coin flip in a suit. FRAG-AI-ML-LLM-16 supplies the reason
the set must be private, with up to eight points of measured drop when
a benchmark is restated fresh, and FRAG-AI-ML-LLM-17 shows what happens
to a public scoreboard once providers optimise against it, with gains
of up to 112 per cent on the arena distribution from modest extra data.
Fits: anything with a stateable acceptance condition, any model
migration, any prompt change you intend to keep. Anti-pattern: writing
the rubric before grading anything. FRAG-AI-ML-LLM-13 names criteria
drift, where practitioners cannot say what good looks like until they
have seen concrete bad outputs, so a rubric fixed up front measures the
wrong thing with great rigour.

**2. Context engineering.** Treat the context window as the design
surface: choose what goes in, in what order, at what budget, and keep
the whole thing legible to a human reading the transcript. EV-0086 and
EV-0085 are the maintained statement of this position, EV-0087 the
evaluation half. FRAG-AI-ML-LLM-02 gives it the mechanism, since
position inside the context measurably changes whether evidence is
used, and FRAG-AI-ML-LLM-03 shows the effect is not a tidy curve but a
surface modulated by distractors, needle-question similarity and
haystack structure, with real loss well before the advertised window is
full. Fits: agent loops, long-running work, anything where you will
need to debug a bad output by reading what the model actually saw.
Anti-pattern: filling the window because it is there. Advertised
context is a capacity limit, not a working limit.

**3. Compile the prompt.** Declare the signature and the metric, let an
optimiser search instructions and demonstrations, put the program and
the metric under version control instead of the prompt text.
FRAG-AI-ML-LLM-25 is the maintained implementation of this.
FRAG-AI-ML-LLM-15 is the argument for it: changing the single character
separating in-context examples moved MMLU by up to twenty-three points,
enough to reorder a leaderboard, and the brittleness did not shrink
with scale. If a character matters that much, hand-tuning is folklore.
Fits: a mature pipeline with a labelled set and more than a handful of
tuned variants. Anti-pattern: reaching for it before you have a metric,
where it can do nothing, or on a small team that will later have to
debug a compiled artefact nobody wrote.

**4. Retrieval as the knowledge substrate.** Keep the model ignorant
and feed it facts at request time. FRAG-AI-ML-LLM-07 is the clearest
evidence for the split: retrieval beat unsupervised fine-tuning in
almost every knowledge-injection condition tested, including for facts
the base model had never seen. FRAG-AI-ML-LLM-05 says start lexical,
because BM25 remains a hard baseline out of domain and dense retrievers
that win in-domain often lose zero-shot. Fits: anything where the facts
change faster than you can retrain, and anything where a citation is
required. Anti-pattern: assuming retrieval solved hallucination.
FRAG-AI-ML-LLM-06 annotated word-level hallucination across roughly
18,000 RAG responses and found models still contradict the very context
they were handed, at rates that differ sharply between generators on
identical retrieved input.

## The disagreements, stated honestly

**Long context versus retrieval is unresolved and the two camps measure
different things.** FRAG-AI-ML-LLM-04 found that when you can afford the
tokens, long-context prompting beat retrieval on average quality, and
retrieval's advantage was cost. FRAG-AI-ML-LLM-03 and
FRAG-AI-ML-LLM-02 found long-context reading degrades in ways an
average hides. Both can be true: an average win with a worse tail. The
practical resolution both sides support is routing, per query, with a
measured escalation rate, which is what Self-Route does. Do not let a
venture settle this by preference.

**Caching order fights retrieval order.** FRAG-AI-ML-LLM-20 wants the
invariant material first so a stable prefix can be cached at a tenth of
base input price. FRAG-AI-ML-LLM-02 wants the load-bearing evidence at
the edges. These pull in opposite directions on the same bytes and the
conflict has to be resolved deliberately per prompt, usually by putting
the stable system material first, the retrieved evidence last, and
measuring whether the front position was ever carrying weight.

**Structured output cost is contested.** FRAG-AI-ML-LLM-22 measured
reasoning accuracy falling under format restriction, worse under
constrained decoding than under a plain instruction, and recommended
reason-then-convert in two calls. Maintainers of the constrained
decoding libraries publicly disputed the comparison as unrepresentative
of correct usage. Two years of native structured output investment have
passed since. Treat this as must-measure on your own task, not as a
settled rule in either direction.

**The Leaderboard Illusion is disputed by the operator.** The arena
maintainers contest the characterisation of private testing and
sampling. That disagreement does not touch the usable conclusion, which
is that leaderboard position never justifies a model choice alone.

**Compiled prompts versus legible prompts has no controlled
comparison.** FRAG-AI-ML-LLM-25 optimises for measured quality, EV-0086
optimises for a human being able to read the context and see why the
model did what it did. Nobody has run the experiment. This is an open
question, not a preference we should dress as evidence.

## Binding, default, preference

**Binding.** These have evidence behind them and failure is expensive.

- Pin the model identifier to a version the provider will not move,
  never a moving alias, and record the
  published retirement date next to the call site. FRAG-AI-ML-LLM-19
  gives a sixty-day notice floor and tentative dates a year out;
  FRAG-AI-ML-LLM-18 shows behaviour moving inside a name's lifetime.
- Hold a private evaluation set the providers have never seen, and
  never tune against it. FRAG-AI-ML-LLM-16 and FRAG-AI-ML-LLM-26.
- Report every eval result with the exact prompt template and model id
  attached. A comparison run under different templates is not a
  comparison. FRAG-AI-ML-LLM-15.
- Never grade a model's output with the same model where the score
  selects between candidates, and where a family-mate judge is
  unavoidable, report the measured offset. FRAG-AI-ML-LLM-12.
- Any pairwise judge protocol runs both orderings and treats
  order-inconsistent pairs as disagreement, reported.
  FRAG-AI-ML-LLM-11.
- Score abstention explicitly. A rubric that pays a guess the same as
  an admission of uncertainty selects for confident error.
  FRAG-AI-ML-LLM-09.
- Groundedness against the retrieved context is measured separately
  from answer correctness. FRAG-AI-ML-LLM-06.

**Default, override with a recorded reason.**

- Retrieval before fine-tuning for anything that is a fact.
  FRAG-AI-ML-LLM-07. Fine-tuning is for form, not knowledge.
- BM25 or a hybrid as the first retriever; embeddings earn their place
  against it on your corpus. FRAG-AI-ML-LLM-05.
- Retrieval metrics split by stage, so a failure attributes to
  retriever or generator rather than to the system.
  FRAG-AI-ML-LLM-24.
- Dataset, solver and scorer kept as separate versioned things, so the
  model can be swapped without rewriting the eval.
  FRAG-AI-ML-LLM-23.
- Stable-prefix-first prompt layout with cache hit rate asserted in
  telemetry, because short prompts fail to cache silently.
  FRAG-AI-ML-LLM-20.
- Statistical reporting on evals: paired differences, clustered
  standard errors, a stated minimum detectable effect.
  FRAG-AI-ML-LLM-14.

**Preference, argue it either way.**

- Compiled prompt optimisation versus hand-written legible context.
- Trained cascade routing versus model self-assessment routing.
  FRAG-AI-ML-LLM-21 versus FRAG-AI-ML-LLM-04.
- Which evaluation framework. The abstractions matter, the tool does
  not.

## Where the evidence is thin

Named as open questions, not filled with confidence we do not have.

- Almost every controlled result here was measured on models that are
  now retired. Direction of effect probably transfers; magnitude
  almost certainly does not. Every number in this pack needs a
  re-measurement trigger, not a citation.
- There is no good evidence on evaluating agentic trajectories as
  opposed to single outputs. FRAG-AI-ML-LLM-23 and EV-0087 gesture at
  it; nobody has a validated method for grading a twenty-step run
  where the final artefact is correct and the path was wasteful.
- Judge validity for domain-specific correctness, as against general
  preference, is largely unmeasured. The eighty per cent human
  agreement in FRAG-AI-ML-LLM-10 is a general-chat number and should
  not be borrowed.
- Cost and latency management has almost no primary engineering
  literature. FRAG-AI-ML-LLM-21 is three years old and predates
  caching and batch pricing. This is the weakest-evidenced area in
  the domain and the pack should say so.
- Safety evaluation for agentic harm, as opposed to refusal behaviour,
  is covered by EV-0212 to EV-0217 rather than by anything here, and
  EV-0214 and EV-0215 show adaptive attackers break defences that pass
  static evaluation. A good safety grade is evidence about one prompt
  distribution.
