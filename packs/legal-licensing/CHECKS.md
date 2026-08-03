---
summary: What a reviewer or a checker can verify about licensing and data-protection routing, split into executable today and judgement
type: guide
tags: [security, pii, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [FRAG-LEGAL-LICENSING-02, FRAG-LEGAL-LICENSING-08, FRAG-LEGAL-LICENSING-09, FRAG-LEGAL-LICENSING-10, FRAG-LEGAL-LICENSING-12, FRAG-LEGAL-LICENSING-13, FRAG-LEGAL-LICENSING-14]
review: 2026-12
review_by: 2026-12
---

# legal-licensing pack checks

The evaluation criteria for work under `packs/legal-licensing/PACK.md`.
Each row names what is verified, how, and whether a machine can do it
today. A check that needs judgement is still a check; it is just a
person's job. None of these is a legal opinion.

## Executable today

These run in CI against the diff and the working tree, and need no
human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | The repository declares its own licence | A licence file exists at the root and the manifest carries an identifier or an explicit reference | B1 |
| C-02 | Declared and actual agree | The identifier in the manifest matches the licence file's text as identified by the scan | B1 |
| C-03 | The inventory exists and is not empty | The scan step produced an inventory with an entry count above zero and above the lockfile's direct dependency count | D2 |
| C-04 | Every component has a licence value | No entry resolves to an unasserted, none or empty value unless that component is named in `LICENCE_DECISION.md` | B2 |
| C-05 | No unmade choices | No verdict column contains a choice expression; each is exactly one identifier | B3 |
| C-06 | Buckets are applied | Every identifier maps to a bucket, and every bucket-two or bucket-three component has a dated `LICENCE_DECISION.md` entry naming the identifier, the triggering event and the disposition | D1, B4 |
| C-07 | Vendored directories carry provenance | Every vendored path has a licence file and a provenance note naming source and revision | D5, B2 |
| C-08 | Per-file declaration on published repositories | The declaration lint passes with no unlicensed or uncovered file | D3 |
| C-09 | Attribution reaches the artefact | The notice file in the built artefact contains an entry for every bucket-one component requiring attribution | D1 |
| C-10 | Inbound provenance | Every commit in the change carries a `Signed-off-by` line with a name and a bracketed address, checked over the whole branch rather than the tip | B6 |
| C-11 | The notice checklist | The privacy notice file exists and contains all ten checklist markers and both complaint routes | B5 |
| C-12 | Registration recorded | A record exists naming either the payment or the schedule exemption relied on, with a date | B5 |
| C-13 | The decision record is current | The newest `LICENCE_DECISION.md` entry is no older than the most recent change to the dependency manifest | B4 |
| C-14 | No fee figure is quoted | No pack or venture file states a charge amount sourced from this pack | B5 |
| C-15 | Escalation was not answered | No `LICENCE_DECISION.md` entry resolves an escalation trigger; each carries a handover reference instead | B7 |
| C-16 | The run stayed inside its budget | Elapsed time is recorded with the decision and is within the stated passes | D8 |
| C-17 | The work still shipped | The venture's own test suite passes on the tip, so a clean licence result was not bought by refusing the feature | D8 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | Whether the component is modified, and where the program boundary sits behind an internal service | Lawyer, because the licence text resolves neither | B4, B7 |
| J-02 | Whether the venture's shape is distribution, hosting or both | Human, once, recorded in the lock-book | B4 |
| J-03 | Whether the recorded choice from a dual-licensed component is one we can actually comply with | Reviewer | B3 |
| J-04 | Whether an attribution obligation is discharged in the form the recipient actually receives | Reviewer | D1 |
| J-05 | Whether an unidentified component was resolved or merely reclassified to make the check pass | Reviewer | B2 |
| J-06 | Whether the lawful basis is correct and the processing fair, which the statute does not state | Human, with advice where it is not obvious | B5 |
| J-07 | Whether the notice is readable by the people it is for | Human | B5 |
| J-08 | Whether the imported bucket table still matches this venture's promise downstream | Human, at review | D1 |
| J-09 | Whether an escalation trigger has fired | Human, and the bias is toward yes | B7 |
| J-10 | Whether the venture places product on the EU market in the course of a commercial activity | Human, recorded with reasoning | D7 |
| J-11 | Whether provenance for agent-written work was recorded rather than authorship assumed | Reviewer | B6 |

## How to read a failing check

C-04, C-05, C-07 and C-11 are blocking and have no negotiated version.
An unidentified component and a missing notice are the two findings
this pack exists to stop, and both are cheap to fix before merge and
expensive afterwards.

C-03 exists because of a specific failure: a scan that ran, found
nothing and was read as a pass. An empty inventory is a broken step
rather than a clean tree.

C-15 exists because the most likely way this pack fails is not a missed
finding. It is an agent that found the hard question and answered it.

C-17 exists because a run that refuses the feature produces a perfect
licensing result and no product. That is a failure with a clean report.

## What these checks do not prove

A green run proves declarations are present, consistent and bucketed. It
does not prove they are correct: a fully conformant repository can
declare the wrong licence (FRAG-LEGAL-LICENSING-08), and detection
reports what a file claims about itself
(FRAG-LEGAL-LICENSING-10). Read the whole set as evidence that the
questions were asked, never as a compliance result.
