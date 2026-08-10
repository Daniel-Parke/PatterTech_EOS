---
summary: Customer support as an operating function, triage before backlog, honest incident communication, and the loop from inbox back into the product
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_customer_inbound, has_paying_customers, has_customer_visible_incident, runs_public_tracker, reports_support_metric, single_responder]
activation_paths: [**/support/**, **/tickets/**, **/status/**, **/incidents/**, **/*complaint*, **/*feedback*]
volatility: slow
review: on-change-of:ISO-10002-revision
sources: [EV-0020, EV-0041, EV-0055, EV-0095, EV-0096, EV-0122, EV-0200, EV-0210, EV-0211, EV-0233, EV-0421, EV-0422, EV-0423, EV-0424, EV-0425, EV-0426, EV-0427, EV-0428, EV-0429, EV-0430, EV-0431, EV-0432]
type: playbook
tags: [eos, ops, product, pii]
---

# support-operations

This pack covers customer support as an operating function: what
arrives, how it is classified, how a customer-visible incident is run
and told, and how a week of inbox becomes backlog items. It activates
on any task touching a support inbox, ticket queue, status page,
complaints route or feedback synthesis. Honest incident communication
and personal-data handling bind. Classification and the severity ladder
are defaults; the ticket system and the survey instrument are taste.

The through-line: the queue is not the product, and the only reason to
run it well is that it is the cheapest evidence about the product you
will ever be handed.

## Activation

**Paths.** Support, helpdesk, inbox, tickets, feedback, complaints,
status, statuspage, oncall, incidents and postmortems directories;
issue and pull-request templates; triage label configuration and stale
or auto-close bot configuration; canned-reply and macro stores; survey
and review export files; contact and help routes in an application.

**Task types.** Triaging inbound; declaring, running or standing down a
customer-visible incident; writing a status update or an all-clear;
setting or changing a severity ladder; designing a complaints route;
choosing or changing a support metric; turning feedback into backlog
items; handing support from a founder to anyone else; setting an
auto-close or stale policy.

**Keywords, fallback only.** Ticket, inbox, triage, severity, SEV,
incident, status page, outage, escalation, complaint, refund, churn,
deflection, satisfaction, backlog grooming, canned reply.

**Applicability predicates.** Every requirement below names the
predicate that turns it on.

| Predicate | True when |
| --- | --- |
| has_customer_inbound | any route exists by which a person outside the venture reports something |
| has_paying_customers | at least one person or organisation pays for the product |
| has_customer_visible_incident | a failure that people outside the venture can see is open or has been open |
| runs_public_tracker | inbound lands in a tracker the public can read and write |
| reports_support_metric | a support number is published, reported to anyone, or used in a decision |
| single_responder | one person absorbs the whole queue |
| exports_ticket_text | ticket content leaves the system of record for any purpose |

An internal tool with no external reporting route trips none of these
and loads nothing beyond the first paragraph. Activation gives advice
and never permission: nothing here lowers a tier floor in
`kernel/POLICY_SPEC.md` or converts a manual-only class into an
autonomous one under `kernel/GUARD_SPEC.md`.

## Outcomes and non-goals

**Outcomes.** Every inbound item has a classification a stranger could
defend, and nothing sits in an unnamed state. A customer-visible
failure is declared on a written trigger rather than on a feeling, and
the people affected are told something true while it is still true.
Duplicate reports of one cause converge on one record and get one
answer. A week of inbox produces backlog items with a stated
denominator, so the product hears the queue rather than the loudest
sender. The point at which one person can no longer absorb the queue is
known before customers discover it.

**Non-goals.** This pack does not choose a helpdesk, a status page
vendor or a survey instrument. It carries no reply templates, no tone
guide and no service-level commitments: those are venture contracts,
not estate doctrine. It does not own the postmortem, which stays with
`packs/devops-reliability/`, nor account management, sales or refund
authority. It sets no response-time target, because no source in this
pack supports a number and inventing one would be the exact failure the
pack warns about.

## Binding requirements

Two requirements bind. One rests on law, one on a protected-set floor
this pack restates for customer messages. The rest of this pack is
defaults and preferences, which is the honest shape for a domain where
most published practice is convention that nobody has measured.

The 2026-08 authority audit under ADR-0008 put one test to all seven
requirements this pack used to bind: a rule binds only where it prevents
a concrete failure that is serious or hard to reverse **and** its basis
is law, a standard, empirical evidence or a protected-set floor. Five
failed it and are now defaults, keeping their B numbers because
`packs/support-operations/CHECKS.md`, the guides and the exemplar cite
them. A default is departed from in writing, never in silence.

**Evidence note.** The twelve sources researched for this pack were
imported into `registry/evidence.json` as EV-0421 to EV-0432, and every
citation here uses the ledger id. Each row carries its version, licence,
access date, maintenance state and review trigger. The frozen batch the
import was made from stays at
`packs/support-operations/research/sources.fragment.json`. Several
sources are paywalled and paraphrased only, so nothing here quotes them.

**B4. A customer-facing message never reports a bypassed check as
passing.** `has_customer_visible_incident`. If a gate was skipped,
waived or run under an emergency route to get the fix out, the incident
record and any all-clear say so in those words. A status update states
what has been verified and by what, and "not yet verified" and "cause
unknown" are legal things to publish. No update asserts a cause the
incident record does not support. Basis: decision, and it binds as a
protected-set floor rather than on the support literature:
`kernel/GUARD_SPEC.md` records a bypassed gate as bypassed and lets no
emergency overlay lower it, and this is that rule pointed at the people
outside the venture. Prevents the two failures that cost the most trust:
an all-clear resting on verification nobody performed, and a second
outage from an unverified fix that the record made look verified. A
published all-clear cannot be unpublished, which is the hard-to-reverse
half.

**B6. A support inbox is a personal-data store and is run as one.**
`has_customer_inbound`, `exports_ticket_text`. Retention, access and
lawful basis follow `packs/security-privacy/`, and the ICO guidance the
estate already cites (EV-0041). No export of ticket text into a
synthesis, analytics or model tool without the recorded basis. Derived
artefacts such as triage files, theme reports and public postmortems
carry ids or hashes, never names, addresses or account numbers. Basis:
law, and data protection is a protected-set item under `GOVERNANCE.md`.
Prevents a support archive becoming an unrecorded personal-data store,
and prevents a convenience export becoming an unlawful transfer. An
export into a synthesis or model tool cannot be recalled, which is the
hard-to-reverse half.

**What deliberately does not bind.** Acknowledging a complaint on
receipt and closing it only once the complainant has been told the
outcome is the core of the complaints standard
(EV-0425). It sits below as the D3 default rather
than as a binding rule, because that standard is guidance written for
organisations large enough to run a quality management system, and the
research graded it accordingly. It is the default this pack expects the
fewest ventures to depart from.

## Defaults

Followed unless the task records a reason to depart.

### Demoted from binding, 2026-08

Five rules that used to bind. Each still names the failure it prevents,
and each says which leg of the ADR-0008 test it failed. Numbers are
unchanged so the checks, guides and exemplar that cite them still
resolve.

**B1. Nothing enters a backlog without a classification, and untriaged
is a state rather than an absence.** `has_customer_inbound`. Every
inbound item carries four independent values before it is ranked:
kind, priority, owning queue, and a triage state that is either
accepted or needs-info (EV-0424). Classification
comes before prioritisation, not after
(EV-0426). Where one cause explains several reports,
they carry one shared incident or defect id and get one answer
(EV-0425). A needs-info item carries the date its
next action is due. Basis: standard. Prevents three failures: work that
is invisible because nobody can query for it, a priority argued from
whoever wrote most recently, and five people receiving five different
accounts of one bug. Failed the seriousness leg: a misfiled item is
refiled, and the queue is recoverable at any point.

**B2. The severity ladder is written before the incident, and one band
changes what the organisation does.** `has_customer_visible_incident`.
The ladder is ordered, each band has a written impact criterion, it
states that the higher band is taken when the call is unclear, and at
least one threshold switches the response mode rather than only the
wording (EV-0421). The band is not litigated during
the incident; the argument goes in the postmortem. Basis: decision,
taken on exemplar practice with no outcome data behind it. Prevents
severity being assigned afterwards to justify the response that already
happened. Failed the basis leg, which the pack already said out loud.

**B3. A customer-visible incident records a communication owner
separately from the person changing the system.**
`has_customer_visible_incident`. Both fields are filled even when the
two values are the same name, because the record has to show the
decision was taken (EV-0423,
EV-0422). Basis: decision. Prevents the fixer's
attention being spent on updates, and prevents an incident closing with
nobody accountable for having told anyone. Failed the basis leg.
Nothing else in this pack catches an incident that closed with nobody
accountable for telling anyone, so this is the default a venture should
think hardest before departing from.

**B5. No target and no published figure is the mean of a duration
distribution.** `reports_support_metric`. Incident and response
durations are reported as percentiles, as raw counts, or not at all
(EV-0211). Per-band time targets are not set, because the corpus that
looked found no correlation between duration and severity. Basis:
empirical-evidence. Prevents a target that describes no incident that
ever happened, and prevents a skewed distribution being summarised by
the one statistic it defeats. Failed the seriousness leg: a bad metric
is replaced by a better one at no cost, and the number itself harms
nobody.

**B7. A loyalty or satisfaction score is a trend about one population,
never a cross-firm benchmark.** `reports_support_metric`. The score is
reported with its population, its n and its date range, and it is never
used to claim a position relative to another company or an industry
figure (EV-0428). Basis: empirical-evidence.
Prevents an instrument being sold internally as evidence it has been
tested for and failed to provide. Scope note: the replication that
settles this covered 21 firms and more than 15,500 interviews from one
national panel, in industries and an era that predate subscription
software. It refutes a superiority claim; it does not show the score is
useless, and it says nothing about behaviour at the sample sizes a
venture with sixty customers actually has. Failed the seriousness leg
by the same reasoning as B5. Publishing the comparison outside the
venture is a marketing claim and belongs to `packs/marketing-growth/`.

### Standing defaults

- **D1. Two queues, incident and request, with separate targets and no
  item in both.** Restoring an interrupted service and fulfilling a
  routine ask have different clocks, so one target describes neither
  (EV-0426). The queue axis in B1 carries the split.
- **D2. Three severity bands while one person responds, five once there
  is a rota.** A rung that changes nothing is theatre, and five levels
  in a venture with one responder is five ways to write the same
  sentence (EV-0421).
- **D3. Acknowledge on receipt, close on answer, and never on silence,
  for anyone who pays.** The route to complain is visible and free to
  use, and the loop closes when the complainant has been told the
  outcome (EV-0425).
- **D4. Auto-close and stale timers on public trackers only.**
  Unreproducible reports close on a timer where the reporter is a
  volunteer and closing costs nothing contractual
  (EV-0424). Recorded counter-evidence: maintainers
  of the project that runs that bot have filed complaints that it
  closes real bugs.
- **D5. One priority band reserved for plausible but unevidenced.**
  Keeps opinion out of the roadmap without throwing it away
  (EV-0424).
- **D6. Declaration runs on written objective triggers.** A second
  person is needed, the failure is visible to customers, or an hour of
  focused work has not closed it (EV-0423). Scope
  note: that hour is calibrated to a very large service estate and is
  not evidence for any threshold here; it is a starting number to argue
  with.
- **D7. A weekly synthesis pass with the coding stance declared before
  coding.** What the data set is, whether coding is inductive or driven
  by an existing frame, whether it reads the surface or the meaning
  underneath, and what counts as a theme, all written down first.
  Prevalence is reported against a stated denominator, because a count
  of tickets mentioning a thing means nothing without the population it
  came from (EV-0431). Themes are constructed by the
  analyst, so "a theme emerged" is not an available sentence.
- **D8. Single-responder utilisation held below seventy per cent.**
  Waiting time in a single-server queue rises as utilisation over one
  minus utilisation, so the wait is roughly two and a third service
  times at seventy per cent, five and two thirds at eighty-five, and
  nineteen at ninety-five (EV-0430). The levers that
  work are reducing arrival variability and holding deliberate slack.
  Scope note: that is a heavy-traffic approximation for one server,
  first come first served, with no priority classes and nobody giving
  up, so a severity-prioritised desk differs in detail while keeping
  the same shape of collapse.
- **D9. A postmortem due date is recorded at the moment of resolution**
  for any customer-visible incident, no more than five days after
  resolution, with a named owner. The clock and the ownership come from
  the exemplar (EV-0200); the number five is the estate's, and it is a
  default rather than a finding.
- **D10. Self-service counts as deflection only when it resolves.**
  Measure resolution and onward contacts, not page views, because a
  self-service layer that does not answer converts into an assisted
  contact with the customer's effort already spent
  (EV-0429).
- **D11. Founder-delivered support is the opening posture and carries a
  written exit signal** recorded on the day it starts
  (EV-0432).

## Preferences

Taste. Depart freely, no reason needed.

- The helpdesk, the status page tool and the survey instrument.
- The label vocabulary, so long as the four axes in B1 stay separable.
- One inbox rather than one per channel while volume is low.
- A public changelog as the standing answer to "did you ever fix it"
  (EV-0055, EV-0095).
- Writing the customer-facing message inside the incident record rather
  than in a separate document.
- Machine-readable error identifiers in product errors so a ticket can
  be matched to a cause without a screenshot (EV-0122).
- Templates for the three commonest replies, rewritten by hand whenever
  the template does not fit.

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| How does inbound get classified, and what keeps the queue finite | Triage pattern, cost per item, what the queue teaches | `packs/support-operations/guides/GD-SUPPORT-001-triage-pattern.md` |
| May an item close without an answer | Auto-close policy per channel, contractual exposure | `packs/support-operations/guides/GD-SUPPORT-002-close-policy.md` |
| Who declares a customer-visible incident, on what signal | False-alarm cost against late-notice cost | `packs/support-operations/guides/GD-SUPPORT-003-declaration-route.md` |
| What do we measure, and what may the number be used for | Which metric, which population, which decision | `packs/support-operations/guides/GD-SUPPORT-004-support-measurement.md` |

Level-three detail sits in `packs/support-operations/refs/`: the triage
record shape, the severity ladder and declaration form, the incident
communication contract, and the synthesis pass. A full worked week is
in
`packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`.

## Failure modes and anti-patterns

- **Severity assigned after the fact.** The band is chosen to match the
  response that already happened, which turns the ladder into a
  narrative device.
- **The fixer writing the updates.** Two jobs, one person, and the
  first thing dropped is the one nobody is chasing.
- **The reassuring all-clear.** An incident closed with "all systems
  operational" while the fix went out under a skipped gate. This is the
  failure B4 exists to stop, and it is the one that gets repeated
  because it feels kind at the time.
- **Auto-close applied to a paying customer.** Silence read as
  resolution, which is exactly the fairness failure the complaints
  standard exists to prevent.
- **One priority axis doing the work of four.** Kind, urgency, owner
  and triage state collapsed into a single P-number, after which no
  query answers anything.
- **A theme with no denominator.** Eleven tickets mentioned a thing.
  Out of how many, from whom, over what period.
- **Prevalence in the inbox read as prevalence in the user base.**
  Support data is self-selected: only people who complained are in it.
- **Mean time to anything.** A skewed distribution summarised by the
  statistic it defeats (EV-0211), and the same failure the estate
  already refuses for developer productivity (EV-0210).
- **The loyalty score as a scoreboard.** A number compared against an
  industry figure, or against a competitor, or across two instruments.
- **Founder support as a permanent cost saving.** The posture is
  designed to fail at scale, and it is measured by what it teaches, not
  by hours absorbed.
- **Discovering the ceiling from angry customers** rather than from a
  utilisation figure that has been climbing for a month.
- **Ticket text pasted into whatever tool is convenient.** A personal
  data transfer with no basis, done in the name of a weekly summary.

## Open questions and counter-evidence

- **Deflection has no evidence base.** No primary source was found by
  the 2026-08-03 cutoff measuring whether self-service deflection
  improves any customer outcome. There is a mechanism for how it
  backfires (EV-0429); the positive case is vendor
  material. D10 is written to be falsifiable rather than to assert a
  benefit.
- **Small-sample loyalty scores are unaddressed.** The original claim
  and the replication both argue at industry scale
  (EV-0427, EV-0428). Neither
  states the n at which a score is stable, which is the only question a
  venture with sixty customers has.
- **Support volume as a churn leading indicator** is plausible, widely
  asserted, and unsupported by any primary source located here. The
  pack records no rule about it.
- **When founder support should end is our inference.** The essay
  arguing for it gives no exit signal
  (EV-0432); the queueing result gives a capacity
  ceiling rather than a learning one
  (EV-0430). "When you stop learning something new
  from each contact" is reasoning, not evidence.
- **Delight against effort is unresolved.** One study finds exceeding
  expectations did not separate loyal from disloyal customers while
  high effort strongly did (EV-0429); the founder
  argument says take extraordinary unscalable measures for small
  numbers (EV-0432). Only a scale hypothesis
  reconciles them, and a hypothesis is not a resolution. Scope note on
  the first: roughly 97,000 customers of contact centres, self-reported
  loyalty intent rather than observed retention, run by a firm selling
  the resulting metric.
- **Manual against automatic declaration has no outcome data on either
  side.** One exemplar wants a human page to a named person
  (EV-0422); common practice auto-declares on a burn
  alert (EV-0020, EV-0096). GD-SUPPORT-003 forces the choice and
  records it rather than pretending the evidence settles it.
- **The two standards conflict on closing.** Timed closure of
  unreproducible reports (EV-0424) against a loop
  that closes only on answer (EV-0425). Both are
  defensible for different relationships, so GD-SUPPORT-002 forces the
  choice per channel instead of letting a tool default decide.
- **B2 and B3 used to bind above their evidence grade.** Both come from
  exemplar practice with no comparative measurement, and the 2026-08
  audit made them defaults for that reason. The arguments behind them
  stand: a ladder written during an incident is not a ladder, and an
  unnamed communication owner is indistinguishable in the record from
  nobody. Departing from either now leaves a written reason.
- **Error-recovery and help heuristics** (EV-0233) give reviewers
  shared vocabulary for support-visible interface defects and are not a
  conformance claim; there is no evidence that following them improves
  outcomes.
