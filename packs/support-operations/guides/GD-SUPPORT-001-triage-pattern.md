---
summary: How does inbound get classified, and what keeps the queue finite?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0055, EV-0200]
review: on-change-of:ISO-10002-revision
type: guide
tags: [ops, product]
review_by: 2028-07
---

# GD-SUPPORT-001: How does inbound get classified, and what keeps the queue finite?

## The question

Four patterns for handling inbound exist in the wild, and they are not
points on one scale. They differ in what the queue is for: restoring a
service, keeping a backlog honest, discharging an obligation, or
learning what the product feels like to use. Pick the wrong one and
either the cost per item is absurd or the queue grows without bound.

## It depends on

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

## Options

### A. Severity-first operational triage
Inbound is classified by blast radius first: an ordered ladder, a rule
that takes the higher band when the call is unclear, and one threshold
that mechanically switches the organisation into a different mode.
Communication is a named role held by someone who is not fixing, and
declaration runs on objective triggers rather than judgement
(FRAG-SUPPORT-OPERATIONS-01, FRAG-SUPPORT-OPERATIONS-03,
FRAG-SUPPORT-OPERATIONS-02, EV-0200). Buys a fast, defensible response
when one cause hits many customers, and a record that survives the
postmortem. Costs a written ladder maintained ahead of time, and it
does nothing for a billing question.

### B. Labelled backlog triage
Inbound is labelled on orthogonal axes, kind, priority, owner, plus a
separate accepted flag so untriaged is queryable. Support questions are
routed out of the defect tracker by label rather than answered inside
it, and items lacking reproduction close on a timer
(FRAG-SUPPORT-OPERATIONS-04). Buys a finite queue and a backlog whose
priorities can be argued with. Costs real bugs to the timer, which the
maintainers of the project that runs the best-known stale bot have
themselves complained about.

### C. Complaint as a closed loop
Every complaint is acknowledged, owned, resolved and answered, and the
loop closes only when the complainant has been told the outcome. The
route to complain is visible and free. Complaint data is analysed in
aggregate and fed back into the product, so recording without a
periodic synthesis pass is a failure of the process rather than a
missed nicety (FRAG-SUPPORT-OPERATIONS-05,
FRAG-SUPPORT-OPERATIONS-06). Buys the most defensible position under a
contractual or regulatory relationship, and consistent answers to the
same defect. Costs the most per item, and the management-system
apparatus is disproportionate below a handful of staff.

### D. Founder as the support function
Support is deliberately unscalable and deliberately temporary. The
founder answers everything, operates the product manually on the
customer's behalf where that helps, and treats each contact as product
research (FRAG-SUPPORT-OPERATIONS-12, EV-0055). Buys the fastest
product learning available at small numbers, and word of mouth as a
side effect. Costs a ceiling that arrives non-linearly
(FRAG-SUPPORT-OPERATIONS-10), and it has no exit signal of its own, so
one has to be written.

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

## Default

D plus A for a pre-revenue venture. D plus A plus C from the first
paying customer. Add B when a public tracker opens or when the defect
backlog outgrows one person's memory. Move off D when the exit signal
fires, which in practice is whichever comes first of the utilisation
figure in PACK.md D8 crossing seventy per cent for two consecutive
weeks, or a month in which no contact taught anything new.

## Worked rulings

- **support-operations exemplar (2026-08, argued)**: a 60-customer paid
  product ran D plus A plus C. Forty inbound items split into an
  incident queue and a request queue, one outage declared under A with
  four duplicate reports collapsed onto one incident id, two billing
  complaints run under C with acknowledgement recorded and no timer,
  and three unreproducible reports left in needs-info with a due date
  rather than closed. See
  `packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`.
- **The conflict is real and is not resolved here (external,
  inherited)**: B closes unreproducible reports on silence and C
  forbids closing before the complainant has been answered. The choice
  is made per channel in
  `packs/support-operations/guides/GD-SUPPORT-002-close-policy.md`, not
  by whichever tool default is switched on.
