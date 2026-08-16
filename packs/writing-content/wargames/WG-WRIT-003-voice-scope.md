---
id: WG-WRIT-003
summary: Which voice applies to this text, and who is allowed to overrule it?
kind: wargame
type: wargame
tags: [brand, content, eos, voice, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-WRIT-009]
applies_when: [writes_eos_internal_prose]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: asserted
sources: [EV-0435, EV-0440, EV-0447, EV-0448]
review: 2028-09
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-WRIT-003: Which voice applies to this text?

## Decision question and stakes

Version one of this estate ran one voice law over everything: the
repository, venture documentation, product copy and brand. That was a
category error. A rule written to stop a shared brain drifting is not a
product style guide, and it is certainly not a brand. ADR-0002
re-scoped it into three. This Wargame decides which of the three a given
piece of text sits under, and what happens when they disagree.

## Doctrines or coverage gap under pressure

- `DOC-WRIT-009` (default): Prose in this repository follows the voice law.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Which repository the file lives in.** That single fact settles most
  cases.
- **Who the reader is.** An agent, a developer, a customer, a market.
- **Whether the reader must act correctly**, which pulls towards
  literal language whatever the brand says.
- **Whether the venture has adopted a brand voice at all.** Most have
  not, and no brand voice binds anyone until it is adopted explicitly.

Applicability is `writes_eos_internal_prose`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. EOS-internal house rule, authority default
Every file in this repository. Plain, spoken, British spelling, no
em-dashes, no exclamation marks, no AI cliches, no two-fragment
antithesis. Basis: decision, ADR-0002. PACK.md B8 carried this as
binding until the 2026-08 audit and carries it as a default now, on the
basis leg: a house ruling is not law, a standard or a measured effect.
Check E004 fails the build either way, which is what actually holds
the register. Buys one recognisable voice across a corpus that agents
read constantly. Costs nothing outside this repository, because it
applies nowhere else. Scope: eos-internal.

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

## Failure premises

### Premortem for A. EOS-internal house rule, authority default

Assume `A. EOS-internal house rule, authority default` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing outside this repository, because it applies nowhere else. Scope: eos-internal.

### Premortem for B. Venture documentation default, authority default

Assume `B. Venture documentation default, authority default` was selected and the outcome failed. Test this option's stated failure mechanism first: an argument the day a venture wants a different register, which is the correct place for that argument. Scope: venture.

### Premortem for C. Brand voice, authority preference

Assume `C. Brand voice, authority preference` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing enforceable, on purpose: a brand voice must never be able to block an engineer's merge. Scope: brand:`<name>`.

### Premortem for D. Literal-instruction register, cutting across all three

Assume `D. Literal-instruction register, cutting across all three` was selected and the outcome failed. Test this option's stated failure mechanism first: a brand its best lines in exactly the places it most wants them.

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

## Safe default

B for a venture repo with no adopted brand, A here, D wherever the
reader has to get something right. No venture inherits a PatterTech
brand voice by default, and no house preference is ever presented to a
venture as a requirement.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Which repository the file lives in.** That single fact settles most cases.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B for a venture repo with no adopted brand, A here, D wherever the reader has to get something right. No venture inherits a PatterTech brand voice by default, and no house preference is ever presented to a venture as a requirement.

**Exit condition:** Stop or roll back the selected branch when nothing outside this repository, because it applies nowhere else. Scope: eos-internal, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Which repository the file lives in.** That single fact settles most cases.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Which repository the file lives in.** That single fact settles most cases.** and ****Who the reader is.** An agent, a developer, a customer, a market.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
