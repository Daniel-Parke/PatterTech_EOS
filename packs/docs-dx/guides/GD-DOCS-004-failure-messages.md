---
summary: What a user-visible failure owes its reader, and how much structure to spend on it
type: guide
tags: [content, voice, delivery]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0175, EV-0327, EV-0328]
review: on-change-of:rustc-diagnostic-style-guide
---

# GD-DOCS-004: What does a failure message owe its reader?

## The question

Something goes wrong and the software has to say so. The fork is how
much structure to spend on the message, given that this is the piece of
documentation with the highest read rate in the system and nobody has
to be persuaded to open it.

## It depends on

- Who reads it: a person at a terminal, a person in an interface, or a
  program parsing it?
- Can anything act on a suggested fix automatically?
- Do stable identifiers for failures exist, or would minting them be a
  new project?
- Can the caller do anything differently depending on which failure it
  was?

## Options

### A. One line, prose

A sentence saying what went wrong. Buys: nothing to build. Costs: the
reader gets no offending input, no alternative and no way to tell one
failure from another.

### B. Primary message, offending input, detail on request

One general message, the specific span or value that caused it, and
long-form explanation behind an explicit request rather than inline
(EV-0328). Buys: the terminal stays readable while the detail is still
available. Costs: two surfaces to write instead of one.

### C. B plus a stable code and a confidence-tiered suggestion

Every failure carries a stable identifier, and any suggested fix
declares whether it is safe to apply automatically, contains
placeholders, might be wrong, or is unstated (EV-0328). Buys: a
downstream tool, including an agent, can decide whether to apply the
fix without reading the prose. Costs: an identifier registry that has
to be maintained, and the tiers are decoration where nothing can apply
a fix.

### D. Structured payload alongside the human text

The failure is emitted as data with a named type, plus a rendered human
string. Buys: a program never parses prose, and the set of failures a
caller can tell apart becomes an explicit part of the interface
(EV-0175). Costs: the failure set becomes a versioned contract, which
is the point and also the cost.

## Decision rule

- Any user-visible failure at all: **B** is the floor. Name the
  condition, show or name the offending input, point at the accepted
  alternative.
- A fixer exists, human or machine, that could apply the suggestion:
  **C**.
- A program or an agent is a first-class caller: **D**, and declare the
  failure set in the interface documentation rather than leaving it to
  be inferred (EV-0175).
- **A** is never sufficient where `emits_user_visible_failure` is true.

## Default

B, with the wording conventions below. Move to C when something can act
on the suggestion, and to D when a program is a caller.

## Wording conventions worth copying

From a compiler that has argued these for years (EV-0328): lower case,
no trailing full stop, plain words in preference to jargon, identifiers
in backticks, and a specific description of what is wrong rather than a
verdict like "illegal". The most transferable idea is not the wording.
It is that a suggestion carries a declared confidence, so the reader
does not have to guess how much to trust it.

Applied to a rejected input, the floor looks like this: say the value
was not recognised, quote it, and name what would have been accepted.
A reader who mistyped a flag can then fix it without opening the
documentation at all, which is the cheapest documentation there is.

## Evidence boundary

The strongest claim here is that reading difficulty predicts
time-to-fix, and it comes from an eye-tracking experiment with 56
undergraduate and graduate participants fixing planted Java defects in
Eclipse in 2017 (EV-0327). Scope it to that population: students, one
language, one IDE, planted defects, no model in the loop. The direction
transfers and the 13 to 25 per cent reading-time figure is not a
target. EV-0328 is a maintainer guide, not a study, and it presumes a
compiler with an error-code registry and a span model. An application
without stable failure identifiers cannot mint error codes cheaply, and
should take the wording and the confidence tier rather than the
registry.

## Worked rulings

- **PatterTech EOS docs-dx pack (2026-08, argued)**: B as the floor, C
  where a fixer exists, D where an agent is a caller. Argued from
  EV-0327 for why it matters and EV-0328 for what to write. B5 carries
  it as a default since the ADR-0008 audit, because a poor message is
  rewritten in one commit.
- **PatterTech EOS itself (2026-08, inherited)**: the checker emits a
  code, a path and a message for every finding, which is B with an
  identifier. Inherited from the checker's finding format.
