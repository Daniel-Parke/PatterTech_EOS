---
summary: Activation, outcomes and decision map for the support-operations Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [has_customer_inbound, has_paying_customers, has_customer_visible_incident, runs_public_tracker, reports_support_metric, single_responder]
activation_paths: [**/support/**, **/tickets/**, **/status/**, **/incidents/**, **/*complaint*, **/*feedback*]
volatility: slow
review: none
sources: [EV-0020, EV-0041, EV-0055, EV-0095, EV-0096, EV-0122, EV-0200, EV-0210, EV-0211, EV-0233, EV-0421, EV-0422, EV-0423, EV-0424, EV-0425, EV-0426, EV-0427, EV-0428, EV-0429, EV-0430, EV-0431, EV-0432]
type: playbook
tags: [eos, ops, product, pii]
depends_on: [product-discovery, devops-reliability]
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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B4"></a>
- `B4` to [DOC-SUPPORT-001](doctrines/DOC-SUPPORT-001-a-customer-facing-message-never-reports-a-bypassed-check-as-pass.md) (default)
<a id="B6"></a>
- `B6` to [DOC-SUPPORT-002](doctrines/DOC-SUPPORT-002-a-support-inbox-is-a-personal-data-store-and-is-run-as-one.md) (binding)
<a id="B1"></a>
- `B1` to [DOC-SUPPORT-003](doctrines/DOC-SUPPORT-003-nothing-enters-a-backlog-without-a-classification-and-untriaged.md) (default)
<a id="B2"></a>
- `B2` to [DOC-SUPPORT-004](doctrines/DOC-SUPPORT-004-the-severity-ladder-is-written-before-the-incident-and-one-band.md) (default)
<a id="B3"></a>
- `B3` to [DOC-SUPPORT-005](doctrines/DOC-SUPPORT-005-a-customer-visible-incident-records-a-communication-owner-separa.md) (default)
<a id="B5"></a>
- `B5` to [DOC-SUPPORT-006](doctrines/DOC-SUPPORT-006-no-target-and-no-published-figure-is-the-mean-of-a-duration-dist.md) (default)
<a id="B7"></a>
- `B7` to [DOC-SUPPORT-007](doctrines/DOC-SUPPORT-007-a-loyalty-or-satisfaction-score-is-a-trend-about-one-population.md) (default)
- source `defaults:006` to [DOC-SUPPORT-008](doctrines/DOC-SUPPORT-008-two-queues-incident-and-request-with-separate-targets-and-no-ite.md) (default)
- source `defaults:007` to [DOC-SUPPORT-009](doctrines/DOC-SUPPORT-009-three-severity-bands-while-one-person-responds-five-once-there-i.md) (default)
- source `defaults:008` to [DOC-SUPPORT-010](doctrines/DOC-SUPPORT-010-acknowledge-on-receipt-close-on-answer-and-never-on-silence-for.md) (default)
- source `defaults:009` to [DOC-SUPPORT-011](doctrines/DOC-SUPPORT-011-auto-close-and-stale-timers-on-public-trackers-only.md) (default)
- source `defaults:010` to [DOC-SUPPORT-012](doctrines/DOC-SUPPORT-012-one-priority-band-reserved-for-plausible-but-unevidenced.md) (default)
- source `defaults:011` to [DOC-SUPPORT-013](doctrines/DOC-SUPPORT-013-declaration-runs-on-written-objective-triggers.md) (default)
- source `defaults:012` to [DOC-SUPPORT-014](doctrines/DOC-SUPPORT-014-a-weekly-synthesis-pass-with-the-coding-stance-declared-before-c.md) (default)
- source `defaults:013` to [DOC-SUPPORT-015](doctrines/DOC-SUPPORT-015-single-responder-utilisation-held-below-seventy-per-cent.md) (default)
- source `defaults:014` to [DOC-SUPPORT-016](doctrines/DOC-SUPPORT-016-a-postmortem-due-date-is-recorded-at-the-moment-of-resolution.md) (default)
- source `defaults:015` to [DOC-SUPPORT-017](doctrines/DOC-SUPPORT-017-self-service-counts-as-deflection-only-when-it-resolves.md) (default)
- source `defaults:016` to [DOC-SUPPORT-018](doctrines/DOC-SUPPORT-018-founder-delivered-support-is-the-opening-posture-and-carries-a-w.md) (default)
- source `preferences:001` to [DOC-SUPPORT-019](doctrines/DOC-SUPPORT-019-the-helpdesk-the-status-page-tool-and-the-survey-instrument.md) (preference)
- source `preferences:002` to [DOC-SUPPORT-020](doctrines/DOC-SUPPORT-020-the-label-vocabulary-so-long-as-the-four-axes-in-b1-stay-separab.md) (preference)
- source `preferences:003` to [DOC-SUPPORT-021](doctrines/DOC-SUPPORT-021-one-inbox-rather-than-one-per-channel-while-volume-is-low.md) (preference)
- source `preferences:004` to [DOC-SUPPORT-022](doctrines/DOC-SUPPORT-022-a-public-changelog-as-the-standing-answer-to-did-you-ever-fix-it.md) (preference)
- source `preferences:005` to [DOC-SUPPORT-023](doctrines/DOC-SUPPORT-023-writing-the-customer-facing-message-inside-the-incident-record-r.md) (preference)
- source `preferences:006` to [DOC-SUPPORT-024](doctrines/DOC-SUPPORT-024-machine-readable-error-identifiers-in-product-errors-so-a-ticket.md) (preference)
- source `preferences:007` to [DOC-SUPPORT-025](doctrines/DOC-SUPPORT-025-templates-for-the-three-commonest-replies-rewritten-by-hand-when.md) (preference)

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
