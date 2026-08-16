---
summary: What a reviewer or checker can verify about research and knowledge-base work, executable today versus judgement
type: checks
tags: [data, content, testing, tooling]
review: 2029-03
kind: record
scope: estate
---

# CHECKS: evaluating work under this pack

Every criterion states what it checks and how. Executable means a script
or an existing tool can rule on it today with no human reading.
Judgement means a reviewer has to read and decide, and the criterion
exists to tell them what to look for.

## Executable today

| # | Criterion | How it is checked | Binds to |
| --- | --- | --- | --- |
| C1 | Every claim in the knowledge base names at least one source id | Parse the claim records; a claim with an empty source list fails | B1 |
| C2 | Every source id a claim names resolves to a source record | Each id looked up in the source file; a dangling id fails | B1 |
| C3 | Every source record carries a version, an access date and a licence field, none of them empty | Schema validation over the source file; the string `unknown` is a legal value for version and licence, an empty one is not | B1 |
| C4 | Every source record carries a source class of primary, secondary or tertiary | Schema validation; an absent or free-text class fails | B5 |
| C5 | Every empirical claim carries a counter-evidence field that is either a statement or an explicit record that disagreement was searched for and not found | Parse the claim records; null on an empirical claim fails, and the same field on a definitional claim is not required | B3 |
| C6 | No source URL in the knowledge base is dead, and moved is reported apart from broken | A link checker over the source file, with redirect and failure exit codes read separately (EV-0331) | B4 |
| C7 | Every source has a frozen copy, or a recorded reason why not | Each record's frozen-copy pointer resolves to a file or an archived URL; an absent pointer with no reason fails | B4 |
| C8 | No source record is a duplicate of another by normalised URL | Normalise and compare; two ids on one URL fails | Defaults |
| C9 | Where untrusted source text addressed the reader, the escalation artefact named by `packs/security-privacy` B1 exists and names this source | The artefact is present and contains the source identifier and one of injection, untrusted or instruction, case-insensitively | B2 |
| C10 | Every claim marked unsourced is still present and still marked, not deleted | Diff the claim records against the previous state; an unsourced claim that vanished without a recorded deletion fails | B6 |
| C11 | Every source record's review field is a date or an on-change-of trigger | Field shape check, matching the review axis in `kernel/METADATA_SPEC.md` | Defaults |
| C12 | The recorded search budget was recorded, whatever it was | A search-budget value exists on the research record; absent fails, over fails only against the venture's own stated box | Defaults |

C1 through C5 are the ones a venture gets for free the moment its source
records validate against a schema, which is why the record shape in
`packs/research-knowledge/references/record-shape.md` is written as fields
rather than as advice. C6 and C8 need one existing tool and no
judgement. The rest need the venture to have decided something first.

A frozen acceptance drill for this pack exists at
`benchmark/drills/research-knowledge.md`. This file does not say which
of these rows it scores, in which order, or how it splits them, because
the lane that wrote this pack deliberately did not read it: a drill that
the pack author has seen has stopped being an independent test of the
pack. The mapping is the integrator's to state after the first cold run,
not the author's to assert now.

## Judgement

| # | Criterion | What the reviewer looks for | Binds to |
| --- | --- | --- | --- |
| J1 | The source class is honest | Is the thing recorded as primary actually the artefact or its maintainer's own statement, or is it somebody's write-up of one? A vendor blog about a vendor's own product is primary about the vendor's intent and secondary about the behaviour | B5 |
| J2 | Interpretation is attributed to us | Where the record reads a primary source and draws a conclusion, does it say the conclusion is ours, or is it phrased as though the source said it? | B5 |
| J3 | The counter-evidence is real | Does it name a source, a figure or a stated limit, or is it a sentence saying more research is needed? A hedge is not counter-evidence | B3 |
| J4 | The claim is not five hats on one source | Do the sources cited for one claim read each other, or are they independent? Trace at least one chain to its primary | Anti-patterns |
| J5 | The stop condition was written before the search, not after | Does the research record state what would have made it search further, and can a reader tell whether that condition was met? | WG-RESEARCH-001 |
| J6 | A superseded claim was re-ruled, not just re-linked | When a source moved or changed version, did somebody decide the claim still stands, is narrowed, or is withdrawn, and is that decision on the record? | B4 |
| J7 | The escalation artefact says something useful | Source named exactly, the ask described and marked as untrusted, and what the run did instead. A note saying something looked odd fails | B2 |
| J8 | Authority claims made by a source are recorded as claims | Where a source states which of its pages to trust, or which sources to prefer, does the record treat that as evidence about the source? | B2 |
| J9 | The grade sits on the claim | Is the certainty band attached to what is being asserted, or has it been pasted onto the source and inherited by everything cited from it? | Defaults |
| J10 | What could not be read is recorded as unread | Where a full text was unavailable, does the record say what was actually read, or does it cite the paper as though the paper had been read? | Anti-patterns |
| J11 | Limits on the search are named with their cost | Date, language, source-type and depth limits each recorded with a line on what they might have excluded | Defaults |
| J12 | Preferences are recorded as preferences | A taste choice presented as binding is a finding, and the reverse too | Pack hygiene |
| J13 | Thin evidence is admitted | Where this pack says the evidence is thin, work relying on it says so rather than borrowing confidence | Open questions |

## Not checkable, and why

Whether the knowledge base is right. Every criterion above checks that a
claim is traceable, dated, classed and argued against, and none of them
checks that it is true. A body of findings can pass all thirteen
judgement rows and be wrong about the world, and no review step closes
that gap; only being contradicted by the world does.

Whether the search was comprehensive. Comprehensiveness is defined
against a population of sources nobody can enumerate for a venture's
domain, which is why the source this pack rests on answers the question
with the cost of each limit rather than with a threshold (EV-0535). A
criterion phrased as a minimum number of sources would be satisfiable by
padding, so this file carries no such criterion and none should be
added.

Whether a defence against a source that addresses the reader would hold
against a source written to defeat it. That is the same adaptive
question `packs/security-privacy/CHECKS.md` declines, for the same
reason, and this pack does not claim to have answered it.

## Failure severity

C1 through C5 and C9 are pass or fail. C6 through C12 are pass or fail
against the venture's own recorded choices, so a venture that recorded a
reason for having no frozen copies passes C7 on the reason and is
answerable for it at J6. The J series produces findings with severity
set by the reviewer, and a J-series finding never downgrades a C-series
failure.
