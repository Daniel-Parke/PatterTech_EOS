---
summary: What licence a repository carries outbound, and which promise that makes to the people downstream
type: guide
tags: [security, product]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [FRAG-LEGAL-LICENSING-01, FRAG-LEGAL-LICENSING-03, FRAG-LEGAL-LICENSING-04, FRAG-LEGAL-LICENSING-07, FRAG-LEGAL-LICENSING-12]
review: on-change-of:https://blueoakcouncil.org/list
review_by: 2028-03
---

# GD-LEGAL-003: What licence does this repository carry outbound?

## The question

A repository is about to be published, or is already public with no
licence file. The fork is which promise we make to the people
downstream, because that promise is what constrains every later choice,
including which dependencies we may take.

## It depends on

- Do we want the code used inside proprietary products?
- Do we care whether improvements come back?
- Is there patent exposure worth an explicit grant?
- Will we ever want to relicense, and who would have to agree?
- Is this a library other code links, or an application people run?

## Options

### A. Permissive, notice only

Use, modify and redistribute with attribution and nothing else. Buys:
the widest adoption, no compatibility argument ever, and the cheapest
promise to keep. Costs: someone can take it proprietary, and nothing
comes back. Within this family the drafting quality varies enough to be
worth checking, since a licence can satisfy the openness criteria and
still be rated poorly for drafting (FRAG-LEGAL-LICENSING-07).

### B. Permissive with an explicit patent grant

The same freedoms plus a stated patent position and a notice file
discipline. Buys: clarity where patents plausibly exist, which is why
the ratings put explicit patent handling at the top
(FRAG-LEGAL-LICENSING-07). Costs: more conditions to discharge, and its
patent terms are incompatible with an older reciprocal licence, which
constrains who can combine our code with what
(FRAG-LEGAL-LICENSING-04).

### C. Reciprocal

Derived works carry the same terms. Buys: improvements return, and the
code cannot be absorbed into a closed product. Costs: reciprocal
licences are mutually incompatible unless one carries an explicit
provision (FRAG-LEGAL-LICENSING-04), so we narrow who can use us. It is
also a promise about combination that our own dependency policy then
has to keep.

### D. Source-available or no licence

Published and readable with rights withheld. Buys: visibility without
giving anything away. Costs: a licence that limits the field of use is
not open source under the ten criteria however reasonable the limit
sounds (FRAG-LEGAL-LICENSING-03), so say so plainly rather than
implying otherwise. Publishing with no licence at all is the worst
version of this: it means exclusive copyright, the fork button grants
nothing, and honest users have to ask (FRAG-LEGAL-LICENSING-12).

## Decision rule

- A library or tool meant to be adopted, no patent exposure: A.
- Anything where a patent claim is plausible, or where a corporate user
  will ask about patents: B.
- The code is the product and absorption into a closed competitor is
  the risk: C, and accept the narrower combination surface.
- Rights genuinely withheld: D, stated as proprietary or
  source-available, never described as open source.
- Never publish with no licence file. B1 in
  `packs/legal-licensing/PACK.md` binds this.

Whichever is chosen, record it as an identifier from the list rather
than as prose, so a machine can read it (FRAG-LEGAL-LICENSING-01).

## Default

A, with the drafting rating used only as a tiebreak between otherwise
equal candidates. The reasoning is that the outbound licence is a
promise, and the cheapest promise to keep is the one with the fewest
conditions.

## Evidence boundary

Three separate axes get collapsed here constantly and they are not one
axis. Whether a licence restricts the wrong things is the openness
question (FRAG-LEGAL-LICENSING-03). Whether it is well drafted is a
different question answered by a panel of lawyers exercising judgement
(FRAG-LEGAL-LICENSING-07). Whether it fits our promise is ours alone.
The identifier registry deliberately records openness and free-software
status as two independent columns rather than merging them into one
verdict, and it will happily name a licence that is neither open nor
safe to depend on (FRAG-LEGAL-LICENSING-01). No source read ranks
outbound licences by outcome, and none of this is legal advice.

## Worked rulings

- **PatterTech EOS legal-licensing pack (2026-08, argued)**: A as the
  default, B where patents are plausible. Argued from the promise
  framing rather than from adoption statistics, because no adoption
  measurement was read at this cutoff.
- **PatterTech EOS itself (2026-08, inherited)**: private repository,
  no outbound licence yet. The moment it is published, B1 applies and
  this guide runs for real.
