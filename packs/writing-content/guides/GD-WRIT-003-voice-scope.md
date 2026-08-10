---
summary: Which voice applies to this text, and who is allowed to overrule it?
kind: guide
authority: default
basis: decision
evidence_grade: asserted
scope: estate
sources: [EV-0435, EV-0440, EV-0447, EV-0448]
review: 2028-09
type: guide
tags: [voice, brand, content]
---

# GD-WRIT-003: Which voice applies to this text?

## The question

Version one of this estate ran one voice law over everything: the
repository, venture documentation, product copy and brand. That was a
category error. A rule written to stop a shared brain drifting is not a
product style guide, and it is certainly not a brand. ADR-0002
re-scoped it into three. This guide decides which of the three a given
piece of text sits under, and what happens when they disagree.

## It depends on

- **Which repository the file lives in.** That single fact settles most
  cases.
- **Who the reader is.** An agent, a developer, a customer, a market.
- **Whether the reader must act correctly**, which pulls towards
  literal language whatever the brand says.
- **Whether the venture has adopted a brand voice at all.** Most have
  not, and no brand voice binds anyone until it is adopted explicitly.

## Options

### A. EOS-internal law, authority binding
Every file in this repository. Plain, spoken, British spelling, no
em-dashes, no exclamation marks, no AI cliches, no two-fragment
antithesis. Basis: decision, ADR-0002. Buys one recognisable register
across a corpus that agents read constantly, and a mechanical check
that catches the commonest tells. Costs nothing outside this repository,
because it applies nowhere else. Scope: eos-internal.

### B. Venture documentation default, authority default
Documentation and product prose inside a venture repo. Plain-language
defaults apply: front-load the answer, lead with the verb, one
instruction per step, the reader's own words
(EV-0435, EV-0447). A venture departs
by recording a reason. Buys a sane starting point that no venture has
to argue for. Costs an argument the day a venture wants a different
register, which is the correct place for that argument. Scope: venture.

### C. Brand voice, authority preference
How a venture sounds to its market. Voice is fixed and describes who
the product is; tone varies with the reader's emotional state
(EV-0448). Capped at preference by
`kernel/METADATA_SPEC.md`, and it activates only by explicit adoption.
Buys a product that sounds like itself. Costs nothing enforceable, on
purpose: a brand voice must never be able to block an engineer's merge.
Scope: brand:`<name>`.

### D. Literal-instruction register, cutting across all three
Not a fourth scope but an override that applies inside any of them. In
instructions, errors and anything the reader must act on correctly:
literal language, simple tense and voice, one instruction per step, no
idiom and no metaphor (EV-0440). Contractions stay
allowed. Buys the reader who is under pressure, unfamiliar with
English, or using cognitive-accessibility support. Costs a brand its
best lines in exactly the places it most wants them.

## Decision rule

The file's repository picks A or B. If the text is a venture's
market-facing copy and the venture has adopted a brand voice, C applies
on top of B. If the reader must act correctly on this specific string,
D overrides the register of whichever scope applies, and the scope keeps
its other rules.

Where scopes conflict: the narrower scope wins on tone, the wider scope
wins on structure. A brand may choose its own register. A brand may not
choose to concatenate a sentence, skip a plural category, or write an
error that does not say what a good answer looks like.

## Default

B for a venture repo with no adopted brand, A here, D wherever the
reader has to get something right. No venture inherits a PatterTech
brand voice by default, and no house preference is ever presented to a
venture as a requirement.

## Worked rulings

- **This repository (2026-08, inherited)**: A, from the voice law in
  `CLAUDE.md` and its byte-identical twin, enforced mechanically by
  check E004. The em-dash prohibition disagrees directly with the
  Microsoft guide (EV-0447), and that is fine: A is a
  house ruling and does not claim to be right in general.
- **Venture documentation (2026-08, argued)**: B. A venture may use
  em-dashes, and the EOS voice law has no authority over it. The
  version one behaviour of applying A to venture prose is the failure
  this guide exists to end.
- **PatterTech house voice (2026-08, re-argued)**: C, and it does not
  exist. The earlier ruling put it in the pattertech-house pack. That
  pack is built, it covers the house visual language, and its own
  non-goals say it is not a copy guide, so it never held a brand voice
  and does not hold one now. Scope C is therefore defined here and
  filled nowhere. A venture that wants a brand voice writes one and
  adopts it by name, and nothing is missing from a venture that has
  not.
