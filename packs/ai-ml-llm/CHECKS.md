---
summary: What a reviewer or a script can verify about model-backed work, split into executable today and judgement
type: guide
tags: [testing, delivery, tooling]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0250, EV-0252, EV-0254, EV-0255, EV-0256, EV-0257, EV-0260]
review: 2026-11
---

# AI, ML and LLM pack checks

The evaluation criteria for work under `packs/ai-ml-llm/PACK.md`. Each
row names what is verified, how, and whether a machine can do it
today. A check that needs a person is still a check.

## Executable today

These run in CI against the diff and the working tree, and need no
human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | An eval entry point exists and runs headlessly | The recorded command exits zero on a clean tree and writes its report to the recorded path | B1 |
| C-02 | The report carries a metric, an item count and an interval | Field presence check for the primary metric, `n`, and either `stderr` or a low and high bound; a bare metric fails | B1 |
| C-03 | The report carries the template identity | Field presence for the template path and its content hash, and string equality of the hash against the file on disk | B2 |
| C-04 | The report carries a pinned model id | Field presence, and a match against the configured pinned-id pattern for each provider in use | B2, B4 |
| C-05 | No moving model aliases in source | Pattern scan over the source for the configured moving-alias forms, for example a `latest` suffix or a bare family name | B4 |
| C-06 | A retirement date is recorded beside every pin | Every pinned identifier has a retirement date within a few lines of it | B4 |
| C-07 | The run is reproducible | Two runs over the same tree produce the same primary metric and the same item count | D8 |
| C-08 | The held-out set is not read by the tuning path | Grep of prompt-selection and optimiser code for the held-out filename returns zero matches, and the report names the file | B3 |
| C-09 | Comparisons are paired | The comparison report carries a field naming the pairing key | D2 |
| C-10 | The gate states what it can detect | The report carries a minimum detectable effect at the current sample size | D2 |
| C-11 | Abstention is reachable and reported | The output type admits an abstention, the report carries `abstain_rate`, and at least one item in the recorded run abstains where the set contains known-ambiguous items | B6 |
| C-12 | Judge runs are labelled | Where a model produced the score, the report carries the judge model id, the human-labelled sample size and the measured agreement | B5 |
| C-13 | Pairwise judging ran both orderings | The judge report carries a per-ordering count and an order-inconsistency rate | B5 |
| C-14 | Retrieval metrics are split by stage | A retrieval system's report carries retriever-stage and generator-stage fields rather than one score | D5 |
| C-15 | Cache assumptions are asserted | Production telemetry reports a cache hit rate rather than assuming caching is on | D7 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later, none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The acceptance set measures the thing the product cares about | Reviewer, because coverage of the failure you fear cannot be checked by field presence | B1 |
| J-02 | The verdict matches the arithmetic | Reviewer, in particular that a difference inside the noise was recorded as unresolved rather than as a win (EV-0255) | D2 |
| J-03 | The rubric was derived from graded outputs rather than written first | Reviewer (EV-0254) | D1 |
| J-04 | The held-out set is genuinely unseen | Reviewer, because a file the provider has never seen cannot be proved by grep (EV-0257) | B3 |
| J-05 | The judge is not a family-mate of the model under test, or the offset is reported | Reviewer | B5 |
| J-06 | The abstention threshold is right for the product | Product owner, because the evidence says score abstention and not where to set it (EV-0250) | B6 |
| J-07 | Consequential output had a person in front of it | Human, at the floor set by `kernel/GUARD_SPEC.md` | B7 |
| J-08 | Groundedness failures were read, not just counted | Reviewer, reading spans against the retrieved context | D5 |
| J-09 | Scope of a borrowed number | Reviewer, that no benchmark figure was promoted beyond its population | Whole pack |
| J-10 | The migration was judged on abstention and behaviour, not accuracy alone | Reviewer | B4 |

## How to read a failing check

C-01 to C-06 are the floor. Without them there is no evidence at all,
and no other row means anything. C-07 to C-11 are what turn a number
into a verdict, and they are the rows most often skipped under time
pressure. C-12 and C-13 apply only where a model grades. C-14 and
C-15 apply only to retrieval systems and to production traffic
respectively.

A J-row that nobody performed is a J-row that failed. J-02 and J-09
are the two a reviewing agent can do well; J-06 and J-07 are the two
it cannot, because both are product and accountability decisions
rather than measurements.

## What this pack deliberately does not check

- Which evaluation library is used.
- Absolute accuracy against any published benchmark. Public numbers
  are an upper bound and never an acceptance condition
  (EV-0257).
- Prompt wording, style or length, beyond the requirement that the
  template is versioned and hashed.
- Cost per call as a gate. It is a number to watch, and the evidence
  base for cost machinery is too old to bind on.

## Wiring note

C-05, C-08 and C-11 are the three a venture has to configure before
the pack has teeth, because each needs a project-specific pattern: the
pinned-identifier pattern for the providers in use, the held-out
filename, and the ambiguous-item subset. Take that first pattern from
the provider's own published id list rather than writing a date match.
A date match is wrong for at least one major vendor, whose current ids
carry no date and are pinned all the same, so it would fail exactly
the identifiers the vendor tells you to send. The rest are field-presence
checks over a report the venture already has to produce, or a second
run of a command that already exists.
