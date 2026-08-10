---
summary: The ai-ml-llm pack applied end to end to a proposed prompt swap on a support ticket classifier, and the model swap after it
type: example
tags: [testing, delivery, data]
kind: exemplar
scope: estate
---

# EX-AIML-001: The prompt that looked better

A worked run of the pack against one concrete situation, from the
proposal to the verdict. Every rule that fires is named where it
fires.

## The situation

A venture runs a support ticket classifier: one function takes ticket
text and returns a label. It has been in production for four months.
A colleague has rewritten the prompt, tried about a dozen tickets by
hand, and says the new version is clearly better. They would also like
to move to a newer model next month. Nothing in the repository can
currently accept or refuse either change.

## Step 1: activation

Predicates `changes_prompt_or_model` and `evaluates_model_output` both
hold, so the pack loads. The classifier's output feeds a routing
queue and does not move money or contact anyone, so `ships_model_output`
holds but binding requirement B7 lands at its lowest floor: no
per-item approval, and a sampled human read of misroutes.

## Step 2: there is nothing to decide with

Guide `packs/ai-ml-llm/guides/GD-AIML-001-acceptance-evidence.md`. The
proposal is a demo. Twelve tickets chosen by the person who wrote the
prompt is not evidence, and the first work is not evaluating the new
prompt, it is building the thing that can evaluate any prompt.

Labels exist, because four months of tickets were routed and corrected
by hand. That rules option A of the guide in and means no model judge
is needed here: correctness is a label equality check, which is option
A of `packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md`.

## Step 3: the set, and the line down the middle

140 labelled tickets are pulled from four months of traffic. Before
anything is scored, they are split: 90 for selection, 50 held out.
The held-out file is named in the eval report and no prompt-selection
code may read it, which is binding requirement B3.

Reading fifty of the tickets by hand first produces something nobody
expected: 18 of the 140 are genuinely ambiguous, where two labels are
equally defensible and the human router had picked one arbitrarily.
That is default D1 doing its job. The rubric could not have been
written before somebody read bad output.

Those 18 change the design of the whole thing. A classifier that must
pick a label on those tickets is being scored on a coin flip, so the
output contract grows a third possibility: the function may abstain.
That is default D10, and it comes with an `abstain_rate` field beside
accuracy in every report from here on.

## Step 4: the entry point

One command at a recorded path, running headlessly, exiting zero,
writing JSON. Fields per `packs/ai-ml-llm/refs/EVAL_REPORT.md`:
accuracy, n, standard error, abstain_rate, the template path and its
content hash, the pinned model id, the dataset id and split, the
held-out set name, the seed and the decoding parameters.

The template hash is binding requirement B2 and it is the field that
makes the next step mean anything. The model responses are recorded
and replayed for the offline path, so two runs over the same tree give
the same accuracy and the same item count, which is default D8.

## Step 5: the comparison

Variant A scores 0.68. Variant B scores 0.72. The colleague reads that
as a win.

Default D2 says the comparison is paired over the same items, and the
report names the pairing. Paired, 20 tickets disagree between the two
variants: 12 where B is right and A wrong, 8 the other way. The net is
4 tickets out of 140, which is the four points. The standard error on
that paired difference is about 3 points, so the interval crosses
zero comfortably.

The minimum detectable effect at 140 items is about 7 points. The set
cannot resolve a 4-point gap, and it was never able to.

The verdict recorded is **unresolved**, per
`packs/ai-ml-llm/refs/EVAL_REPORT.md`. Not "B is better", and not "A
is better either". The honest next actions are to grow the set or to
accept B on grounds other than accuracy, recorded as such.

What actually happened: B was accepted on the grounds that it abstains
on 11 of the 18 ambiguous tickets against A's zero, which is a real
behaviour difference the eval can resolve, and the accuracy claim was
dropped. The decision is recorded with both numbers.

## Step 6: the model swap

Guide `packs/ai-ml-llm/guides/GD-AIML-005-model-lifecycle-and-cost.md`
and `packs/ai-ml-llm/refs/MODEL_MIGRATION.md`.

The existing call site used a moving alias, which is binding
requirement B4 broken. It is replaced with the pinned identifier this
provider publishes, taken from the provider's own id list rather than
guessed at from its shape, and the published retirement date is
recorded in a comment beside it. The
usage audit turns up a second caller in an operations script nobody
had counted.

The candidate model is run against the same frozen set, same
templates, same hashes, and the paired difference is reported. It
scores two points higher and abstains half as often, which is the
number that stops the migration: the same accuracy with far fewer
abstentions on a set with 18 known-ambiguous items means the new model
is guessing where the old one declined. That goes back for a
threshold change before the switch, not after it.

## Step 7: what runs from now on

The eval runs on every change to the prompt, the model or the
decoding parameters, and on a schedule against the pinned model,
because behaviour moves inside a name (requirement B4). Misrouted
tickets rotate into the set. Nothing rotates out because a variant
scored badly on it.

## What this run cost

An afternoon reading tickets, a day building the entry point, and one
uncomfortable conversation about a four-point gap that was not there.

## What it would have looked like without the pack

The new prompt merged on twelve hand-picked examples. The abstention
question never asked, so 18 tickets a month keep being routed on a
coin flip. The model swapped a month later on a vendor blog post, its
lower abstention read as an improvement, and the first evidence that
anything changed arriving as a support complaint about misrouted
tickets that nobody can trace to a cause, because no run recorded
which template or which model produced it.
