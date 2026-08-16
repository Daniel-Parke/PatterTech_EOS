---
id: WG-MKTG-001
summary: Which growth philosophy does this venture run?
kind: wargame
type: wargame
tags: [brand, content, eos, product, seo, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-MKTG-004, DOC-MKTG-013]
applies_when: [publishes_public_content]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0055, EV-0095, EV-0353, EV-0356, EV-0359, EV-0360, EV-0361, EV-0365, EV-0366, EV-0368, EV-0369]
review: on-change-of:Reforge-and-IPA-primary-text-access
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-MKTG-001: Which growth philosophy does this venture run?

## Decision question and stakes

Four traditions claim to explain how a business grows, and they pull
budget in different directions. Picking by habit means inheriting
whichever one the last plan was written in. PACK.md D1 requires the
choice to be named and recorded before spend; this Wargame is where the
choice is argued.

## Doctrines or coverage gap under pressure

- `DOC-MKTG-004` (default): One named growth philosophy per venture, recorded before spend.
- `DOC-MKTG-013` (default): Reach to category non-buyers is the opening bet for a small brand.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether the buyer already searches.** A category with no reading
  habit gives an organic asset nothing to compound on.
- **Whether the product itself produces the next user.** Loops need a
  real mechanism, not an arrow on a diagram.
- **Purchase frequency.** Repeat-purchase categories behave differently
  from one-off high-consideration ones.
- **Money and patience.** Reach costs both, and shows nothing in a
  weekly dashboard.
- **The gap between interest and readiness.** A long gap is what an
  owned channel is for.
- **Platform risk.** A business that dies when one account is closed has
  already made a decision it has not written down.

Applicability is `publishes_public_content`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Compounding organic asset
Publish in the open and let the archive do the acquiring: content, docs
and search discovery as one artefact, edited on encounter (EV-0095).
Buys an asset that keeps working after the spend stops, and cheap
credibility in a technical category. Costs a payback measured in a year
or more, and it produces nothing at all where buyers do not read
(EV-0353, EV-0356, EV-0366).

### B. Reach-led brand building
Buy penetration among people who have never bought, budget by time
horizon rather than blended return, and treat loyalty as a consequence
of size rather than a lever (EV-0368, EV-0369). Buys growth
in the only place the repeat-purchase panels say it comes from. Costs
money, patience, and visibility in short-term reporting. The evidence is
directional: both records were read at second hand, and one rests on
self-selected award entries.

### C. Growth loops
Name the step where output re-enters as input, through content,
invitation or a public artefact, and put the engine inside product usage
(EV-0365). Buys compounding without proportional spend, and a
single owner for a mechanism a funnel would split across teams. Costs
credibility: the source is a practitioner essay with no data, published
by a consultancy positioning its own curriculum.

### D. Lifecycle and owned channel
Capture consent with provenance, run sequences against the gap between
interest and readiness, and treat sending reputation as a production
service level (EV-0359, EV-0360, EV-0361). Buys a channel
nobody can take away and a compliance surface that is auditable. Costs a
real and jurisdictional compliance burden, and it needs an audience that
already exists.

## Failure premises

### Premortem for A. Compounding organic asset

Assume `A. Compounding organic asset` was selected and the outcome failed. Test this option's stated failure mechanism first: a payback measured in a year or more, and it produces nothing at all where buyers do not read (EV-0353, EV-0356, EV-0366).

### Premortem for B. Reach-led brand building

Assume `B. Reach-led brand building` was selected and the outcome failed. Test this option's stated failure mechanism first: money, patience, and visibility in short-term reporting. The evidence is directional: both records were read at second hand, and one rests on self-selected award entries.

### Premortem for C. Growth loops

Assume `C. Growth loops` was selected and the outcome failed. Test this option's stated failure mechanism first: credibility: the source is a practitioner essay with no data, published by a consultancy positioning its own curriculum.

### Premortem for D. Lifecycle and owned channel

Assume `D. Lifecycle and owned channel` was selected and the outcome failed. Test this option's stated failure mechanism first: a real and jurisdictional compliance burden, and it needs an audience that already exists.

## Decision rule

If the buyer already searches for the problem and the category has a
reading habit, choose A. If the category is repeat-purchase or
mass-market and most buyers are light buyers who are not in market
today, choose B. If usage genuinely produces the next user and you can
name the reinvestment step without drawing it, choose C. If the purchase
is considered with a real gap between interest and readiness, or losing
a platform account would end the business, choose D. Combining two is
allowed; running all four with one person is not a strategy, it is a
list.

## Safe default

A for a technical venture with a reading audience, D alongside it as
soon as anyone gives you an address. B is the default for a small brand
in a repeat-purchase category, which is where PACK.md D10 points. C is
never a default: it is earned by naming the mechanism.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the buyer already searches.** A category with no reading habit gives an organic asset nothing to compound on.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A for a technical venture with a reading audience, D alongside it as soon as anyone gives you an address. B is the default for a small brand in a repeat-purchase category, which is where PACK.md D10 points. C is never a default: it is earned by naming the mechanism.

**Exit condition:** Stop or roll back the selected branch when a payback measured in a year or more, and it produces nothing at all where buyers do not read (EV-0353, EV-0356, EV-0366), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the buyer already searches.** A category with no reading habit gives an organic asset nothing to compound on.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Whether the buyer already searches.** A category with no reading habit gives an organic asset nothing to compound on.** and ****Whether the product itself produces the next user.** Loops need a real mechanism, not an arrow on a diagram.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
