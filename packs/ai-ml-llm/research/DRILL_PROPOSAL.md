---
summary: Cold-agent acceptance drill for the AI, ML and LLM pack, build the gate before tuning the classifier
type: example
tags: [eos, testing]
---

# Drill proposal: AI, ML and LLM pack

One run, one cold agent, no human turns after the prompt. No network.

## Fixture

`drills/ai-ml-llm/fixture/` at a pinned commit, copied to a temp dir
per run. A support-ticket classifier: `classify.py` with one public
function `classify(ticket_text) -> {"label": str, "abstain": bool}`
that never abstains, `prompt.txt` (variant A), `prompt_b.txt`,
`labelled.jsonl` (120 tickets, 18 genuinely ambiguous),
`stub_client.py` (a deterministic offline model stub keyed on prompt
hash and input, so runs are reproducible with no network), and a
two-line `README.md` with no accuracy claim. The stub is built so
variant A scores 0.71 and variant B 0.74, a gap the sample cannot
resolve.

## Prompt given to the agent

"Read the AI, ML and LLM pack. Someone wants to swap this classifier's
prompt for a variant they say is better, and later swap the model.
Make it possible to accept or reject such a change on evidence. Follow
the pack."

## Machine-checkable criteria

All must pass, graded against the final working tree.

1. An eval entry point runs headlessly and exits 0, at a recorded path.
2. Its output is JSON containing `accuracy`, `n`, and an interval or
   standard-error field. A bare accuracy fails.
3. The output records the prompt template identity (path plus content
   hash) and the model identifier, checked by string equality against
   the hash of `prompt.txt`.
4. Two runs on the same tree give byte-identical `accuracy` and `n`.
5. The A versus B comparison is paired over the same items, evidenced
   by a field naming the pairing, and the verdict on 0.71 versus 0.74
   is not "B is better". Either "no significant difference" or an
   explicit statement that the sample cannot resolve it passes.
6. `classify` can return `abstain: true`, and at least one of the 18
   ambiguous tickets is abstained on in the recorded run.
7. The output reports an `abstain_rate` field beside accuracy.
8. A held-out split exists that the tuning path never reads: grep of
   the prompt-selection code for the held-out filename returns zero
   matches, and the eval report names it.
9. Every model identifier in the source matches the dated-id regex in
   the drill config. No moving aliases.
10. Under 20 minutes wall-clock, zero outbound calls, enforced by
    running with networking disabled.

## Scoring and freeze

Pass requires all ten. Criteria 1 to 5 test evaluation-first with
honest statistics, 6 and 7 the abstention rule, 8 the private held-out
rule, 9 model pinning. Fixture commit hash, stub score table, model-id
regex and grader script are frozen by the integrator before any pack
content is authored, so the pack cannot be written to the drill.
