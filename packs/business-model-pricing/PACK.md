---
summary: Activation, outcomes and decision map for the business-model-pricing Doctrine and Wargames
type: pack
tags: [money, product, eos]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [sets_a_price, publishes_a_price, sells_to_consumers, sells_by_subscription, sells_to_public_sector, bundles_or_discounts, reports_commercial_metrics]
activation_paths: [**/pricing/**, **/*pricing*.md, **/plans/**, **/tiers/**, **/*subscription*, **/*checkout*, **/*invoice*]
volatility: event-driven
review: none
sources: [EV-0287, EV-0288, EV-0289, EV-0290, EV-0291, EV-0292, EV-0293, EV-0294, EV-0295, EV-0296, EV-0297, EV-0298, EV-0299, EV-0300, EV-0301, EV-0302, EV-0303, EV-0304, EV-0055, EV-0059, EV-0095, EV-0096, EV-0197, EV-0199, EV-0210]
display_name: Business Models and Pricing
category: product-commercial
id_namespace: BMP
depends_on: [product-discovery, legal-licensing]
---


# Business Models and Pricing

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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-BMP-001](doctrines/DOC-BMP-001-the-headline-price-includes-every-unavoidable-charge.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-BMP-002](doctrines/DOC-BMP-002-a-consumer-subscription-can-be-entered-knowingly-and-left.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-BMP-003](doctrines/DOC-BMP-003-revenue-is-recognised-never-counted-at-the-bank.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-BMP-004](doctrines/DOC-BMP-004-tax-thresholds-are-watched-as-pricing-events.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-BMP-005](doctrines/DOC-BMP-005-open-on-a-named-practice-with-its-condition-and-a-revisit.md) (default)
<a id="D2"></a>
- `D2` to [DOC-BMP-006](doctrines/DOC-BMP-006-a-price-change-is-announced-with-its-cause-and-the-cause-is.md) (default)
<a id="D3"></a>
- `D3` to [DOC-BMP-007](doctrines/DOC-BMP-007-trial-length-starts-near-a-week-and-is-tested-across-the.md) (default)
<a id="D4"></a>
- `D4` to [DOC-BMP-008](doctrines/DOC-BMP-008-retention-is-reported-as-a-cohort-curve-and-lifetime-value.md) (default)
<a id="D5"></a>
- `D5` to [DOC-BMP-009](doctrines/DOC-BMP-009-every-commercial-number-travels-with-its-definition.md) (default)
<a id="D6"></a>
- `D6` to [DOC-BMP-010](doctrines/DOC-BMP-010-a-survey-derived-price-is-a-bracket-never-the-decision.md) (default)
<a id="D7"></a>
- `D7` to [DOC-BMP-011](doctrines/DOC-BMP-011-unit-cost-is-allocated-before-a-margin-is-claimed.md) (default)
<a id="D8"></a>
- `D8` to [DOC-BMP-012](doctrines/DOC-BMP-012-the-repricing-trigger-is-written-before-it-fires.md) (default)
<a id="D9"></a>
- `D9` to [DOC-BMP-013](doctrines/DOC-BMP-013-payment-terms-are-written-down-because-they-exist-either-way.md) (default)
<a id="D10"></a>
- `D10` to [DOC-BMP-014](doctrines/DOC-BMP-014-no-pattern-from-the-regulators-almost-always-harmful-list.md) (default)
- source `preferences:001` to [DOC-BMP-015](doctrines/DOC-BMP-015-price-endings.md) (preference)
- source `preferences:002` to [DOC-BMP-016](doctrines/DOC-BMP-016-tier-count-and-tier-names.md) (preference)
- source `preferences:003` to [DOC-BMP-017](doctrines/DOC-BMP-017-whether-a-public-price-exists-at-all.md) (preference)
- source `preferences:004` to [DOC-BMP-018](doctrines/DOC-BMP-018-publishing-the-commercial-policy-in-a-public-handbook.md) (preference)

## Decision map

| Fork | Wargame | Default |
| --- | --- | --- |
| What is this price anchored to? | `packs/business-model-pricing/wargames/WG-BMP-001-price-anchor.md` | Cost-informed or competition-informed opening, with a dated move to value evidence |
| What is the unit of charge? | `packs/business-model-pricing/wargames/WG-BMP-002-charging-unit.md` | The simplest unit the buyer can forecast |
| How does someone try this before paying? | `packs/business-model-pricing/wargames/WG-BMP-003-try-before-paying.md` | A time-boxed trial near a week, with a test plan |
| When and how does the price change? | `packs/business-model-pricing/wargames/WG-BMP-004-repricing-trigger.md` | A written cost-or-value trigger, announced with its cause |

Level-three detail: the artefacts a decision has to emit are in
`packs/business-model-pricing/references/DECISION_RECORD.md`, the dated duties
in `packs/business-model-pricing/references/UK_OBLIGATIONS.md`, the cohort
method in `packs/business-model-pricing/references/RETENTION_AND_LTV.md`, the
house metrics in
`packs/business-model-pricing/references/METRIC_DEFINITIONS.md`, and a worked
run in
`packs/business-model-pricing/examples/EX-BMP-001-first-consumer-subscription.md`.

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
licence, access date and review trigger. Seven rows come from earlier
estate research rather than this pack's sweep: the two public handbooks
(EV-0055, EV-0095), the error budget policy (EV-0096), the FinOps
allocation (EV-0197), the two engineering-metric sources behind D5
(EV-0199, EV-0210) and the experiment decision framework the trial
Wargame uses (EV-0059). The synthesis is in
`packs/business-model-pricing/research/NOTES.md`, and the licence and
quotation sweep is at
`packs/business-model-pricing/research/provenance.fragment.json`. That
sweep is the weakest part of this pack's provenance: twelve of the
twenty-five rows it cites carry a licence nobody has confirmed, most of
them publisher-copyright papers read through abstracts or author-hosted
copies.
