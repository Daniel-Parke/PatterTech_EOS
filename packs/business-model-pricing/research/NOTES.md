---
summary: What the evidence supports for business model and pricing, three contrasting philosophies with fit conditions, the disagreements, and the binding versus default versus preference split
type: example
tags: [eos, testing]
---

# Business model and pricing research notes

Cutoff 2026-08-03. Eighteen new sources in `sources.fragment.json`.
From the existing ledger this pack leans on FinOps (EV-0197) for unit
cost allocation, GrowthBook's experiment decision framework (EV-0059)
for how a pricing test is called, the GitLab and PostHog handbooks
(EV-0055, EV-0095) as public exemplars of writing pricing and
commercial policy down, DORA's five key metrics (EV-0199) and SPACE
(EV-0210) for metric hygiene, and the SRE error budget policy
(EV-0096) as the shape of a pre-agreed trigger.

## The three philosophies, and when each fits

### 1. Cost-plus and competitor-anchored pricing

Set the price from what it costs to serve plus a margin, or from what
the nearest comparable product charges. Still the majority practice
(FRAG-01). It is cheap, it is defensible to a customer, and under
FRAG-06 it is the framing that buyers accept when the price rises,
because a cost-justified increase reads as fair and a demand-driven
one reads as exploitation.

Fits when the buyer can compare like for like, when the product is
undifferentiated, when the seller has no way to assess value yet, and
in the first months of a venture where there is no willingness-to-pay
evidence at all. FRAG-02 is the honest correction to the usual
sneering: competition-informed and cost-informed pricing are not
uniformly worse, their payoff depends on conditions.

Anti-patterns: pricing off a competitor whose cost base and funding
you do not share; a margin percentage carried over from a different
business; treating cost-plus as permanent rather than as the opening
position while value evidence is gathered.

### 2. Value-based pricing

Price from the buyer's perceived benefit, segment by segment. The
evidence says this is what works and also that most firms cannot do
it (FRAG-01): the blockers are value assessment, value communication,
segmentation, sales incentives and sponsorship, all capability
problems rather than belief problems.

Fits when the product changes a measurable number in the buyer's
world, when segments differ enough to price differently, and when
someone owns the value case. For a small venture the practical form
is narrow: one segment, one quantified before-and-after, one price.

Anti-patterns: declaring value-based pricing without building the
value assessment, which produces a higher number with no argument
behind it; surveying willingness to pay and treating the answer as
fact (FRAG-03 shows hypothetical elicitation overstates it and only
incentive-compatible methods survived a real-purchase test); running
a Van Westendorp meter and calling the crossing point the price, when
the vendor selling the method lists its own limits, including no
competitive context and no volume prediction (FRAG-04).

### 3. Metered and usage-based models

Price the unit of consumption rather than the seat or the licence.
This is where the pack's evidence is thinnest and the marketing
loudest. Widely repeated benchmark claims (usage-based firms showing
higher net revenue retention, adoption rising year on year) trace
back to vendor surveys and blog aggregations, not to controlled work,
and they are exposed to survivorship and self-selection: firms whose
customers grow adopt usage pricing and also retain better. No source
worth recording was found at this cutoff that isolates the causal
effect. That is an open question, recorded as one, and no benchmark
number from that literature is carried into the pack.

What can be said from primary sources is structural. IFRS 15
(FRAG-11) requires that every bundle decompose into distinct
performance obligations with defensible stand-alone selling prices,
so a metered add-on invented for the pricing page becomes a revenue
recognition problem later. Fader and Hardie (FRAG-10) show that
cohort retention rises over time purely because high-churn customers
leave first, so a lifetime value computed from a blended churn rate
is wrong in a knowable direction, and usage-based revenue makes that
worse because expansion and contraction move within a live account.

Fits when consumption tracks value closely and the buyer can predict
their bill. Anti-pattern: metering something the buyer cannot forecast
or control, which converts a pricing model into a support queue.

## Where the sources disagree

- **Value-based pricing as capability failure versus conditional
  choice.** FRAG-01 treats cost and competitor pricing as resistance
  to be overcome; FRAG-02 treats them as rational under some
  conditions. The reconciliation the pack should carry: name the
  practice and the condition, and set a date to revisit, rather than
  pledging allegiance to one practice.
- **Trial length.** FRAG-08 (Management Science, one SaaS firm, 7 vs
  14 vs 30 days) finds 7 days best, with consumer learning as the
  mechanism. FRAG-09 (Frontiers, 680,588 users, 3 vs 7 days) finds
  the longer trial better, lifting adoption and delayed conversion
  while immediate conversion did not move. Taken together these are
  not a contradiction but an interior optimum near a week, and a
  warning: FRAG-09's immediate-conversion null would have killed the
  change if the test had been judged on that stage alone. This is the
  load-bearing contradiction for the pack, because it kills any
  guide sentence of the form "use an N day trial" and replaces it
  with a measurement rule.
- **Hypothetical willingness-to-pay methods.** FRAG-03 says only
  incentive-compatible elicitation passed against real purchases;
  evaluations of the price sensitivity meter report it is biased and
  yet reaches predictive quality comparable to the incentive-aligned
  mechanism (FRAG-04 counter-evidence). Unsettled. Treat survey
  prices as an upper bound and a bracket, never as the decision.
- **Decoy tiers.** The regulator lists decoys among practices the
  literature finds almost always harmful (FRAG-14), while the
  replication evidence says the effect mostly fails to appear with
  realistic stimuli (FRAG-07), and defenders say it holds when
  choices carry economic consequences. Harm and efficacy are separate
  questions and the pack should not rely on either.

## Binding, default, preference

**Binding.** These are law or accounting at the access date, and a
venture does not get to prefer otherwise.

- Unavoidable mandatory charges appear in the headline price; drip
  pricing is banned and the CMA enforces directly (FRAG-13).
- Consumer subscriptions must meet the DMCC duties once commenced:
  separate key pre-contract information, express acknowledgement of
  the payment obligation, renewal reminders, an online exit route,
  cooling-off (FRAG-12). Commercial commentary at the cutoff put
  commencement at spring 2027 after repeated delays, so build to the
  principles and do not hard-code section detail.
- Revenue is recognised under the five-step model, not on cash
  receipt; bundles need stand-alone selling prices (FRAG-11).
- Payment terms exist whether or not they are written: 30 days by
  default in commercial supply, 60 by agreement between businesses,
  30 for public authorities (FRAG-15), and an unoverridable 30 days
  implied into every public contract (FRAG-16).
- VAT registration at 90,000 pounds rolling turnover (FRAG-17) and
  Making Tax Digital for Income Tax from 6 April 2026 above 50,000
  pounds qualifying income (FRAG-18) are dated obligations with
  refresh triggers, not permanent facts.

**Default.** Overridable with a recorded reason.

- Open cost-plus or competitor-anchored, with a dated review to move
  to value evidence (FRAG-01, FRAG-02).
- A price change is announced with its cause, and the cause is a cost
  or delivered-value change (FRAG-06).
- Trial length starts near a week and is tested (FRAG-08, FRAG-09).
- Retention is reported as a cohort curve; lifetime value is never
  computed as revenue over blended churn (FRAG-10).
- Every metric in a commercial report carries its definition and
  calculation next to the number, and a definition change is stated
  when it happens. This mirrors DORA and SPACE discipline (EV-0199,
  EV-0210); an attempt to anchor it in SEC Release 33-10751 on key
  performance indicators failed at this cutoff because sec.gov and
  the Federal Register mirror both refused the fetch, so the rule is
  carried on internal reasoning and is weaker than it should be.

**Preference.** Style, argue it if you like.

- Price endings and rounding. FRAG-05 is real evidence for nine
  endings, strongest for items new to the buyer and weaker with sale
  cues, from US catalogue retail in the 1990s. Not transplantable to
  a B2B list price as a rule.
- Tier names, the number of tiers, whether a public price exists.

## Open questions to hand to the author

1. No causal evidence was found for usage-based versus seat-based
   pricing on retention. Either find it or the pack states the
   structural argument only.
2. No primary source found at this cutoff that fixes the definitions
   of ARR, net revenue retention or churn. Public filings say openly
   that ARR has no standardised meaning, which is itself the finding,
   but the pack needs its own written definitions rather than a
   citation.
3. Nothing found on financial controls proportionate to a one-person
   venture (segregation of duties is not available with one person).
   Likely needs a first-principles guide, marked as such.
