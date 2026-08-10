---
summary: Where a domain rule lives, how much model it earns, and the money, time and lifecycle types that stop it being quietly wrong
type: playbook
tags: [arch, data, money, product]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule, models_money, models_time, has_lifecycle_state]
activation_paths: [**/domain/**, **/models/**, **/rules/**, **/entities/**, **/*pricing*.py, **/*billing*.py, **/*eligibility*, **/state_machine*, **/*invariant*]
volatility: slow
review: 2027-09
sources: [EV-0010, EV-0017, EV-0071, EV-0098, EV-0099, EV-0100, EV-0138, EV-0150, EV-0157, EV-0163, EV-0188, EV-0206, EV-0269, EV-0270, EV-0271, EV-0272, EV-0273, EV-0274, EV-0275, EV-0276, EV-0277, EV-0278, EV-0279, EV-0280, EV-0281, EV-0282, EV-0283, EV-0284, EV-0285, EV-0286]
---

# Business logic and modelling pack

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

## Binding requirements

Two requirements bind. Each names its predicate, its evidence, its basis
and the failure it prevents. Everything else here is a default or a
preference, which in a domain this young is the honest split.

The authority audit under ADR-0008 moved three of the original five to
defaults, and the reason is the same in all three cases: each said
`Basis: decision`, and each rested on a practitioner essay rather than
on law, a standard or a measurement. The type-narrowing rule is now D9,
the outbox rule is D10 and the event-pattern naming rule is D11. The two
that stayed keep their numbers and their basis is `standard` in both
cases.

**B1. Money is an integer count of minor units carrying its currency
code.** `models_money`. No float, no bare number, no assumption that the
exponent is two. The published lists carry an alphabetic code, a numeric
code and a minor unit exponent per currency, and that exponent varies
(EV-0283); the largest payment provider represents every amount the same
way (EV-0284). Arithmetic between two currencies is refused rather than
coerced, and a stored amount keeps the code it was denominated in,
because currencies retire (EV-0283). Prevents the defect nobody sees
until reconciliation: binary fractions that do not sum, and a total out
by a factor of a hundred in the one currency nobody tested. Basis:
standard. See
`packs/business-logic-modelling/refs/MONEY_AND_CURRENCY.md`.

**B2. A timestamp that will be compared or advanced carries a zone
identifier, not just an offset.** `models_time`. An offset is a single
number; a zone identifier such as Europe/London is a function from
instants to offsets, and only the second answers what one day later
means across a daylight-saving change (EV-0281). A naive timestamp with
no zone is refused outright. Prevents the bug that appears twice a year
and always in production: a hold that expires an hour early, a renewal
that bills twice, a report whose day boundary moves. Basis: standard.
See `packs/business-logic-modelling/refs/TIME_TYPES.md`.

Nothing here lowers a tier floor in `kernel/POLICY_SPEC.md` or converts
a guarded action under `kernel/GUARD_SPEC.md`. Money movement is a
guarded action whatever this pack says about modelling it.

## Defaults

Followed unless the venture's lock-book records a reason to depart.

**D1. Start with no model and earn the next step.** Logic in ordinary
functions until a named invariant spans more than one object. Reason: a
speculative model charges build cost, delay cost, carry cost on every
later change, and repair cost when the guess proves wrong (EV-0273). The
threshold is ours rather than any source's, and it is argued in
`packs/business-logic-modelling/guides/GD-BLM-001-model-shape.md`.

**D2. An aggregate boundary is a transactional consistency boundary and
nothing else.** One aggregate per transaction, references to other
aggregates by identity only, small clusters preferred (EV-0269), and the
boundary written up in the field set of
`packs/business-logic-modelling/refs/BOUNDARY_WRITE_UP.md` (EV-0270).
Reason: the field set makes the design reviewable, and a long list of
corrective policies is the tell that logic leaked out of the boundary.
Both sources are consulting experience with no measurement behind them.

**D3. A lifecycle with forbidden transitions is an explicit machine, and
an illegal transition raises rather than doing nothing quietly.** A
declared machine refuses what a set of booleans merely fails to notice,
and hierarchy plus parallel regions stop the state explosion that makes
flat machines unusable (EV-0279, EV-0280). Reason: a silent no-op leaves
the caller believing the change happened. Depart when the lifecycle has
no forbidden transition at all.

**D4. One time dimension until somebody has actually had to answer a
two-dimensional question.** Add valid time and transaction time
together, or neither (EV-0275). Reason: the second dimension answers
what we thought was true when we ran the payroll, and it complicates
every reader of the model, which is the over-modelling D1 refuses.
Depart once a correction, a dispute or a reprocessing has been asked for
and the answer was not available.

**D5. Choose the narrowest temporal type that holds the fact.** A
birthday is a plain date, an opening time is a wall-clock time, a
deadline is a zoned date-time, a log line is an instant (EV-0282).
Reason: a wide type silently invents a zero, a zone or a UTC assumption
for a value that is genuinely unknown.

**D6. Rules stay in code until they change on a different clock from the
code.** When they do, move them to a flat decision table with declared
inputs, outputs and overlap handling, never to a chaining inference
engine (EV-0277, EV-0278). Reason: with chaining, one rule's action
satisfies another's condition and nobody predicts the outcome from
reading any single rule (EV-0274), while a flat table is a closed form
whose completeness is machine-checkable. A handful of rules earns
neither. See
`packs/business-logic-modelling/guides/GD-BLM-002-rule-placement.md`.

**D7. Conversion between domain money and any external money happens in
one adapter.** The minor-unit exponent is a property of a currency in a
context, not of the currency alone: the same provider charges some
currencies with two decimals and pays them out whole (EV-0284). Reason:
one place to be wrong, and the domain keeps one representation
(EV-0150).

**D8. State-stored until replay is the requirement.** Event sourcing
charges in three places: replay must not re-fire external effects, must
not re-read external data at today's values, and old event shapes must
stay readable (EV-0276). Reason: audit alone is a bad reason to adopt
it, because a log is cheaper.

**D9. A constraint expressible in the constructor or the type is
expressed there.** `encodes_domain_rule`. A value that cannot legally
exist cannot be constructed, and narrowing happens at the boundary as
early as possible, so nothing downstream re-checks and nothing forgets
(EV-0285). A separate `validate` or `is_valid` method a caller may skip
does not satisfy it. Reason: scattered checking is how inconsistent
state gets in. This is a default rather than binding because EV-0285 is
a practitioner essay whose own author states it as an ideal, and because
the failure it names is a structural weakness rather than a serious or
irreversible event. Where the language cannot restrict construction, a
constructor-enforced value object is the equivalent; where neither is
available, record what checks instead.

**D10. A state change and its outbound message are committed together or
not at all.** `crosses_consistency_boundary`. The message goes to an
outbox written in the same transaction as the state change, and every
consumer is idempotent (EV-0157). Reason: otherwise the state is saved
with the event lost, or the event is sent with the state rolled back,
and nothing in the system can tell you which happened. This is a default
rather than binding because EV-0157 is a pattern catalogue with no
measurement behind it; the failure is real, the evidence is a
description. Depart only with a written account of how the two writes
are reconciled instead, and note that the pattern buys at-least-once
delivery and nothing more, which is why the idempotence half is not the
part to drop.

**D11. A change that publishes or consumes events names which of the
four patterns it means.** `crosses_consistency_boundary`. Event
notification, event-carried state transfer, event sourcing and CQRS are
four different things, and failures get attributed to event-driven
architecture in general when one of them was responsible (EV-0163). A
change record saying "we went event-driven" does not satisfy it. Reason:
otherwise the argument cannot be settled, because the parties mean
different things. This is a default rather than binding because the
failure is an argument nobody can settle, which costs time and nothing
else, and because EV-0163 is a definitional essay with no measurement.

## Preferences

Taste. Record them, do not gate on them, and depart without asking.

- **Ubiquitous language naming, the ddd-crew canvases and the starter
  process as thinking aids** (EV-0098, EV-0099, EV-0100). Their own
  maintainers warn against institutionalising the process, so the estate
  does not, and the strongest review reports onboarding cost and scarce
  expertise as recurring problems (EV-0286).
- **Event storming as the discovery method** (EV-0271). A past-tense
  business event is a good unit of conversation, and the source sells
  training, has nothing controlled behind it, and transfers nothing to
  an agent working alone.
- **Object-shaped or function-shaped domain layers.** Behaviour-free
  objects with every rule in a service are called an anti-pattern
  (EV-0272), and the same source is content with a procedural service
  layer over a rich model.
- **Property-based tests for domain invariants** (EV-0017, EV-0188),
  which the delivery-testing pack owns properly.
- **A small purpose-built evaluator over a standards-grade engine**
  where a table is wanted and a second runtime is not (EV-0274,
  EV-0071).

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| How much model does this domain earn | Procedures, aggregates, types or declarations | `packs/business-logic-modelling/guides/GD-BLM-001-model-shape.md` |
| Where does this rule live | Code, table, machine or engine | `packs/business-logic-modelling/guides/GD-BLM-002-rule-placement.md` |
| How is money represented and converted | Type, rounding, allocation, adapter | `packs/business-logic-modelling/guides/GD-BLM-003-money-representation.md` |
| How much time does this fact carry | Type width and number of dimensions | `packs/business-logic-modelling/guides/GD-BLM-004-time-modelling.md` |
| State or events as the record | Storage, replay, corrections, erasure | `packs/business-logic-modelling/guides/GD-BLM-005-state-or-events.md` |

Detail sits in `packs/business-logic-modelling/refs/`, a worked run in
`packs/business-logic-modelling/exemplars/`, and what a reviewer or
script can verify in `packs/business-logic-modelling/CHECKS.md`.

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
