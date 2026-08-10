---
summary: How do you change code nobody can specify, read carefully, pin behaviour, reconstruct a spec or rewrite behind a contract?
type: guide
tags: [testing, delivery, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0008, EV-0094, EV-0177, EV-0179, EV-0180, EV-0182]
review: 2027-10
---

# GD-COD-004: How do you change code nobody can specify?

## The question

You have to change code whose intended behaviour is not written down
anywhere. That is now the normal case, not the exception: it covers
inherited code, and it covers code an agent wrote last month that nobody
read closely. The fork is what you put in place before you touch it, and
that is a question about how you find out you broke something.

## It depends on

- Is current behaviour deterministic enough to record?
- Is the change adding behaviour, or moving structure, or both?
- How would you find out you broke it? In CI, in an hour, or from a
  customer?
- Is anyone depending on the current bugs?

## Options

### A. Read it and change carefully

No net, just attention. Buys: no setup cost. Costs: the failure is
silent and arrives later, and attention does not scale to code a model
wrote faster than you can read it. This is the option that quietly
becomes the default when nobody rules.

### B. Characterisation pin, then change

Capture current output for representative inputs as an approved
artefact, diff every run against it, and require a deliberate approval
for any change to it (EV-0180). Buys: a behaviour net in minutes,
which is the precondition for safe structural change. Costs: it records
current bugs as if they were intent, so it is a net and never a
specification, and approvals rot into reflexive stamps unless approving
is treated as a real act (EV-0094).

### C. Reconstruct the specification, then test to it

Work out what the code was meant to do, write that down, and test
against the written intent rather than the observed output. Buys: tests
that mean something, and a specification that outlives the change.
Costs: slow, and where the reconstruction is wrong you have replaced an
undocumented behaviour with a documented misunderstanding.

### D. Rewrite behind a declared contract

Freeze the interface, write a fresh implementation, run both against the
same inputs until they agree, then swap. Buys: an escape from code that
cannot be reasoned about. Costs: the most expensive option, and the
comparison harness is itself a project.

## Decision rule

- You are moving structure and not changing behaviour: B first, always.
  The pin lands in its own commit before the structural commit.
- You are adding behaviour to code with no specification: B for what
  exists, then a failing test for the new behaviour, then the
  implementation. Three commits, that order.
- The behaviour is genuinely misunderstood by everyone, and the code is
  small: C.
- The module is beyond reasoning and the interface is stable: D, and
  route it as a project rather than a change.
- A alone is not an option on any code with a caller you did not write.

## Default

B. It is the cheapest thing that turns a silent failure into a loud one,
and the cost of getting it wrong on inherited code is measured in
incidents rather than in minutes.

## When to refactor at all

Refactor when a pending change demands it. Developer-reported motivation
for detected refactorings is overwhelmingly situational, driven by a
specific change being made or by duplication met while working, rather
than by detected smells (EV-0177, Java open source, 2016, self-reported).
A smell-detector backlog is therefore a poor model of the work. The
counter-signal worth watching is that refactoring volume appears to fall
sharply in machine-assisted codebases (EV-0179, vendor study, direction
only), which suggests the change-driven trigger gets skipped rather than
that the model is wrong. Instrument your own repository if you want to
know.

## The rule that stops a fix buying decay

A fix that duplicates a block to avoid touching a shared path has
bought its result with structure. Check that the duplicate-block count
for the file you touched is no higher after your change than before it.
This is mechanical and cheap, and it is the one structural metric worth
gating in a small repository. Justify it locally rather than from the
published magnitudes (EV-0179).

## Evidence boundary

EV-0177 is self-reported motivation with recall bias, and it says
nothing about whether the refactorings improved anything. EV-0180 is a
tool, not a study. EV-0182 supplies the framing that any behaviour you
want preserved has to be defended by an automated test rather than by
convention, and it comes from a very large monorepo with a build system
that can run affected tests cheaply, so the principle transfers and the
machinery does not. That text carries a no-derivatives licence, so
nothing here reproduces it.

## Worked rulings

- **PatterTech EOS coding pack (2026-08, argued)**: B binding as
  requirement B2. Argued from EV-0180 for the mechanism and EV-0177 for
  the trigger.
- **Webhook receiver with no tests (2026-08, argued)**: B, then the new
  failing test, then the fix, in three commits. See
  `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`.
- **Bulk dependency bumps (2026-08, inherited)**: the existing suite is
  the pin, and the fixed validate loop from EV-0008 is the whole
  procedure.
