---
id: WG-LEGAL-003
summary: What licence a repository carries outbound, and which promise that makes to the people downstream
kind: wargame
type: wargame
tags: [eos, product, security, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-LEGAL-001]
applies_when: [publishes_code]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0337, EV-0339, EV-0340, EV-0343, EV-0348]
review: on-change-of:https://blueoakcouncil.org/list
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-LEGAL-003: What licence does this repository carry outbound?

## Decision question and stakes

A repository is about to be published, or is already public with no
licence file. The fork is which promise we make to the people
downstream, because that promise is what constrains every later choice,
including which dependencies we may take.

## Doctrines or coverage gap under pressure

- `DOC-LEGAL-001` (default): Every repository declares its own licence.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Do we want the code used inside proprietary products?
- Do we care whether improvements come back?
- Is there patent exposure worth an explicit grant?
- Will we ever want to relicense, and who would have to agree?
- Is this a library other code links, or an application people run?

Applicability is `publishes_code`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Permissive, notice only

Use, modify and redistribute with attribution and nothing else. Buys:
the widest adoption, no compatibility argument ever, and the cheapest
promise to keep. Costs: someone can take it proprietary, and nothing
comes back. Within this family the drafting quality varies enough to be
worth checking, since a licence can satisfy the openness criteria and
still be rated poorly for drafting (EV-0343).

### B. Permissive with an explicit patent grant

The same freedoms plus a stated patent position and a notice file
discipline. Buys: clarity where patents plausibly exist, which is why
the ratings put explicit patent handling at the top
(EV-0343). Costs: more conditions to discharge, and its
patent terms are incompatible with an older reciprocal licence, which
constrains who can combine our code with what
(EV-0340).

### C. Reciprocal

Derived works carry the same terms. Buys: improvements return, and the
code cannot be absorbed into a closed product. Costs: reciprocal
licences are mutually incompatible unless one carries an explicit
provision (EV-0340), so we narrow who can use us. It is
also a promise about combination that our own dependency policy then
has to keep.

### D. Source-available or no licence

Published and readable with rights withheld. Buys: visibility without
giving anything away. Costs: a licence that limits the field of use is
not open source under the ten criteria however reasonable the limit
sounds (EV-0339), so say so plainly rather than
implying otherwise. Publishing with no licence at all is the worst
version of this: it means exclusive copyright, the fork button grants
nothing, and honest users have to ask (EV-0348).

## Failure premises

### Premortem for A. Permissive, notice only

Assume `A. Permissive, notice only` was selected and the outcome failed. Test this option's stated failure mechanism first: someone can take it proprietary, and nothing comes back. Within this family the drafting quality varies enough to be worth checking, since a licence can satisfy the openness criteria and still be rated poorly for drafting (EV-0343).

### Premortem for B. Permissive with an explicit patent grant

Assume `B. Permissive with an explicit patent grant` was selected and the outcome failed. Test this option's stated failure mechanism first: more conditions to discharge, and its patent terms are incompatible with an older reciprocal licence, which constrains who can combine our code with what (EV-0340).

### Premortem for C. Reciprocal

Assume `C. Reciprocal` was selected and the outcome failed. Test this option's stated failure mechanism first: reciprocal licences are mutually incompatible unless one carries an explicit provision (EV-0340), so we narrow who can use us. It is also a promise about combination that our own dependency policy then has to keep.

### Premortem for D. Source-available or no licence

Assume `D. Source-available or no licence` was selected and the outcome failed. Test this option's stated failure mechanism first: a licence that limits the field of use is not open source under the ten criteria however reasonable the limit sounds (EV-0339), so say so plainly rather than implying otherwise. Publishing with no licence at all is the worst version of this: it means exclusive copyright, the fork button grants nothing, and honest users have to ask (EV-0348).

## Decision rule

- A library or tool meant to be adopted, no patent exposure: A.
- Anything where a patent claim is plausible, or where a corporate user
  will ask about patents: B.
- The code is the product and absorption into a closed competitor is
  the risk: C, and accept the narrower combination surface.
- Rights genuinely withheld: D, stated as proprietary or
  source-available, never described as open source.
- Never publish with no licence file. B1 in
  `packs/legal-licensing/PACK.md` is that default, and departing from
  it means publishing something nobody may lawfully use.

Whichever is chosen, record it as an identifier from the list rather
than as prose, so a machine can read it (EV-0337).

## Safe default

A, with the drafting rating used only as a tiebreak between otherwise
equal candidates. The reasoning is that the outbound licence is a
promise, and the cheapest promise to keep is the one with the fewest
conditions.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Do we want the code used inside proprietary products?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, with the drafting rating used only as a tiebreak between otherwise equal candidates. The reasoning is that the outbound licence is a promise, and the cheapest promise to keep is the one with the fewest conditions.

**Exit condition:** Stop or roll back the selected branch when someone can take it proprietary, and nothing comes back. Within this family the drafting quality varies enough to be worth checking, since a licence can satisfy the openness criteria and still be rated poorly for drafting (EV-0343), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Do we want the code used inside proprietary products?

## Counter-evidence and transfer limits

### Evidence boundary

Three separate axes get collapsed here constantly and they are not one
axis. Whether a licence restricts the wrong things is the openness
question (EV-0339). Whether it is well drafted is a
different question answered by a panel of lawyers exercising judgement
(EV-0343). Whether it fits our promise is ours alone.
The identifier registry deliberately records openness and free-software
status as two independent columns rather than merging them into one
verdict, and it will happily name a licence that is neither open nor
safe to depend on (EV-0337). No source read ranks
outbound licences by outcome, and none of this is legal advice.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
