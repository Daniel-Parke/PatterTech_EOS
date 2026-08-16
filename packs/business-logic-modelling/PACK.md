---
summary: Activation, outcomes and decision map for the business-logic-modelling Doctrine and Wargames
type: pack
tags: [arch, data, money, product]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [encodes_domain_rule, models_money, models_time, has_lifecycle_state]
activation_paths: [**/domain/**, **/models/**, **/rules/**, **/entities/**, **/*pricing*.py, **/*billing*.py, **/*eligibility*, **/state_machine*, **/*invariant*]
volatility: slow
review: none
sources: [EV-0010, EV-0017, EV-0071, EV-0098, EV-0099, EV-0100, EV-0138, EV-0150, EV-0157, EV-0163, EV-0188, EV-0206, EV-0269, EV-0270, EV-0271, EV-0272, EV-0273, EV-0274, EV-0275, EV-0276, EV-0277, EV-0278, EV-0279, EV-0280, EV-0281, EV-0282, EV-0283, EV-0284, EV-0285, EV-0286]
display_name: Business Logic and Domain Modelling
category: engineering
id_namespace: BLM
depends_on: [product-discovery]
---


# Business Logic and Domain Modelling

This pack covers business logic: where a domain rule lives, what shape
the model takes, and how money, time and lifecycle state are represented
so the rules cannot be quietly wrong. It activates on any task that
writes or changes a rule a business person could argue with, stores or
computes an amount of money, compares or advances a date, or gives a
thing a status with transitions.

## Activation

**Paths touched.** Any module named for the domain rather than the
machinery: domain, model, models, entities, rules, policy, pricing,
billing, ledger, invoice, subscription, booking, scheduling. Decision
tables and state machine definitions in any format. Migrations that
touch a column holding an amount, a currency, a timestamp or a status.

**Task types.** Model a new domain concept. Add, change or delete a
business rule. Compute a price, a total, a proration or a balance. Give
a thing a status, or move it between statuses. Answer a question about
when a thing was true. Review any of those.

**Keywords, fallback only.** Domain model, aggregate, entity, value
object, invariant, business rule, decision table, state machine,
lifecycle, currency, rounding, proration, timezone, daylight saving,
effective date, event sourcing. Keywords never override the predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| encodes_domain_rule | the change writes a condition a business person could argue with |
| models_money | an amount of money is stored, computed or compared |
| models_time | a date or timestamp is stored, compared or advanced |
| has_lifecycle_state | a thing carries a status with transitions somebody could get wrong |
| crosses_consistency_boundary | one operation changes two things that could be observed apart |
| rules_change_independently | the rules change on a different release clock from the code |

Do not load this pack for pure plumbing: transport, serialisation,
retries, logging and deployment carry no domain rule. A task that trips
a path trigger and satisfies no predicate loads nothing beyond the first
paragraph.

## Outcomes and non-goals

**Outcomes.** A rule somebody can argue with is written where somebody
can find it. An invariant is enforced where it cannot be skipped rather
than re-checked in four places. An amount of money survives arithmetic,
storage and a trip through a payment provider without losing a penny or
changing currency. A date question has one right answer across a
daylight-saving boundary. A lifecycle refuses the transitions that must
never happen. The model is the smallest one that holds the invariant,
and the reason it grew is recorded.

**Non-goals.** This pack does not own service boundaries, data topology
or deployment shape, which sit in `packs/architecture/PACK.md`. It does
not own migration mechanics or expand-and-contract sequencing, which sit
in `packs/devops-reliability/PACK.md` and EV-0206. It does not own test
strategy, which sits in `packs/delivery-testing/PACK.md`. It does not
own wire contracts or event envelopes, which sit in
`packs/api-integration/PACK.md` and EV-0138. It does not own tax,
accounting or regulatory rules, which are venture facts in `registry/`,
never doctrine. It does not adopt domain-driven design as a house
method: the strongest review of DDD finds demonstrated value in
decomposition and thin support for anything else (EV-0286).

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-BLM-001](doctrines/DOC-BLM-001-money-is-an-integer-count-of-minor-units-carrying-its.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-BLM-002](doctrines/DOC-BLM-002-a-timestamp-that-will-be-compared-or-advanced-carries-a-zone.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-BLM-003](doctrines/DOC-BLM-003-start-with-no-model-and-earn-the-next-step.md) (default)
<a id="D2"></a>
- `D2` to [DOC-BLM-004](doctrines/DOC-BLM-004-an-aggregate-boundary-is-a-transactional-consistency.md) (default)
<a id="D3"></a>
- `D3` to [DOC-BLM-005](doctrines/DOC-BLM-005-a-lifecycle-with-forbidden-transitions-is-an-explicit.md) (default)
<a id="D4"></a>
- `D4` to [DOC-BLM-006](doctrines/DOC-BLM-006-one-time-dimension-until-somebody-has-actually-had-to-answer.md) (default)
<a id="D5"></a>
- `D5` to [DOC-BLM-007](doctrines/DOC-BLM-007-choose-the-narrowest-temporal-type-that-holds-the-fact.md) (default)
<a id="D6"></a>
- `D6` to [DOC-BLM-008](doctrines/DOC-BLM-008-rules-stay-in-code-until-they-change-on-a-different-clock.md) (default)
<a id="D7"></a>
- `D7` to [DOC-BLM-009](doctrines/DOC-BLM-009-conversion-between-domain-money-and-any-external-money.md) (default)
<a id="D8"></a>
- `D8` to [DOC-BLM-010](doctrines/DOC-BLM-010-state-stored-until-replay-is-the-requirement.md) (default)
<a id="D9"></a>
- `D9` to [DOC-BLM-011](doctrines/DOC-BLM-011-a-constraint-expressible-in-the-constructor-or-the-type-is.md) (default)
<a id="D10"></a>
- `D10` to [DOC-BLM-012](doctrines/DOC-BLM-012-a-state-change-and-its-outbound-message-are-committed.md) (default)
<a id="D11"></a>
- `D11` to [DOC-BLM-013](doctrines/DOC-BLM-013-a-change-that-publishes-or-consumes-events-names-which-of.md) (default)
- source `preferences:001` to [DOC-BLM-014](doctrines/DOC-BLM-014-ubiquitous-language-naming-the-ddd-crew-canvases-and-the.md) (preference)
- source `preferences:002` to [DOC-BLM-015](doctrines/DOC-BLM-015-event-storming-as-the-discovery-method.md) (preference)
- source `preferences:003` to [DOC-BLM-016](doctrines/DOC-BLM-016-object-shaped-or-function-shaped-domain-layers.md) (preference)
- source `preferences:004` to [DOC-BLM-017](doctrines/DOC-BLM-017-property-based-tests-for-domain-invariants.md) (preference)
- source `preferences:005` to [DOC-BLM-018](doctrines/DOC-BLM-018-a-small-purpose-built-evaluator-over-a-standards-grade.md) (preference)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| How much model does this domain earn | Procedures, aggregates, types or declarations | `packs/business-logic-modelling/wargames/WG-BLM-001-model-shape.md` |
| Where does this rule live | Code, table, machine or engine | `packs/business-logic-modelling/wargames/WG-BLM-002-rule-placement.md` |
| How is money represented and converted | Type, rounding, allocation, adapter | `packs/business-logic-modelling/wargames/WG-BLM-003-money-representation.md` |
| How much time does this fact carry | Type width and number of dimensions | `packs/business-logic-modelling/wargames/WG-BLM-004-time-modelling.md` |
| State or events as the record | Storage, replay, corrections, erasure | `packs/business-logic-modelling/wargames/WG-BLM-005-state-or-events.md` |

Detail sits in `packs/business-logic-modelling/references/`, a worked run of
one renewal through money, time and lifecycle at
`packs/business-logic-modelling/examples/EX-BLM-001-subscription-renewal.md`,
and what a reviewer or script can verify in
`packs/business-logic-modelling/CHECKS.md`.

## Failure modes and anti-patterns

- **Float money, and two decimal places hard-coded.** The commonest
  pair. Both survive every test with round numbers, and both fail on the
  first reconciliation or the first zero-decimal currency (EV-0283,
  EV-0284).
- **Offset stored instead of zone, or a naive local datetime.**
  Arithmetic is right for ten months of the year, and the comparison
  looks fine while meaning nothing (EV-0281).
- **The validate method nobody calls.** A check the caller can skip is a
  suggestion rather than an invariant (EV-0285).
- **The god aggregate**, holding every association a screen wanted,
  loaded on every write and contended by every user (EV-0269), and its
  cousin the long list of corrective policies, which is logic that
  should sit inside the boundary leaking into compensating handlers
  (EV-0270).
- **Anaemic and expensive at once.** Full mapping and lifecycle cost
  paid, every rule in a service anyway (EV-0272). Either put the rules
  where the data is or do not build the model.
- **Booleans standing in for a lifecycle.** `is_active`, `is_cancelled`
  and `is_complete` on one row, three of the eight combinations
  meaningless and none of them refused (EV-0279).
- **The rule engine bought for eleven rules**, and worse, a chaining
  one. A second runtime for logic that fits on a page, and outcomes
  nobody predicts from reading any single rule (EV-0274, EV-0278).
- **Event sourcing adopted for audit.** A log is cheaper and does not
  make erasure a research problem (EV-0276).
- **Bitemporality by default.** Every reader of the model pays, and
  nobody has asked the question yet (EV-0275).
- **Aggregate boundaries treated as permanent.** The source that gives
  the rules spends its third part on first designs being superseded
  (EV-0269).

## Open questions and counter-evidence

**The threshold is ours.** D1 says start with no model and grow when a
named invariant spans more than one object. No source states that
threshold: one gives the costs of over-modelling (EV-0273) and another
the costs of the middle position (EV-0272), and the line between them is
an estate decision. It is the first thing to re-argue if a venture finds
it in the wrong place.

**Object-shaped domain logic cannot be binding.** One source calls
behaviour-free objects an anti-pattern (EV-0272), the best-supported
techniques here put correctness in types and tables rather than entity
methods (EV-0285, EV-0277), and the systematic review finds DDD's
demonstrated value is decomposition (EV-0286). That contradiction is why
tactical DDD sits in preferences.

**The evidence base is thin and mostly practitioner argument.** The one
systematic review here covers 36 peer-reviewed studies, reports that
several of its primaries carried no empirical evaluation at all, and
inherits publication bias towards successful adoptions (EV-0286). No
source measures whether aggregate sizing affects defect or contention
rates, and nothing here is measured on agent-written code, where
self-reported speed is not evidence of anything (EV-0010). Everything in
the defaults section is argued rather than measured.

**Rule engines are a live disagreement.** The critique is seventeen
years old and lands hardest on chaining inference (EV-0274). A
standardised non-chaining table form with defined evaluation semantics
answers it (EV-0277, EV-0278). Both survive, which is why D6 separates
the flat table from the chaining engine instead of treating externalised
rules as one choice.

**Currency authority is not single.** The standard lists and the
provider's contract disagree on minor units for specific currencies
(EV-0283, EV-0284), so no currency table is authoritative across a whole
system. That is the reason for D7 rather than an argument against either
source.

**Erasure against an append-only log is unresolved.** Every source read
here predates the obligation or ignores it (EV-0276), so anyone adopting
event sourcing over personal data is on their own and
`packs/security-privacy/PACK.md` governs.

**Two sources are recorded at reduced confidence.** The statecharts
paper was read at abstract level only and the DMN hit policies were not
verified at access (EV-0280, EV-0277). No rule here rests on the
unverified detail of either.

**Refresh triggers.** Re-argue this pack on: an ISO 4217 amendment
affecting a currency a venture holds; DMN 1.7 reaching formal status; a
controlled study comparing DDD and non-DDD outcomes on matched systems;
the first venture that needs erasure inside an event log.

## Evidence pointer

The eighteen sources behind this pack were frozen at
`packs/business-logic-modelling/research/sources.fragment.json` and have
since been imported into `registry/evidence.json` as EV-0269 to EV-0286.
Every `EV-` id cited above resolves to a row there carrying version or
commit, licence, access date, applicability limits and a review trigger.
The rest are estate rows this pack borrows: the agent productivity
caution (EV-0010), the property-testing rows the delivery-testing pack
owns (EV-0017, EV-0188), the rule-engine row (EV-0071), the
domain-discovery canvases (EV-0098, EV-0099, EV-0100), the event
envelope (EV-0138), ports and adapters (EV-0150), the outbox (EV-0157),
the event-pattern essay (EV-0163) and expand-and-contract (EV-0206). The
synthesis is in `packs/business-logic-modelling/research/NOTES.md`, and
the licence and quotation sweep is at
`packs/business-logic-modelling/research/provenance.fragment.json`. Nine
of the rows this pack cites carry a licence nobody has confirmed, and
several of the rest are all-rights-reserved practitioner essays where
the ledger records paraphrase only.
