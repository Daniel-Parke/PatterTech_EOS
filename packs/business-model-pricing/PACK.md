---
summary: How a venture chooses what it sells and what it charges, three pricing practices under one legal and accounting floor
type: playbook
tags: [money, product, eos]
kind: rule
authority: binding
lifecycle: active
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price, publishes_a_price, sells_to_consumers, sells_by_subscription, sells_to_public_sector, bundles_or_discounts, reports_commercial_metrics]
activation_paths: [**/pricing/**, **/*pricing*.md, **/plans/**, **/tiers/**, **/*subscription*, **/*checkout*, **/*invoice*]
volatility: event-driven
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
sources: [EV-0287, EV-0288, EV-0289, EV-0290, EV-0291, EV-0292, EV-0293, EV-0294, EV-0295, EV-0296, EV-0297, EV-0298, EV-0299, EV-0300, EV-0301, EV-0302, EV-0303, EV-0304, EV-0055, EV-0059, EV-0095, EV-0096, EV-0197, EV-0199, EV-0210]
---

# business-model-pricing

This pack covers what a venture sells, what it charges for it, and what
the price then obliges it to do. It activates on any task that sets or
changes a price, designs a tier, a trial or a bundle, writes a pricing
page, or reports a commercial number. UK consumer, payment and
accounting law binds. Which information the price is anchored to is a
conditional choice, and the pack makes you name the condition.

## Activation

**Paths.** Anything under a pricing, plans, billing, checkout,
subscribe, tariff, invoicing, finance or commercial directory. Price and
plan configuration in payment-provider code. A public pricing or terms
page. Cohort, revenue and retention reporting code.

**Task types.** Set an opening price. Change an existing price. Design
tiers, bundles, discounts or a trial. Build or change a checkout or a
renewal flow. Write invoicing or payment terms. Report revenue,
retention, churn or growth to anyone. Decide whether a charge is
optional.

**Keywords, fallback only.** Price, pricing, tier, packaging, bundle,
discount, trial, freemium, metered, seat, subscription, renewal, churn,
retention, ARR, MRR, LTV, margin, VAT, invoice, payment terms, refund,
cooling-off. Keywords never override the predicates.

**Applicability predicates.** Each requirement below names the predicate
that turns it on.

| Predicate | True when |
| --- | --- |
| sets_a_price | the task fixes or changes a number a buyer pays |
| publishes_a_price | a price is shown to anyone outside the venture |
| sells_to_consumers | the buyer is an individual acting outside a trade |
| sells_by_subscription | a charge recurs without a fresh purchase decision |
| sells_to_public_sector | the buyer is a UK contracting authority |
| bundles_or_discounts | one payment covers more than one distinct promise |
| reports_commercial_metrics | a revenue, retention or growth number leaves the venture |

A task that touches a pricing path but satisfies no predicate loads
nothing beyond the paragraph above. Internal cost modelling with no
customer-facing number is one such task.

## Outcomes and non-goals

**Outcomes.** A price that carries the practice it was set by and the
condition that justified that practice. A headline number a buyer can
rely on. A subscription a buyer can leave without asking permission. A
payment clock both sides can point at. Revenue recognised against what
was delivered rather than counted at the bank. Commercial numbers that
mean the same thing next quarter as they did this one.

**Non-goals.** Campaigns, channels and marketing consent sit in the
marketing-growth pack. What to build and for whom sits in
product-discovery. Contract drafting and licence choice sit in
legal-licensing. Infrastructure cost measurement sits in
devops-reliability via FinOps (EV-0197); this pack consumes that
allocation rather than producing it. Experiment plumbing sits in
data-analytics. This pack sets no number for any venture, and it is not
a substitute for an accountant.

## Binding requirements

Four requirements bind. Each is law or an accounting standard at the
access date, and a venture does not get to prefer otherwise. Everything
else in this pack is a default or a preference, which is the honest
position for a domain whose commercial evidence is mostly single-firm
field experiments and surveys.

The authority audit under ADR-0008 moved two of the original six to
defaults. Writing payment terms down is now D9, because the statute
supplies the term whether or not anyone writes it, so the rule's own
contribution is a record rather than a duty. The regulator's
almost-always-harmful list is now D10, because it is an evidence review
rather than a prohibition, and the unlawful part of it is already bound
by B1. The four that stayed keep their numbers, so the citations in the
refs, checks and exemplar still resolve, which is why the list below
runs B1, B2, B4, B5.

**B1. The headline price includes every unavoidable charge.**
Predicates: publishes_a_price, sells_to_consumers. Any charge the buyer
cannot avoid appears in the advertised number, not at the end of the
journey. Prevents drip pricing, which the CMA now enforces against
directly under the commenced consumer provisions of the DMCC Act, with
penalties reported up to ten per cent of global turnover (EV-0299). The
contested boundary is between unavoidable and genuinely optional; record
which side each charge sits and why. See
`packs/business-model-pricing/refs/UK_OBLIGATIONS.md`.

**B2. A consumer subscription can be entered knowingly and left
easily.** Predicates: sells_to_consumers, sells_by_subscription. Key
pre-contract information given separately, an express acknowledgement of
the payment obligation at the final step, reminder notices before
renewal payments, a straightforward online exit route, and cooling-off
on entry and on specified renewals (EV-0298). Prevents the renewal flow
that treats silence as consent, which is the pattern the statute was
written to stop. Scope note: the DMCC subscription chapter was enacted
in 2024 and was still awaiting commencement regulations at the cutoff,
with commercial commentary putting it near spring 2027. Build to the
principles; do not hard-code section detail into product copy.

**B4. Revenue is recognised, never counted at the bank.** Predicates:
bundles_or_discounts, reports_commercial_metrics. Follow the five-step
model, and decompose every bundle, discount and add-on into distinct
performance obligations with defensible stand-alone selling prices
(EV-0297). Prevents the tier invented for the pricing page that nobody
can allocate a transaction price to later. Scope note: IFRS 15 applies
where the entity reports under IFRS; a UK micro-entity may sit under FRS
102 or FRS 105 and a US filer under ASC 606. Name your framework in the
decision record.

**B5. Tax thresholds are watched as pricing events.** Predicates:
sets_a_price, reports_commercial_metrics. VAT registration is compulsory
once taxable turnover over any rolling twelve months exceeds ninety
thousand pounds, or is expected to within thirty days (EV-0303). Making
Tax Digital for Income Tax starts 6 April 2026 above fifty thousand
pounds of qualifying income, 2027 above thirty thousand and 2028 above
twenty thousand (EV-0304). Prevents crossing the VAT threshold and
discovering the effective consumer price has fallen by the VAT rate
overnight. Both are dated policy numbers with refresh triggers, held in
`packs/business-model-pricing/refs/UK_OBLIGATIONS.md`, never inlined
elsewhere.

Guarded actions stay outside this pack. Taking money, refunding money
and changing a live price are ruled by `kernel/GUARD_SPEC.md` and its
non-waivable floors. No pricing argument changes a guard verdict.

## Defaults

Each applies unless the venture's lock-book overrides it with a recorded
reason.

**D1. Open on a named practice with its condition and a revisit date.**
Say whether the price is value-informed, competition-informed or
cost-informed, and say what makes that the right anchor here. Reason:
more than four fifths of surveyed firms priced from cost or competitor
levels while agreeing value pricing works, and the blockers were all
capability rather than belief (EV-0287); later work finds the three
practices pay off under different conditions rather than ranking
(EV-0288). Scope note: both are self-reported surveys of mid-size and
large firms, pre-SaaS, with no causal identification. See
`packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md`.

**D2. A price change is announced with its cause, and the cause is cost
or delivered value.** Reason: buyers judge a rise that protects an
existing margin against a cost increase as fair, and a rise that
exploits a demand shift as unfair (EV-0292). Scope note: 1986
telephone-survey fairness judgements, not observed churn; the paper puts
no number on what a violation costs. Override where you can show the
retention consequence in your own cohorts. See
`packs/business-model-pricing/guides/GD-BMP-004-repricing-trigger.md`.

**D3. Trial length starts near a week and is tested across the whole
funnel.** Reason: one SaaS firm found seven days beat fourteen and
thirty (EV-0294) while another found seven beat three (EV-0295), which
together support an interior optimum rather than a direction. The second
study also moved delayed conversion and trial adoption while immediate
conversion stayed flat, so a test judged on the first stage alone reads
as a null and gets abandoned wrongly. A trial length that ships without
a test plan is a number the evidence does not support. See
`packs/business-model-pricing/guides/GD-BMP-003-try-before-paying.md`.

**D4. Retention is reported as a cohort curve, and lifetime value is
never revenue over blended churn.** Reason: the observed period-over-
period retention rate of a cohort rises with age purely because
high-churn customers leave first, so a single average churn projected
forward is wrong in a knowable direction (EV-0296). Scope note: the
model needs several periods of contractual cohort data, which a
first-year venture does not have; until then report the observed curve
and refuse the single number. See
`packs/business-model-pricing/refs/RETENTION_AND_LTV.md`.

**D5. Every commercial number travels with its definition.** The formula
sits next to the number, and a definition change is stated in the report
where it happens. Reason: this mirrors the metric hygiene the DORA and
SPACE work insists on (EV-0199, EV-0210), and no primary source was
found at the cutoff that fixes ARR, net revenue retention or churn.
Honest weakness: an attempt to anchor this in the SEC release on key
performance indicators failed because the source could not be fetched,
so D5 rests on internal reasoning and is weaker than it should be. See
`packs/business-model-pricing/refs/METRIC_DEFINITIONS.md`.

**D6. A survey-derived price is a bracket, never the decision.** Reason:
only incentive-compatible elicitation passed against real purchase
behaviour, and hypothetical answers overstate willingness to pay
(EV-0289); the vendor selling the price sensitivity meter lists its own
limits, including no competitive context and no volume prediction
(EV-0290). Treat the range as an upper bound until a real transaction
tests it.

**D7. Unit cost is allocated before a margin is claimed.** Every charged
unit carries an allocated cost to serve, using the FinOps allocation the
devops-reliability pack owns (EV-0197). Reason: a margin percentage
without an allocation is a guess wearing a decimal point.

**D8. The repricing trigger is written before it fires.** Agree in
advance what movement in cost or delivered value opens a price change,
and what the response is, in the shape of a pre-agreed error budget
policy (EV-0096). Reason: a trigger written after the pressure arrives
is negotiated under the pressure.

**D9. Payment terms are written down, because they exist either way.**
Predicates: sets_a_price, sells_to_public_sector. Where nothing is
agreed, a commercial payment is late thirty days after the later of
invoice receipt and delivery; terms may run to sixty days between
businesses where fair, and public authorities pay within thirty
(EV-0301). Every public contract carries an implied thirty-day term that
no clause can override, and a valid invoice needs the supplier name, a
description, the amount and a unique identifier (EV-0302). Those are the
law and they apply whatever this pack says. What is a default is writing
the term into the quote, and the reason is that a quote shipped with no
term invites the belief that nothing is therefore late. Departing means
recording that the statutory default is the term you are relying on.

**D10. No pattern from the regulator's almost-always-harmful list.**
Predicates: publishes_a_price, sells_to_consumers. Drip pricing, sludge,
dark nudges, decoys, choice overload, sensory manipulation and
information overload are classified by the CMA's own evidence review as
practices the literature finds almost always harmful (EV-0300). Reason:
building a conversion tactic from that list is an enforcement exposure.
This is a default rather than binding because EV-0300 is an evidence
review rather than a prohibition, and because its unlawful core, drip
pricing, is already bound by B1 on the statute. Departing means
recording the argument, and legal advice is the sensible shape for that
record. Note the separation: whether a pattern is harmful and whether it
works are different questions, and the decoy evidence answers the second
one badly (EV-0293).

## Preferences

Taste. Record them, do not gate on them, override them without asking.

- **Price endings.** Nine endings raised demand in three field
  experiments, most for items new to the buyer and least where sale cues
  were present (EV-0291). That was US catalogue retail of physical goods
  in the late 1990s, and it does not transplant to a subscription list
  price as a rule.
- **Tier count and tier names.** Nothing in the evidence sets a number.
- **Whether a public price exists at all**, and how currency and
  rounding are displayed.
- **Publishing the commercial policy in a public handbook**, as the
  GitLab and PostHog handbooks do (EV-0055, EV-0095). Useful discipline,
  not an obligation.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| What is this price anchored to? | `packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md` | Cost-informed or competition-informed opening, with a dated move to value evidence |
| What is the unit of charge? | `packs/business-model-pricing/guides/GD-BMP-002-charging-unit.md` | The simplest unit the buyer can forecast |
| How does someone try this before paying? | `packs/business-model-pricing/guides/GD-BMP-003-try-before-paying.md` | A time-boxed trial near a week, with a test plan |
| When and how does the price change? | `packs/business-model-pricing/guides/GD-BMP-004-repricing-trigger.md` | A written cost-or-value trigger, announced with its cause |

Level-three detail: the artefacts a decision has to emit are in
`packs/business-model-pricing/refs/DECISION_RECORD.md`, the dated duties
in `packs/business-model-pricing/refs/UK_OBLIGATIONS.md`, the cohort
method in `packs/business-model-pricing/refs/RETENTION_AND_LTV.md`, the
house metrics in
`packs/business-model-pricing/refs/METRIC_DEFINITIONS.md`, and a worked
run in
`packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md`.

## Failure modes and anti-patterns

- **Fees revealed at checkout and called transparency.** Drip pricing
  with a new name (EV-0299). Alongside it: counting cash as revenue
  (EV-0297), a renewal that treats silence as consent (EV-0298), and a
  price rise announced with a demand cause (EV-0292).
- **A margin percentage carried over from a different business**, or a
  price copied from a competitor whose cost base and funding you do not
  share. Competition-informed pricing is legitimate under its conditions
  (EV-0288); copying a funded rival's loss-leader is not one of them.
- **Declaring value-based pricing without building the value
  assessment.** That produces a higher number with no argument behind it
  (EV-0287). The cheap version of the same error is calling the price
  sensitivity meter crossing point the price, which the vendor says it
  is not (EV-0290).
- **A decoy tier.** It is on the regulator's harmful list (EV-0300) and
  only eleven of ninety-one replication attempts found the effect with
  realistic stimuli (EV-0293). Liability on one side, no reliable
  benefit on the other.
- **A fixed trial length with no test plan**, or a trial test judged on
  immediate conversion alone when the stage that moved was the delayed
  one (EV-0294, EV-0295).
- **Lifetime value as revenue over blended churn.** Wrong in a knowable
  direction (EV-0296).
- **Metering something the buyer cannot forecast or control.** That
  converts a pricing model into a support queue.
- **Quoting a benchmark from usage-based-pricing marketing.** See the
  open question below.

## Open questions and counter-evidence

**Usage-based pricing has no causal evidence here.** The widely repeated
claims that usage-based firms retain better trace back to vendor surveys
and blog aggregations, and they are exposed to survivorship and
self-selection: firms whose customers grow adopt usage pricing and also
retain better. No source worth recording was found at the cutoff that
isolates the effect. This pack therefore carries the structural argument
for metering (EV-0297 on obligations, EV-0296 on why expansion and
contraction wreck a blended projection) and no benchmark number from
that literature.

**The two pricing-practice sources disagree about what cost-plus is.**
One treats cost and competitor anchoring as capability failure to be
overcome (EV-0287), the other as conditionally rational (EV-0288). D1
takes the reconciliation: name the practice and the condition, set a
date, and skip the allegiance.

**Hypothetical willingness-to-pay methods are unsettled.** The
comparison against real purchases favours incentive-compatible methods
(EV-0289), while published evaluations report the price sensitivity
meter reaching predictive quality comparable to the incentive-aligned
mechanism despite its bias (EV-0290). D6 assumes neither settles it.

**Metric definitions rest on internal reasoning.** D5 is the weakest
rule in the pack by provenance, and it stays a default for that reason.
Financial controls for a one-person venture are worse off still: nothing
was found on controls proportionate to a venture where segregation of
duties is unavailable, so nothing has been written.

**Trial-length evidence is two single firms.** Both are randomised field
experiments, which is the strongest grade in this pack, and both are one
firm in one category. Neither transfers to B2B pilots with procurement,
or to a product whose value only appears after a full billing cycle.

**Legal rows are dated, not permanent.** The DMCC subscription chapter
is enacted and not commenced. The VAT threshold and the MTD timetable
move at fiscal events, and the MTD dates have moved before.

**Refresh triggers.** Re-argue this pack on: commencement regulations
for DMCC Part 4 Chapter 2; a revision of CMA207 or CMA209; a Budget
change to the VAT registration threshold; an HMRC change to the MTD
timetable; a multi-firm trial-length experiment; a causal study of
usage-based versus seat-based pricing; obtaining the full text behind
EV-0288.

## Evidence pointer

The eighteen sources behind this pack were frozen at
`packs/business-model-pricing/research/sources.fragment.json` and have
since been imported into `registry/evidence.json` as EV-0287 to EV-0304.
Every `EV-` id cited above resolves to a row there carrying version,
licence, access date and review trigger. Six rows come from earlier
estate research rather than this pack's sweep: the two public handbooks
(EV-0055, EV-0095), the error budget policy (EV-0096), the FinOps
allocation (EV-0197) and the two engineering-metric sources behind D5
(EV-0199, EV-0210). The synthesis is in
`packs/business-model-pricing/research/NOTES.md`, and the licence and
quotation sweep is at
`packs/business-model-pricing/research/provenance.fragment.json`. That
sweep is the weakest part of this pack's provenance: twelve of the
twenty-five rows it cites carry a licence nobody has confirmed, most of
them publisher-copyright papers read through abstracts or author-hosted
copies.
