---
summary: The fields an eval report must carry, the paired comparison arithmetic, the held-out split and what a verdict may say
type: foundation
tags: [testing, delivery, data]
kind: fact
scope: estate
sources: [EV-0250, EV-0255, EV-0256, EV-0257, EV-0264, EV-0265]
volatility: slow
review: on-change-of:EV-0255
---

# Eval report reference

Level three detail behind binding requirements B2 and B3, defaults D9
and D10, and Wargame
`packs/ai-ml-llm/wargames/WG-AIML-002-acceptance-evidence.md`.

## The entry point

One headless command at a recorded path, exiting zero on a completed
run and non-zero on a failed one, writing a machine-readable report to
a recorded location. No notebook, no manual step, no copy and paste
from a terminal into a pull request description. If a person has to be
present, it is a demo.

## Required fields

Every report carries all of these. A report missing any one of them
cannot accept or refuse a change.

| Field | Why |
| --- | --- |
| `accuracy` or the task's primary metric | The result |
| `n` | The item count, without which the metric means nothing |
| `stderr` or `ci_low` and `ci_high` | An eval is a sample from an unseen super-population (EV-0255) |
| `abstain_rate` | Accuracy alone selects for confident error (EV-0250) |
| `prompt_template_path` and `prompt_template_sha256` | A run under a different template is a different experiment (EV-0256) |
| `model_id` | Pinned identifier, never a moving alias |
| `dataset_id` and `split` | Which items, and which side of the held-out line |
| `held_out_set` | Named so a reader can see what was not tuned against |
| `seed` and decoding parameters | Reproducibility |
| `run_started` and duration | Cost and staleness |

Where a model judge produced the score, add `judge_model_id`,
`judge_agreement_n` and the measured agreement against the
human-labelled sample.

## The paired comparison

Two variants are compared on the same items, and the report names the
pairing explicitly, for example `paired_on: item_id`. Paired
differences remove item-difficulty variance and raise power sharply
against comparing two independent means (EV-0255). Where
items share a passage or a source, cluster the standard error at that
level rather than at the item.

The report also states the minimum detectable effect at this sample
size. A gate that has not said what difference it can detect cannot
refuse anything, and cannot honestly accept anything either.

## What a verdict may say

Three verdicts are legitimate:

- **Accept.** The difference exceeds the minimum detectable effect in
  the intended direction.
- **Reject.** The difference exceeds it in the wrong direction.
- **Unresolved.** The difference is inside the noise, or the sample
  cannot resolve it. This is a result, and it is the correct answer
  more often than anyone likes.

A verdict of "B looks better" on a three-point gap over a hundred and
twenty items is none of these. Either the arithmetic supports the
claim or the honest report is that the set is too small, and the next
action is more items rather than a decision.

## The held-out split

Two files. One the prompt-selection and optimiser path may read, one
it may not. The report names the held-out file, and a check greps the
selection code for its filename and fails on any match. Public
benchmark numbers are an upper bound and a private set is the only
thing that measures your system (EV-0257).

Rotate items into the held-out set from production failures. Never
rotate them out because a variant scored badly on them.

## Structure of the eval itself

Dataset, solver and scorer stay separate and versioned
(EV-0264), so a model swap does not rewrite the eval and a
scorer swap does not rewrite the dataset. For retrieval systems, split
the metrics by stage: context precision and recall for the retriever,
faithfulness and answer relevance for the generator
(EV-0265). One end-to-end score cannot tell you which half
to fix.

## Reproducibility

Two runs over the same tree give the same primary metric and the same
item count. Pin the model id, fix the decoding parameters, record the
seed, and hold recorded or stubbed responses for the offline path.
This is a decision rather than a measured finding, made because a
number nobody can reproduce cannot be argued about and a gate that
costs real money per run gets skipped. Where the acceptance condition
genuinely needs live sampling, report the run-to-run variance instead
and say so in the report.

## What this reference does not settle

The interval arithmetic assumes roughly independent items and a scalar
score, and it does not model judge error, so intervals from that
method alone are too narrow when a model does the grading
(EV-0255). Agent trajectories, where the unit of observation
is ambiguous, have no validated method here at all.
