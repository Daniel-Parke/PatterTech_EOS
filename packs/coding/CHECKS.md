---
summary: What a reviewer or a checker can verify about coding work, split into executable today and judgement
type: guide
tags: [delivery, ci, tooling]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0006, EV-0069, EV-0070, EV-0164, EV-0174, EV-0175, EV-0180]
review: 2027-05
review_by: 2027-05
---

# Coding pack checks

The evaluation criteria for work under `packs/coding/PACK.md`. Each row
names what is verified, how, and whether a machine can do it today. A
check that needs judgement is still a check; it is just a person's job.

## Executable today

These run in CI against the diff and the working tree, and need no
human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | An oracle commit precedes the implementation commit | History walk: the first commit touching a changed source file is preceded by a commit adding or changing a test for it | B1 |
| C-02 | The oracle actually failed before the fix | The new test is run against the parent commit and must fail there and pass on the tip | B1 |
| C-03 | Behaviour is pinned before structure moves | A characterisation or approval test for the touched file exists and passes at both the parent commit and the tip | B2 |
| C-04 | No swallowed errors | Pattern scan over changed files for bare catch-alls and for catch bodies that are only a pass, a continue or a bare default return | B3 |
| C-05 | Declared failure names agree | String equality of every declared failure name across the module, the tests and the interface documentation, no synonyms | B4 |
| C-06 | The suite is green and not empty | Test runner exits zero and reports a collected count above the floor set by the venture | B1 |
| C-07 | The fix was not bought with duplication | Duplicate-block count for each touched file is no higher than at the parent commit, with the tool version and threshold pinned in the venture config | Default D5 |
| C-08 | The gate ran diff-aware | Policy and security rules report against the diff only, blocking findings separate from monitoring findings | B5 |
| C-09 | Repository health | Automated repository state checks pass at the venture's configured level | B5 |
| C-10 | Style is settled by tooling | Formatter and linter clean, with configuration in the repository | D2 |
| C-11 | Tier declaration matches the diff | Router recomputation at the gate does not raise the tier above what was declared | D1 |
| C-12 | Trunk conditions | Branch age at merge, active branch count, and merge cadence sampled against the venture's thresholds | D3 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The oracle states intent rather than restating the implementation | Reviewer | B1 |
| J-02 | The test is an assertion and not an observational print dressed as one | Reviewer, because a passing test that would pass regardless is syntactically fine (EV-0006) | B1 |
| J-03 | An approved file change is a deliberate behaviour decision rather than a reflexive stamp | Reviewer (EV-0180) | B2 |
| J-04 | A translation did not lose information the caller needed | Reviewer (EV-0175) | B3 |
| J-05 | The declared failure set is one callers can actually recover from differently | Reviewer | B4 |
| J-06 | The change definitely improves overall code health | Reviewer, on the health gradient rather than a perfection bar (EV-0164) | D2 |
| J-07 | The refactor was demanded by a pending change | Reviewer | D5 |
| J-08 | Architectural fit | Human, at R2 and above, and the known weak spot of agent review | D1 |
| J-09 | Accountability | Human, at R3, because nobody else can be answerable | D1 |

## How to read a failing check

C-01 through C-07 are about the change itself and are non-negotiable at
every tier. C-08 and C-09 are the gate and are non-negotiable at every
tier. C-11 and C-12 are process conditions and are the two most likely
to carry a recorded lock-book override.

A J-row cannot fail silently, because a J-row that nobody performed is a
J-row that failed. At R0 and R1 the J-rows are performed by a reviewing
agent kept separate from the author, with a human sample. At R2 and
above a person performs J-06 through J-09 directly.

## What this pack deliberately does not check

- Naming, beyond whether the concepts encoded are the right ones. Do not
  gate on naming uniformity.
- Coverage percentage as a target. The delivery-testing pack owns test
  depth.
- Commit message grammar, unless the venture's release automation
  consumes it.
- Absolute duplication level. Only the direction across a single change,
  per C-07.

## Wiring note

C-04, C-05 and C-07 are the three checks a venture has to configure
before the pack has teeth, because each needs a tool choice and a pinned
version. The rest are either history walks or already present in a
normal CI run. Nothing here is executable until the venture writes those
three into its own gate configuration.
