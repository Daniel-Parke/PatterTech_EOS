---
summary: What a reviewer or a script can verify about a discovery record, split into executable today and judgement
type: guide
tags: [product, testing, tooling]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0059]
review: 2027-08
review_by: 2027-08
---

# Product discovery pack checks

The evaluation criteria for work under `packs/product-discovery/PACK.md`.
Each row names what is verified, how, and whether a machine can do it
today. A check that needs a person is still a check.

Most of these run against a single file, the `discovery.md` for the
decision, whose shape is fixed in
`packs/product-discovery/refs/DISCOVERY_RECORD.md`.

## Executable today

These run over the record and the sources it names, and need no human
input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | The record exists and carries every mandatory section | Heading match on Problem, Evidence, Signal, Risks and Decision, exact strings | B1 |
| C-02 | The problem is not the solution restated | The requested feature name, taken from the intake note, does not appear in the Problem section, case-insensitive substring | B2 |
| C-03 | Every signal line is well formed | Each line under Signal matches the signal, threshold, source grammar | B3 |
| C-04 | Every named source exists | Each source value resolves to a file, table or instrument present in the repository or the named export | B3 |
| C-05 | All four risks are present and answered | Exactly four lines under Risks, opening value, usability, feasibility and viability, each carrying a substantive answer rather than a stub | B4 |
| C-06 | Every number is traceable | Extract every integer and decimal from the record; each must appear in a named source or be derivable by count from a stated filter | B5 |
| C-07 | Model-produced claims are labelled | Any citation of an unprovenanced persona or segment file carries the word unverified within the same line | B6 |
| C-08 | A TEST verdict declares its rules | The record carries a stopping rule line and a sample line | B7 |
| C-09 | The sample is not larger than the population | The sample integer is no greater than the user count in the named metrics source | B7 |
| C-10 | The verdict is one of three words | The first non-blank line under Decision is exactly BUILD, TEST or KILL | B8 |
| C-11 | The record was written before the work | The commit adding the record precedes the first commit implementing it | B1 |
| C-12 | Acceptance criteria parse in EARS order | Each criterion matches the while, when, shall, response clause order | D9 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The problem statement would survive a completely different implementation | Reviewer | B2 |
| J-02 | The signal would actually move if the goal were met, rather than being whatever the analytics package counts | Reviewer | B3 |
| J-03 | The threshold was chosen before the data, not fitted to it afterwards | Reviewer, from the commit order | B7 |
| J-04 | The viability answer is a written answer rather than an assumption in a suit | Reviewer, because this is the risk a solo operator skips | B4 |
| J-05 | The evidence filter is stated honestly, a read-and-classify count not presented as a search count | Reviewer | B5 |
| J-06 | The chosen option was compared against something real rather than against nothing | Reviewer | D3 |
| J-07 | The depth of the discovery matches the reversibility of the commitment | Reviewer | D1 |
| J-08 | The test is powerable at this traffic, rather than theatre with statistics attached | Reviewer, against the working rule in the samples reference | D5 |
| J-09 | A model was given the structuring job and not the origination job | Reviewer | D6 |
| J-10 | A KILL verdict was genuinely available, and the record would have reached it on different evidence | Reviewer | B8 |

## How to read a failing check

C-01 through C-10 are about the record itself and hold at every tier.
C-11 and C-12 are process conditions and are the two most likely to
carry a recorded lock-book override.

A J-row that nobody performed is a J-row that failed. J-04, J-08 and
J-10 are the three that a solo operator most often skips, and they are
the three that most often decide whether the work was worth doing.

## What this pack deliberately does not check

- Any prioritisation score. No framework located has a controlled
  evaluation, so gating on a score would gate on a convention. See
  `packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md`.
- Interview or participant counts as a target. The recruitment frame
  decides whether a discovery is wrong, and the count decides how much
  of the truth you got.
- Whether the record is long. A short record that reaches a verdict
  beats a long one that does not.
- Statistical analysis of an experiment readout. The data-analytics
  pack owns that, along with the asymmetric gate shape this pack
  borrows for its stopping rules (EV-0059).

## Wiring note

C-04, C-06 and C-09 are the three a venture must configure before the
pack has teeth, because each needs to know where the sources live: the
export directory, the metrics file and the intake queue. The rest are
string and structure checks over one file, and a checker can run them
the day the record is written.
