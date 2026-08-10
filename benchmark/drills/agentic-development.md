---
summary: Cold-agent acceptance drill for the agentic development pack, topology selection under pressure
type: example
tags: [eos]
---

# Drill proposal: pick the topology, justify it, bound it

Single run, cold agent, no prior conversation. The agent is given only
the pack and the brief below, and writes one file,
`drill-out/TOPOLOGY_DECISION.md`. No network, no repo edits elsewhere.

## The brief handed to the agent

A venture needs a nightly job that takes a queue of 40 independent
customer support transcripts, extracts structured complaints from each,
then writes one merged weekly report file and opens a pull request. The
transcripts are read-only. The report file is shared. Runs must survive
a process restart mid-batch. Opening the pull request is externally
visible. There is a schema validator for the extraction output and no
oracle for the report prose.

## Deterministic acceptance criteria

The output file is checked mechanically. All must hold.

1. Front-matter present with `summary`, `type` and a `tags` list
   containing `eos`.
2. Contains a level-two heading `## Topology` whose section names
   exactly one topology from the pack's ten-item list for extraction and
   one for the merge step.
3. The extraction topology selected is `fan-out/fan-in`; the merge and
   pull-request stage is `human checkpoint` or a sequential pipeline
   terminating in a human checkpoint.
4. A `## Pressures` section names at least three of: decomposability,
   shared-state coupling, oracle quality, reversibility, latency, cost,
   context pressure, failure localisation, and ties each by name to the
   choice.
5. States the single-writer rule explicitly: the merged report is
   written by exactly one agent, and the string `single-writer` or
   `one writer` appears.
6. A `## Bounds` section gives numeric limits for at least two of
   turns, tokens, wall-clock, with units.
7. A `## Resumability` section names checkpoint or event-log resumption
   and states that resumed side effects must be idempotent.
8. A `## Verification` section places the schema validator on the
   extraction output and states that the prose has no external oracle,
   so no evaluator-optimizer loop is claimed for it.
9. A `## Approval` section requires human approval before the pull
   request is opened.
10. Cites at least four evidence ids matching `EV-\d{4}` or
    `FRAG-AGENTIC-DEVELOPMENT-\d{2}`, at least two of them from the
    pack's own fragment set.
11. Voice check passes: no em-dashes, no exclamation marks, British
    spellings, and the file is 120 lines or fewer.

Pass requires all eleven. A checker script asserts each as a regex or
line-count test over the single output file; nothing is graded by a
model.
