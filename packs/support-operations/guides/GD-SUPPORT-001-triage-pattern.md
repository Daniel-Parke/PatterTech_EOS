---
id: GD-SUPPORT-001
summary: How does inbound get classified, and what keeps the queue finite?
kind: wargame
type: wargame
tags: [eos, ops, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-SUPPORT-003]
applies_when: [has_customer_inbound]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0055, EV-0200]
review: on-change-of:ISO-10002-revision
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SUPPORT-001: How does inbound get classified, and what keeps the queue finite?

## Decision question and stakes

Four patterns for handling inbound exist in the wild, and they are not
points on one scale. They differ in what the queue is for: restoring a
service, keeping a backlog honest, discharging an obligation, or
learning what the product feels like to use. Pick the wrong one and
either the cost per item is absurd or the queue grows without bound.

## Doctrines or coverage gap under pressure

- `DOC-SUPPORT-003` (default): Nothing enters a backlog without a classification, and untriaged is a state rather than an absence.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **What the failures look like.** Availability-shaped, where one cause
  hits many people at once, or request-shaped, where each item is its
  own small thing.
- **Whether the reporter pays.** A volunteer on a public tracker and a
  customer under contract are different relationships, and closing on
  silence costs differently in each.
- **How many people can respond.** Role separation needs bodies.
- **Whether the venture still needs to learn what using the product is
  like**, or already knows.
- **Volume against responders.** The arithmetic in PACK.md D8 decides
  this one whatever anybody prefers.

Applicability is `has_customer_inbound`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Severity-first operational triage
Inbound is classified by blast radius first: an ordered ladder, a rule
that takes the higher band when the call is unclear, and one threshold
that mechanically switches the organisation into a different mode.
Communication is a named role held by someone who is not fixing, and
declaration runs on objective triggers rather than judgement
(EV-0421, EV-0423,
EV-0422, EV-0200). Buys a fast, defensible response
when one cause hits many customers, and a record that survives the
postmortem. Costs a written ladder maintained ahead of time, and it
does nothing for a billing question.

### B. Labelled backlog triage
Inbound is labelled on orthogonal axes, kind, priority, owner, plus a
separate accepted flag so untriaged is queryable. Support questions are
routed out of the defect tracker by label rather than answered inside
it, and items lacking reproduction close on a timer
(EV-0424). Buys a finite queue and a backlog whose
priorities can be argued with. Costs real bugs to the timer, which the
maintainers of the project that runs the best-known stale bot have
themselves complained about.

### C. Complaint as a closed loop
Every complaint is acknowledged, owned, resolved and answered, and the
loop closes only when the complainant has been told the outcome. The
route to complain is visible and free. Complaint data is analysed in
aggregate and fed back into the product, so recording without a
periodic synthesis pass is a failure of the process rather than a
missed nicety (EV-0425,
EV-0426). Buys the most defensible position under a
contractual or regulatory relationship, and consistent answers to the
same defect. Costs the most per item, and the management-system
apparatus is disproportionate below a handful of staff.

### D. Founder as the support function
Support is deliberately unscalable and deliberately temporary. The
founder answers everything, operates the product manually on the
customer's behalf where that helps, and treats each contact as product
research (EV-0432, EV-0055). Buys the fastest
product learning available at small numbers, and word of mouth as a
side effect. Costs a ceiling that arrives non-linearly
(EV-0430), and it has no exit signal of its own, so
one has to be written.

## Failure premises

### Premortem for A. Severity-first operational triage

Assume `A. Severity-first operational triage` was selected and the outcome failed. Test this option's stated failure mechanism first: a written ladder maintained ahead of time, and it does nothing for a billing question.

### Premortem for B. Labelled backlog triage

Assume `B. Labelled backlog triage` was selected and the outcome failed. Test this option's stated failure mechanism first: real bugs to the timer, which the maintainers of the project that runs the best-known stale bot have themselves complained about.

### Premortem for C. Complaint as a closed loop

Assume `C. Complaint as a closed loop` was selected and the outcome failed. Test this option's stated failure mechanism first: the most per item, and the management-system apparatus is disproportionate below a handful of staff.

### Premortem for D. Founder as the support function

Assume `D. Founder as the support function` was selected and the outcome failed. Test this option's stated failure mechanism first: a ceiling that arrives non-linearly (EV-0430), and it has no exit signal of its own, so one has to be written.

## Decision rule

Run more than one. The patterns are not exclusive, and the axes in
PACK.md B1 are what let them coexist: the queue axis routes an item to
the pattern that handles it.

Start from D while the founder still learns something new from most
contacts, and write the exit signal on day one. Route anything
availability-shaped and customer-visible to A, from the first paying
customer onwards, because the cost of a late notice is already real at
one customer. Route anything from a paying customer that is a
complaint rather than a question to C. Use B for a public tracker and
for the internal defect backlog, and only there. If the venture has no
paying customers and no public tracker, D alone is honest and A is
still cheap insurance.

## Safe default

D plus A for a pre-revenue venture. D plus A plus C from the first
paying customer. Add B when a public tracker opens or when the defect
backlog outgrows one person's memory. Move off D when the exit signal
fires, which in practice is whichever comes first of the utilisation
figure in PACK.md D8 crossing seventy per cent for two consecutive
weeks, or a month in which no contact taught anything new.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****What the failures look like.** Availability-shaped, where one cause hits many people at once, or request-shaped, where each item is its own small thing.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** D plus A for a pre-revenue venture. D plus A plus C from the first paying customer. Add B when a public tracker opens or when the defect backlog outgrows one person's memory. Move off D when the exit signal fires, which in practice is whichever comes first of the utilisation figure in PACK.md D8 crossing seventy per cent for two consecutive weeks, or a month in which no contact taught anything new.

**Exit condition:** Stop or roll back the selected branch when a written ladder maintained ahead of time, and it does nothing for a billing question, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **What the failures look like.** Availability-shaped, where one cause hits many people at once, or request-shaped, where each item is its own small thing.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****What the failures look like.** Availability-shaped, where one cause hits many people at once, or request-shaped, where each item is its own small thing.** and ****Whether the reporter pays.** A volunteer on a public tracker and a customer under contract are different relationships, and closing on silence costs differently in each.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
