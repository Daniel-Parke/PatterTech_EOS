---
summary: Prompt layout mechanics, the caching against position conflict, context budget and how to measure usable length
type: foundation
tags: [perf, data, delivery]
kind: fact
scope: estate
sources: [FRAG-AI-ML-LLM-02, FRAG-AI-ML-LLM-03, FRAG-AI-ML-LLM-04, FRAG-AI-ML-LLM-20, EV-0086]
volatility: fast
review: on-change-of:FRAG-AI-ML-LLM-20
---

# Context layout reference

Level three detail behind default D7 and guide
`packs/ai-ml-llm/guides/GD-AIML-004-prompt-maintenance.md`.

## The two rules that fight

**Caching wants stability first.** A cached prefix read is charged at
a tenth of base input while a cache write costs a quarter to a full
multiple more, and the minimum cacheable prefix varies by model, so a
prompt whose first bytes change per request pays the write price and
never collects the read discount. Short prompts fail to cache with no
error at all, which is why the cache token counts have to be read back
from the response rather than assumed (FRAG-AI-ML-LLM-20).

**Position wants evidence at the edges.** Accuracy is highest when the
needed evidence sits at the very start or the very end of the context
and degrades markedly in the middle, including on models sold as
long-context (FRAG-AI-ML-LLM-02).

Both cannot own the front of the prompt.

## The resolution

Stable system material first, retrieved evidence last, the question
last of all. That gives the cache a stable prefix and gives the
evidence the tail edge, which is the edge you can control per request.
The front edge goes to material that does not change, and the
measurement that matters is whether anything at the front was ever
carrying weight. Ablate it: remove the front block, re-run the eval,
and see whether the score moves. If it does not, the block is paying
rent it does not earn.

Both numbers belong in telemetry: cache hit rate, and the eval score
under the current layout. A layout change is a change to the prompt
artefact and goes through the same acceptance path as any other
(binding requirement B2).

## Context budget

The advertised window is a capacity limit. Reliability falls as input
grows even on tasks that are trivially easy at short length, and the
fall is modulated by how semantically close the needed material is to
the question, by whether plausible distractors are present, and by how
the haystack is structured (FRAG-AI-ML-LLM-03). A two hundred thousand
token window can show serious loss well before it is full.

Measure your own usable length. Take the real task, hold the needed
material fixed, grow the surrounding material in steps, and plot the
score. Pin the budget below the point where it starts to fall, and
re-measure on every model change, because the number belongs to the
model and not to the task.

## Practical consequences

- More context is a cost with a quality risk attached, not a free
  improvement. Adding a document to the prompt needs the same
  justification as adding a dependency.
- Compaction, structured notes and just-in-time retrieval are how long
  work stays inside a budget (EV-0086).
- Distractors are worse than volume. Retrieving five plausible-looking
  wrong documents does more damage than retrieving one right one and
  nothing else.
- Where the corpus fits and the tokens are affordable, whole context
  can beat retrieval on average quality (FRAG-AI-ML-LLM-04). The tail
  is the part to check before believing the average.

## Evidence boundary

The position results are 2023-vintage models on single-needle
retrieval and short-answer questions, which do not represent
synthesis, code editing or agent trajectories, and the degradation is
not the tidy curve the headline suggests once distractors and
similarity are varied (FRAG-AI-ML-LLM-03). The context-rot work comes
from a retrieval vendor with an interest in long context looking
unreliable, published with an open replication toolkit and not peer
reviewed. The caching numbers are one vendor's pricing table as read
on 2026-08-03 and change without notice, so re-read before putting
them in a cost model.
