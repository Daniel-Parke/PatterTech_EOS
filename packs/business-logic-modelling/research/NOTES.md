---
summary: What the evidence supports for the business logic and modelling pack, four contrasting philosophies with fit conditions, and the binding versus default versus preference split
type: example
tags: [eos, testing]
---

# Business logic and modelling research notes

Cutoff 2026-08-03. Eighteen new sources in `sources.fragment.json`,
plus ledger evidence already held: ddd-crew Bounded Context Canvas,
Context Mapping and Starter Modelling Process (EV-0098, EV-0099,
EV-0100), Fowler on event-driven patterns (EV-0163), transactional
outbox (EV-0157), parallel change (EV-0206), hexagonal architecture
(EV-0150), CloudEvents (EV-0138), Open Policy Agent (EV-0071),
property-based testing (EV-0017, EV-0188) and the METR RCT (EV-0010).
Read the pack against one fact first. The only systematic review here
(FRAG-18, 36 peer-reviewed studies) finds domain-driven design has
demonstrated value for decomposing systems, that several of its own
primaries carried no empirical evaluation at all, and that onboarding
cost and scarce expertise recur as problems. Everything else is
practitioner argument, standards and maintained tooling. That is not
nothing, but it is not a licence to make tactical DDD binding.

## The four philosophies, and when each fits

### 1. No model: procedures over data

Logic lives in ordinary functions that read, decide and write. No
domain layer, no mapping, no ubiquitous-language ceremony.

Fits when rules are thin, the system mostly moves data between a form
and a table, and nobody can name an invariant spanning two rows.
FRAG-05 is the argument for staying here: a speculative model is not a
free option, it charges carry cost on every later change, delay cost on
the work that mattered, and repair cost when the guess proves wrong.

Anti-patterns: the middle position FRAG-04 attacks, paying the full
price of entities and mapping then putting every rule in a service
anyway; and assuming the shape stays cheap after the rules thicken,
since the tell (one condition re-checked in four places) is only
visible if somebody looks.

### 2. Aggregates: the boundary is the transaction

Cluster what must never be observed inconsistent, make one thing the
entry point, reconcile the rest afterwards. FRAG-01 gives four rules:
only a true invariant justifies a boundary, one aggregate per
transaction, reference other aggregates by identity, everything outside
is eventually consistent. FRAG-02 turns that into a reviewable form:
enforced invariants, handled commands, created events, state
transitions, corrective policies, throughput, size.

Fits when a real invariant spans several objects, concurrent writes to
the same cluster are likely, and different rules tolerate different
staleness.

Trade-off: eventual consistency is not free. It needs the outbox
(EV-0157) so state and event cannot diverge, and every consumer
idempotent, because that pattern buys at-least-once and nothing more.
Anti-patterns: the aggregate grown to hold every association a screen
wants, which FRAG-01 names as the common failure; a long list of
corrective policies, which FRAG-02 treats as logic leaking out of the
boundary; and fixing boundaries early, which FRAG-01's own third part
contradicts by showing first designs superseded.

### 3. Types: make the illegal state unrepresentable

Push the invariant into the shape of the data so the check cannot be
skipped. FRAG-17: a validating function throws away what it learned, a
parsing function returns a value carrying the proof, so nothing
downstream re-checks and nothing forgets. Narrow at the boundary, as
early as possible. FRAG-14 applies the same move to time, where seven
distinct types replace one timestamp and stop code silently assuming
zero, UTC or local. FRAG-15 applies it to money: an integer count of
minor units plus a currency code, since the exponent varies by currency
and is not always two.

Fits everywhere a scalar is not really a scalar: money, dates,
identifiers, quantities with units, constrained strings. Cheapest
enforcement in the pack, costing nothing at runtime and impossible to
bypass. Limits: FRAG-17 concedes some invariants are hard to type, and
the argument weakens where construction cannot be restricted, leaving a
constructor-checked value object as the equivalent. Invariants spanning
several objects hand back to philosophy 2.

Anti-patterns: a wrapper type per field with no invariant inside it;
and validating at the boundary while still passing the raw shape
inwards, which is the scattered-checking failure the source names.

### 4. Declarative logic: tables, machines and engines

Take the decision out of control flow and put it in a closed form with
declared inputs, outputs and evaluation. FRAG-09 (DMN 1.5) is the
standard for decisions: a requirements graph plus decision tables in a
defined expression language, making completeness and overlap
machine-checkable in a way a chain of conditionals is not. FRAG-11 and
FRAG-12 are the lifecycle version: a statechart with hierarchy and
parallel regions, so illegal transitions are refused by the machine and
state does not explode the way a flag per condition does.

Fits when rules change on a different clock from the code, when the
condition combinations exceed what anyone holds in their head, or when
a lifecycle has transitions that must never happen.

Trade-off: an engine is a second runtime, artefact and deployment story
(FRAG-10), which for a handful of rules is exactly the carry cost of
FRAG-05. Anti-pattern: chaining. FRAG-06 is the strongest warning
here. When one
rule's action satisfies another's condition, nobody predicts the
outcome from reading any single rule, and a rule set big enough to need
a clever matching algorithm for speed is already too big to reason
about. The related myth, that business people will maintain the rules,
is named there as the thing that usually fails.

## Cross-cutting: time and money

Time. FRAG-13 is unambiguous: a UTC offset is not a time zone. An
offset is a number, a zone identifier is a function from instants to
offsets, and only the second answers what one day later means across a
daylight-saving boundary. FRAG-07 adds the second dimension: where a
fact can be corrected later, you need when it was true and when we came
to believe it, or you cannot answer what we thought the rate was when
we ran the payroll. That dimension costs, and FRAG-07 concedes it
complicates every reader, so it is a decision, not a default.

Money. Integer minor units plus a currency code, never a float
(FRAG-15). Currencies retire, so an amount keeps the code it was
denominated in. FRAG-16 shows the exponent is a property of a currency
in a context: the same processor charges some currencies with two
decimals and pays them out whole, so conversion between domain money
and any external system belongs in one adapter and nowhere else.

## Where the sources disagree

- **Rich entities versus everything else.** FRAG-04 calls
  behaviour-free objects an anti-pattern, yet concedes a procedural
  service layer over a rich model is fine, and the best-supported
  techniques here (FRAG-17, FRAG-09) put correctness in types and
  tables, not entity methods. FRAG-18 then finds DDD's demonstrated
  value is decomposition, not correctness. This is the load-bearing
  contradiction: object-shaped domain logic cannot be binding.
- **Rule engines.** FRAG-06 (2009) argues against externalised rules on
  interaction complexity. FRAG-09 and FRAG-10 show a standardised,
  non-chaining table form that answers the objection. The critique
  survives for chaining inference and not for flat tables, so any rule
  must name which is meant.
- **Process discipline.** EV-0100's maintainers warn against
  institutionalising their own process, and FRAG-01's third part argues
  designs should be superseded. Both cut against a fixed pipeline.
- **Event sourcing.** FRAG-08 is candid about three costs: replay must
  not re-fire effects, must not re-read external data at today's
  values, and old event shapes must stay readable. It names audit alone
  as a bad reason to adopt, and it predates erasure obligations against
  an immutable log.
- **Currency authority.** FRAG-15 and FRAG-16 disagree on minor units
  for specific currencies, so no single currency table is
  authoritative across a whole system.

## Binding, default, preference

Binding, because violating them produces wrong answers found late or
never:

1. Money is an integer count of minor units carrying its currency code.
2. A timestamp that will be compared or advanced carries a zone
   identifier, not just an offset.
3. A constraint expressible in the constructor or the type is expressed
   there, not in a check the caller can skip.
4. A state change followed by an outbound message goes through the
   outbox (EV-0157), and every consumer is idempotent.

Default, unless the change record argues otherwise:

1. Start at philosophy 1. Introduce an aggregate when a named invariant
   spans more than one object, and write it in the FRAG-02 field set.
2. One aggregate per transaction; cross-aggregate references by
   identity.
3. A lifecycle with forbidden transitions is an explicit machine, not a
   set of booleans.
4. One time dimension. Add the second only against a question somebody
   has actually had to answer.

Preference, argued per venture: ubiquitous-language naming, event
storming as the discovery method, DMN versus a small purpose-built
evaluator, object-shaped versus function-shaped domain layers.

## Open questions, honestly

- No source measures whether aggregate sizing affects defect or
  contention rates. FRAG-01 is consulting experience.
- Nothing tells us how this behaves when agents write the code. FRAG-18
  does not cover it and EV-0010 says our intuitions are unreliable.
- The threshold between philosophy 1 and philosophy 2 is the most
  useful rule the pack could state, and no source states it. Writing
  one means inventing it.
- Erasure against an append-only log is unresolved by every source read
  here.
- FRAG-12 was read at abstract level only and FRAG-09's decision-table
  hit policies were not verified, so neither carries a detailed rule.
