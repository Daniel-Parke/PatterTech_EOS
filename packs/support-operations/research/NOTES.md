---
summary: Research synthesis for the support-operations pack, covering triage and severity models, response measurement, self-service trade-offs, feedback synthesis and founder-scale realities
type: example
tags: [eos, testing]
---

# Support operations research notes

Cutoff 2026-08-03. Twelve new sources in `sources.fragment.json`.
Existing ledger rows reused rather than re-recorded: EV-0200 (postmortem
ownership and clock), EV-0211 (incident duration is skewed, so a mean is
arithmetic the data does not support), EV-0096 (error budget dial),
EV-0020 (OpenSLO), EV-0055 (GitLab Handbook), EV-0095 (edit-on-encounter
docs), EV-0041 (ICO on personal data, which support inboxes are full
of), EV-0122 (RFC 9457 error types), EV-0233 (NN/g heuristics on error
recovery and help), EV-0210 (SPACE, no single number captures a system).

## The four patterns

### Pattern A: severity-first operational triage

Sources: FRAG-01, FRAG-02, FRAG-03, FRAG-06, EV-0200.

Inbound is classified by blast radius first. A written ladder, a
tie-break rule that says take the higher level when unsure, and one
threshold that mechanically flips the organisation into a different
mode. Communication is a named role held by someone who is not fixing.
Declaration triggers are objective, not felt: a second team is needed,
it is customer-visible, or an hour of focused work has not closed it.
Fits when failures are availability-shaped, when several customers are
hit by one cause, and when a late notice costs more than a false alarm.

Trade-offs: the ladder only pays if the rungs change behaviour. Five
levels in a venture with one responder is theatre. The three-factor
business score in FRAG-02 (visibility, actual impact now, duration and
confidence) is the part that transfers to any size.

Anti-patterns: severity assigned after the fact to justify the response
that already happened; the person fixing also writing the status
updates; auto-declaring a business incident from a monitoring
threshold, which FRAG-02 argues against and which nobody has measured.

### Pattern B: labelled backlog triage

Sources: FRAG-04, FRAG-06.

Inbound is labelled on orthogonal axes, kind, priority, owner, and a
separate accepted flag so untriaged is a queryable state rather than an
absence. Support questions are routed out of the defect tracker by
label instead of being answered inside it. Items lacking reproduction
close on a timer. A priority band is reserved for
plausible-but-unevidenced, which keeps opinion out of the roadmap
without discarding it. Fits when most inbound is requests and bug
reports rather than outages, when the reporter is not under contract,
and when the queue would otherwise grow without bound.

Trade-offs: the timer is what makes the queue finite and is also what
loses real bugs. Kubernetes maintainers have filed complaints about
their own stale bot closing important issues, honest evidence against
the mechanism from inside the project that runs it.

Anti-patterns: one priority axis doing the work of four; closing on
silence when the silent party is a paying customer, which collides with
Pattern C; using label counts as a health metric without a denominator.

### Pattern C: complaint as a closed loop

Sources: FRAG-05, FRAG-06.

Every complaint is acknowledged, owned, resolved and answered, and the
loop closes only when the complainant has been told the outcome. The
route to complain is visible and free. Complaint data is analysed in
aggregate and fed back into the product, so recording without a
periodic synthesis pass is a failure of the process rather than a
missed nicety. Incidents and service requests are separate queues with
separate targets, restore versus fulfil. Fits when there is a
contractual or regulatory relationship, when customers pay, and when
the same defect will otherwise be reported by many people who each get
a different answer.

Trade-offs: the most expensive pattern per item and the most
defensible. The management-system apparatus is disproportionate below a
handful of staff; the two-queue split and classify-before-prioritise
are the parts worth taking.

Anti-patterns: an inbox with no acknowledgement step; a resolution rule
invented per complaint, the fairness failure the standard exists to
prevent.

### Pattern D: founder as the support function

Sources: FRAG-12, FRAG-10, EV-0055.

Support is deliberately unscalable and deliberately temporary. The
founder answers everything, operates the product manually on the
customer's behalf, and treats each contact as product research. The
posture is designed to fail at scale, and the transition has to be
planned because the essay arguing for it gives no exit signal. Fits
below roughly the point where the founder stops learning something
new from each contact. Kingman gives the ceiling from the other side: a
single-server queue at eighty-five per cent utilisation waits about
five and two thirds service times, at ninety-five per cent about
nineteen. Response time collapses non-linearly before any visible
capacity problem, and the levers that work are reducing arrival
variability and holding deliberate slack, not working faster.

Anti-patterns: treating founder support as a permanent cost saving;
measuring it by hours worked; discovering the ceiling from angry
customers rather than a utilisation number.

## Where the sources disagree

1. **The load-bearing one: single-number loyalty measurement.**
   FRAG-07 claims a single recommendation question predicts growth
   better than longer instruments. FRAG-08 attempted the replication on
   the very industries named as exemplars, using 21 firms and over
   15,500 interviews from an independent national panel, and found
   explanatory power statistically indistinguishable from a
   conventional satisfaction index. The superiority claim does not
   survive; the operational virtue does, a number the front line can
   act on this week. Consequence: any loyalty score is a trend line
   about one population over time, never a cross-firm benchmark, never
   evidence that one instrument sees what another cannot. EV-0210 says
   the same in another domain.

2. **Delight versus effort versus founder attention.** FRAG-09 finds
   exceeding expectations did not separate loyal from disloyal
   customers while high effort strongly did. FRAG-12 argues founders
   should take extraordinary unscalable measures to delight small
   numbers of users. Not reconciled by evidence, only by a scale
   hypothesis: the founder's mechanism is learning and word of mouth at
   fifty users, the effort finding comes from mature contact centres.
   That is a hypothesis, not a resolution.

3. **Close on silence versus close on answer.** FRAG-04 closes
   unreproducible items after twenty days of silence and stales at
   ninety. FRAG-05 requires the complainant to be answered before the
   loop closes. Both defensible for different relationships, so the
   pack forces the choice per channel rather than letting tooling
   defaults decide.

4. **Manual versus automatic declaration.** FRAG-02 wants
   customer-facing declaration to be a human page to a named person.
   Common practice auto-declares on an SLO burn alert (EV-0020,
   EV-0096). Neither has outcome data.

5. **Duration metrics.** Severity ladders invite per-band mean time
   targets. EV-0211 shows incident duration is positively skewed and
   found no correlation between duration and severity in the VOID
   corpus, so a mean is the wrong statistic.

## Binding, default, preference

Binding, each mechanically checkable:

- Every inbound item carries a classification before it enters any
  backlog, and untriaged is a queryable state, not an absence.
- The severity ladder is written before the incident, includes the
  take-the-higher tie-break, and names at least one threshold that
  changes behaviour rather than only wording.
- Any customer-visible incident records a communication owner
  separately from the person changing the system, even when both names
  are the same person, because the record proves the decision was made.
- No target and no reported figure is a mean of a duration
  distribution (EV-0211). Percentiles, counts, or nothing.
- Support inboxes are personal data. Retention and access follow
  EV-0041; no export of ticket text into a synthesis tool without it.
- A loyalty score is never reported as a cross-firm benchmark
  (FRAG-08).

Default, overridable with a recorded reason: three severity bands for a
venture and five once there is a rota; incidents and service requests
as separate queues with separate targets (FRAG-06); a weekly synthesis
pass with the coding stance declared before coding and prevalence
against a stated denominator (FRAG-11); auto-close timers on public
trackers only, never on a paying customer's complaint; single-responder
utilisation held below seventy per cent (FRAG-10). Preference: the
survey instrument, the status page tool, the ticket system, the label
vocabulary.

## Open questions, where evidence is genuinely thin

- **Deflection rate.** No primary source found measuring whether
  self-service deflection improves any customer outcome. FRAG-09 gives
  the mechanism by which it backfires, an unresolving self-service layer
  adds a hop rather than removing one, but the positive case is vendor
  material only. Unevidenced.
- **Small-sample loyalty scores.** FRAG-07 and FRAG-08 both argue at
  industry scale. Neither says at what n a score is stable, which is
  exactly the question a venture with fifty customers has.
- **Support volume as a churn leading indicator.** Plausible, often
  asserted, no primary source located by the cutoff.
- **When founder support should end.** FRAG-12 gives no exit signal and
  FRAG-10 gives a capacity ceiling, not a learning one. The
  stop-learning criterion in Pattern D is our inference, not evidence.

Refresh triggers: an independent replication of either loyalty claim; a
revision of ISO 10002 or ISO/IEC 20000-1; any change to the PagerDuty
or Kubernetes triage documents named in the fragment.
