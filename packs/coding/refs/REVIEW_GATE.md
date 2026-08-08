---
summary: What the machine gate must contain, how findings are split, and how a human reads a diff when one does
type: foundation
tags: [delivery, ci]
kind: fact
scope: estate
sources: [EV-0069, EV-0070, EV-0164, EV-0165, EV-0166, EV-0167, EV-0181]
volatility: slow
review: 2027-02
---

# Review gate reference

Level 3 material behind binding requirement B5 and default D1. Guide:
`packs/coding/guides/GD-COD-002-review-gate.md`.

## The machine half

The gate is binding under every routing decision. Four properties make
it work, and dropping any one of them is how gates die.

**Diff-aware.** Rules run against what the change introduced, not
against the whole repository. A gate that reports the accumulated
history on every run drowns the new finding in the old ones and gets
disabled within a month (EV-0070).

**Rules as code, in the repository.** Policy is written as executable
rules that look like the code they match, versioned with the code, and
reviewable as a diff (EV-0070). Policy carried in a vendor console is
policy nobody can review.

**Blocking split from monitoring.** Two lists. Blocking findings stop
the merge. Monitoring findings are recorded and reviewed at retro. A
gate where everything blocks becomes a gate where nothing does.

**Repository state, not repository claims.** Health checks read what the
repository actually does, such as whether dependencies are pinned and
whether branch protection is on, rather than what its documentation
says (EV-0069).

## Why the gate is not optional

Generated code is not security-neutral by default. In a systematic
prompt-completion experiment across 89 security-relevant scenarios
producing 1,689 programs, roughly 40 per cent contained a vulnerability,
and the rate varied with the weakness class, the prompt and the domain
(EV-0181).

Scope: a 2021 model on deliberately security-loaded scenarios. Later
models score better and the headline number should not be applied to
current tooling or to ordinary code. The structural claim survives
regardless: generation quality varies with prompt and domain in ways the
author cannot see, so the check has to sit downstream of generation.

## Minimum contents of the gate

1. The test suite, including the oracle authored under requirement B1.
2. Static analysis and policy rules over the diff, blocking set separate
   from the monitoring set.
3. The error-path scan from `packs/coding/refs/ERROR_PATH.md`.
4. The declared-failure-name string equality check.
5. Dependency and repository health checks.
6. A duplicate-block count for touched files, compared with the count
   before the change.
7. Formatter and linter, settled by configuration, never by a reviewer.

## The human half

When a human does review, the rules are short.

**Approve on the health gradient.** Approve once the change definitely
improves overall code health even when it is imperfect. Refuse only what
definitely worsens it (EV-0164). A perfection bar stalls the queue and
buys nothing.

**Separate design from style.** Design judgement is arguable on
engineering grounds and belongs in review. Style is settled by the style
guide and the formatter, and does not (EV-0164).

**Read the error paths first.** That is where the catastrophes are.

**Keep changes small.** Small changes are the mechanism that makes
review affordable at all; a reviewer can find five minutes repeatedly
and cannot find thirty minutes once (EV-0164, EV-0165).

**Do not review names for uniformity.** Review which concepts a name
encodes and leave the wording. See the preferences section of
`packs/coding/PACK.md`.

## What review does not deliver

The stated top motivation for review is finding defects, and the
measured outcome is that reviews yield far fewer defect findings than
expected, with most of the value arriving as knowledge transfer, team
awareness and alternative solutions. The binding constraint on review
quality is the reviewer's understanding of the change and its context
(EV-0166).

Two consequences for a solo operator directing agents. Blanket human
review buys little, because the knowledge transfer has no second person
to reach. And a reviewer approving a diff they do not understand is
producing a signature, not a review.

## The archived-source caveat

The health-gradient guidance comes from a repository archived read-only
in November 2025 (EV-0164). It is a fixed historical artefact and will
not track agentic review practice. The case study behind the small-change
and low-iteration figures is from 2018 and predates machine authorship
entirely (EV-0165). The argument that agents supersede human inspection
is a 2026 preprint with no new data (EV-0167). There is no controlled
measurement of reviewing machine-written diffs. Treat this whole section
as the best available and not as settled.
