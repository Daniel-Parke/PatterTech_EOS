---
summary: What a reviewer or a checker can verify about documentation work, split into executable today and judgement
type: checks
tags: [content, delivery, ci, tooling]
kind: record
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0044, EV-0102, EV-0170, EV-0326, EV-0330, EV-0331, EV-0332, EV-0333, EV-0335]
review: 2027-08
---

# docs-dx pack checks

The evaluation criteria for work under `packs/docs-dx/PACK.md`. Each
row names what is verified, how, and whether a machine can do it today.
A check that needs a person is still a check.

## Executable today

These run in CI against the working tree with no network access and no
human input, unless a row says otherwise.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | Internal links resolve | Pinned link checker over the repository, internal invocation only, fails on the link-failure exit code | B1 |
| C-02 | Anchors resolve | Same run with fragment checking switched on, so a link to a renamed heading fails | B1 |
| C-03 | The link check itself ran | Runtime and configuration exit codes are handled separately from the link-failure code, so a crashed checker never reads as a clean run | B1 |
| C-04 | The link checker is pinned | The invocation names an exact release rather than a floating tag | B1 |
| C-05 | A moved or deleted page is not left dangling | For every path removed or renamed in the diff, either a redirect exists at the old path or no reference to it remains | B2 |
| C-06 | Fenced blocks execute | Every block in a nominated language under the documentation tree runs in a clean directory with no network, and the step fails on any non-zero exit | B3 |
| C-07 | Unexecuted blocks declare themselves | Every block neither executed nor carrying one of the permitted skip markers is a finding | B3 |
| C-08 | The snippet gate actually catches drift | A block calling a documented command with an unknown flag is injected, and C-06 must then fail | B3 |
| C-09 | Generated reference is current | The generator runs and the committed output must match byte for byte | B4 |
| C-10 | The generator is pinned | Generator version is fixed alongside the checker, so the C-09 diff cannot fire on formatting churn | B4 |
| C-11 | Failures are not empty | Every user-visible failure path produces a message above a minimum length that names the offending input | B5 |
| C-12 | Failure identities are declared | Every failure a caller may distinguish appears by the same name in the code, the tests and the interface documentation | B5 |
| C-13 | An agent entry file exists at the root path | Presence check, plus byte-identity with its sibling copy where the repository keeps two | B6 |
| C-14 | Commands named in the agent entry file are covered | Every command it names appears in an executed block or a test invocation | B6 |
| C-15 | External link checking does not block | Injecting a link to an unreachable host fails no step | D5 |
| C-16 | The blocking steps run offline | The blocking documentation job runs with network access disabled and still passes | D5 |
| C-17 | A running Unreleased section exists | Heading present in `CHANGELOG.md`, with at least one entry when the diff changes a user-visible surface | D3 |
| C-18 | README question set present | Headings or content covering all five questions in `packs/docs-dx/references/DOC_FORMS.md`: what, why, how, state and next | D2 |
| C-19 | Prose rules are advisory | The prose linter's step reports without failing the build unless the rule is on the promoted list | D7 |

C-01 through C-10 are the gate. C-11 and C-12 need a venture-specific
convention before they have teeth. C-08 and C-16 are the two rows that
prove the gate rather than run it, and a repository that has never run
them has an untested gate.

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The corrected instructions are the sequence a reader actually needs | Reviewer, because execution proves a block runs and never that it is the right block to show | B3 |
| J-02 | The prose around a working example is still true | Reviewer, because nothing verifies prose (EV-0330) | B3 |
| J-03 | The document's truth is in the right place | Reviewer, against `WG-DOCS-001` | D1 |
| J-04 | A confusing page is confusing because it mixes forms | Reviewer, using the four forms as a diagnostic rather than a layout | D1 |
| J-05 | A changelog entry states a consequence rather than restating the diff | Reviewer (EV-0333) | D3 |
| J-06 | A failure message would let a reader recover unaided | Reviewer, reading it cold | B5 |
| J-07 | The confidence tier on a suggested fix is honest | Reviewer, because an over-confident tier is worse than none | D4 |
| J-08 | The agent entry file is accurate, not merely present | Reviewer (EV-0044) | B6 |
| J-09 | Missing content is being addressed before style | Reviewer, because absence outranks form (EV-0326) | D6 |
| J-10 | A skip marker is a genuine constraint rather than an opt-out | Reviewer, watching the count of markers over time | B3 |
| J-11 | A prose rule has earned promotion to blocking | Reviewer, on observed false-fire rate (EV-0335) | D7 |

## How to read a failing check

C-09 and C-10 sit behind B4, the one requirement the ADR-0008 audit
left binding, and they are non-negotiable wherever their predicate is
true. C-01 to C-08 and C-11 to C-14 now sit behind defaults: the tests
are unchanged, and what changed is that a venture may decline one and
write down why. A failing C-05 is usually a half-finished rename,
and the fix is in the same change, not a follow-up. A failing C-08 or
C-16 means the gate is not trustworthy, which is worse than any single
broken link, because every other green run was uninformative.

A J-row that nobody performed is a J-row that failed. J-01, J-05 and
J-06 are the three most commonly skipped, and they are the three that
map directly onto the reader's experience.

## What this pack deliberately does not check

- Prose style beyond the mechanical subset, and nothing at all about
  voice, which `GOVERNANCE.md` owns.
- Page count, word count or any documentation coverage percentage.
- Whether documentation improved onboarding time. No evidence in this
  pack's set supports that measure, and turning a throughput number
  into a target is a known failure.
- Which directory structure documentation uses.
- External link reachability as a blocking condition, ever.

## Wiring note

Four things need a venture decision before this pack has teeth: the
pinned link checker and its invocation, the list of fence languages the
snippet gate executes, the permitted skip markers, and the minimum
failure-message contract behind C-11 and C-12. Everything else is
either a presence check or already present in a normal CI run. Nothing
here is executable until those four are written into the venture's own
gate configuration.
