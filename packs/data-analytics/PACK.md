---
summary: Analytics data, event taxonomy, model shape, quality gates, experiment statistics and what the analytics layer may hold about a person
type: playbook
tags: [eos, data, testing, pii]
kind: rule
authority: binding
lifecycle: active
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_analytics_table, defines_events, runs_experiment, reads_for_decision, handles_analytics_identifier]
activation_paths: [**/analytics/**, **/dbt/**, **/models/marts/**, **/events/**, **/*event*.json, **/*experiment*, **/dashboards/**, **/*metric*.sql, **/*.sql]
volatility: slow
review: 2027-11
sources: [EV-0041, EV-0056, EV-0057, EV-0059, EV-0138, EV-0139, EV-0225, EV-0240, EV-0305, EV-0306, EV-0307, EV-0308, EV-0309, EV-0310, EV-0311, EV-0312, EV-0313, EV-0315, EV-0316, EV-0317, EV-0318, EV-0319, EV-0320, EV-0321]
---

# Data and analytics pack

This pack covers analytics data: how product events are named and
validated, how analytics models are shaped and gated, how an experiment
is allowed to end, and what the analytics layer may hold about a person.
It activates on any task that publishes an analytics table, defines a
tracked event, runs an experiment, or turns product data into a claim
someone will act on.

## Activation

Load this pack when any of the following is true.

**Paths touched.** Transformation projects and their model trees
(`models/`, `dbt_project.yml`, `transform/`); event tracking and
tracking-plan files; warehouse or lakehouse table definitions;
experiment or feature-flag configuration; analytics notebooks and query
files; dashboard definitions; any `raw/`, `staging/`, `marts/` or
`warehouse/` directory.

**Task types.** Model or remodel data for analysis. Add, rename or
retire a tracked event. Design, run or read an experiment. Write a query
whose answer is going to a decision. Build or change a dashboard. Move
analytics data between stores. Decide what an analytics table may hold
about a person.

**Keywords, fallback only.** Event, tracking plan, funnel, cohort,
warehouse, lakehouse, model, grain, fact, dimension, A/B test,
experiment, variant, uplift, significance, p-value, dashboard, metric,
data quality, freshness. Keywords are the weakest signal and never
override the predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| publishes_analytics_table | a table, view or model is read by anything outside the session that wrote it |
| defines_events | the task adds, renames, retires or reshapes a tracked product event |
| runs_experiment | units are assigned to variants and a metric is read from that assignment |
| reads_for_decision | product data is turned into a claim someone will act on |
| handles_analytics_identifier | the analytics layer will hold a column that can identify a living person |

A one-off query a person reads and throws away trips no predicate and
loads nothing beyond this pack's first paragraph. Activation gives
advice, never permission: no requirement here lowers a tier floor set by
`kernel/POLICY_SPEC.md` or converts a manual-only action class into an
autonomous one under `kernel/GUARD_SPEC.md`.

## Outcomes and non-goals

**Outcomes.** A number that leaves the room can be traced to a table
with a named owner and a rule that would have stopped it if it were
wrong. Two people asking the same business question by different routes
get the same answer. An experiment either produces a decision that
survives being checked, or it says plainly that it cannot. Nothing in
the analytics layer identifies a person unless someone recorded why it
may.

**Non-goals.** Migration mechanics and schema rollout sit in
`packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md`.
Transport, envelope and API contract shape sit in
`packs/api-integration/PACK.md`. Threat modelling, secret handling and
access control sit in `packs/security-privacy/PACK.md`. Dashboard visual
design sits in `packs/ui-ux/PACK.md`. This pack picks no vendor and no
tool.

**What this pack can and cannot prove.** Almost all product analytics is
observational. A funnel, a cohort chart and a week-on-week delta
describe what happened to people who selected themselves into doing
something. They do not identify a cause, and no amount of query care
converts them into one. Only a randomised experiment supports a causal
claim, and only when its assumptions held (B4, B5). Otherwise the honest
verb is "changed alongside", not "caused". This is the most common way
an analytics stack produces confident nonsense, and it is a discipline
of wording before it is one of statistics.

## Binding requirements

Three requirements bind. Each names the predicate that turns it on, the
evidence behind it, and the failure it prevents. Most rules in this
domain are defaults or preferences, and that is correct for a field this
young.

The authority audit under ADR-0008 moved three of the original six to
defaults, and the reason is the same in all three: each gave its basis
as a decision, and a rule the estate merely chose is a default. The
one-document ownership rule is now D9, the blocking quality gate is D10,
and the grain declaration is D11, which puts it back at the grade the
research gave it. The three that stayed keep their numbers, so the
citations in the guides, refs, checks and exemplar still resolve, which
is why the list below runs B3, B4, B5.

**B3. No column that can identify a living person lands in the analytics
layer without a recorded lawful basis and a named complaints path.**
`handles_analytics_identifier`. UK duties are statutory: a recorded
lawful basis and a statutory complaints route are duties, not good
practice (EV-0225), with the ceremony around them proportionate to the
risk to people (EV-0041). Prevents source columns being copied forward
because they were in the source, which is how an email address ends up
in a marts table nobody meant to hold one. Basis: law.

**B4. The randomisation unit, the primary metric and the stopping rule
are written down before traffic starts.** `runs_experiment`. Prevents
the failure that no later analysis can repair: choosing the metric and
the stopping point after seeing the data. The dominant experimentation
errors are interpretive rather than computational, and monitoring a
fixed-horizon test continuously can push the false positive rate far
above its nominal five per cent (EV-0313). Scope note: that finding
comes from platforms running hundreds of concurrent experiments for
millions of users. The mechanism transfers to one experiment; the base
rates do not. Basis: empirical-evidence.

**B5. Sample ratio mismatch is checked and reported before any
experiment result is read, and a failed check voids the result.**
`runs_experiment`. A gap between the assignment ratio you asked for and
the ratio you observed means something interfered, and whatever
interfered almost certainly also moved the metric, so the result is not
usable at any confidence level (EV-0316). Prevents the worst outcome in
this domain: computing the check, seeing it fail, and reporting the win
anyway. Basis: empirical-evidence.

Guarded actions sit outside this pack. Deletion of production data,
secret access and the rest keep their floors under
`kernel/GUARD_SPEC.md` whatever an analytics task concludes.

## Defaults

Each applies unless the venture's lock-book records a reason to depart.

**D1. Object-action event names, with anything varying per occurrence in
a property.** Names are generated from the product's objects and the
actions available on them rather than enumerated one at a time, and no
identifier, number or variant goes in the name (EV-0319). Reason: a
generated taxonomy stays finite, an enumerated one grows to thousands of
near-duplicates. The evidence is vendor assertion, and the casing is
taste.

**D2. Staging, intermediate and marts layering, one prefix per layer.**
Staging is one to one with sources and only cleans and renames, joins
and logic sit in intermediate models, marts hold business entities
(EV-0307). Reason: the prefix tells a reviewer what a model may do, so
review is mechanical. Costs model count and build time. Override for a
project small enough that the layers are ceremony.

**D3. Fixed horizon, unless a sequential method is chosen deliberately
and written into the stopping rule.** Reason: a correctly powered
fixed-horizon test left alone is the most powerful option per unit of
traffic (EV-0313). Where people will look anyway, fix the statistic
rather than the operator: always-valid and group sequential methods make
monitoring supported (EV-0312) and ship in a maintained Apache-2.0
library, so this is not a reason to buy a platform (EV-0317).

**D4. Below the traffic for a properly powered test, do not run one.**
An underpowered test launders a coin flip as evidence and is worse than
an argued decision with an instrumented rollout. Reason: with a low
prior on any idea working, a bare significant result from a small sample
is more likely false than a naive reading suggests (EV-0313). No source
says this plainly, because none was written for a venture. Decide by
argument, ship behind a flag, watch a guardrail (EV-0059).

**D5. One managed warehouse until the working set argues otherwise.**
Size the stack to the query working set rather than the storage total
(EV-0311). Reason: below a few terabytes the catalogue, compaction and
snapshot maintenance an open format asks for usually exceeds the
coupling it avoids (EV-0310).

**D6. Contracts on public models only.** Freeze the interface of models
other people read, leave private models uncontracted (EV-0057). Reason:
contract discipline on a model with one caller buys rigidity and no
coordination.

**D7. Use pre-experiment covariates where a stable unit was observed
before the test.** Variance reduction from pre-period behaviour bought
roughly half the variance at Bing, which is the same power at half the
users (EV-0315). Reason: sensitivity is cheaper than traffic. It does
nothing for new users, first-session funnels or anonymous traffic, so
the default holds only where the precondition does.

**D8. Identify by surrogate or hashed key in the analytics layer.** The
join key is a surrogate or a salted hash rather than the natural
identifier, so B3 has a cheap default answer. Reason: collecting less is
the cheapest privacy control and the sources barely mention it.
Differentially private aggregates (EV-0321) are a later step, never a
substitute for collecting less.

**D9. Every published table and every tracked event has one named owner,
and its schema, quality rules, freshness expectation and owner live in
one document.** `publishes_analytics_table`, `defines_events`. Reason:
the unowned gap. A schema contract with no freshness rule and a
freshness monitor with no owner produce the same outage, and the
structural point behind the data-contract standard is that they belong
in one document with a named team, not that the document uses a
particular format (EV-0305). This is a default rather than binding
because the estate chose it: no law, standard or measurement says the
five elements must sit in one file, and the outage it prevents is one a
rerun fixes. Departing means saying who owns the gap instead.

**D10. A quality gate failure blocks publication.**
`publishes_analytics_table`. A rule that raises a ticket while the table
publishes is monitoring, not a gate. Quality rules run inside the
pipeline as part of the build, not as a separate audit afterwards
(EV-0306, EV-0056). Reason: the documented-gate failure, a contract
written and never executed, which is documentation wearing a gate's
clothes. This is a default rather than binding because the evidence
behind it shows that in-pipeline checking works at scale, not that
blocking beats alerting; that comparison has not been run. Departing
means recording what stops bad data reaching a decision instead, and
saying it out loud, because a gate demoted to a monitor is the thing
this pack most often finds.

**D11. A fact model declares its grain in words before it declares
columns.** `publishes_analytics_table`. One sentence naming what one row
is. Reason: the unauditable table. Without a stated grain nobody can say
whether a count is double-counting, and every downstream number inherits
the ambiguity. Grain-first is the first of the three ordered dimensional
decisions and survives every argument about physical shape (EV-0308).
This is the grade the research gave it, and the ADR-0008 audit returned
it there: EV-0308 is a practice body with no measurement behind it, and
the failure is a number nobody can audit rather than one nobody can
undo.

## Preferences

Taste. Record them, do not gate on them, and override them without
asking.

- The contract file format. A dedicated standard, a transformation
  tool's schema file and an expectation suite all satisfy D9, and the
  format war is unsettled (EV-0305).
- The casing convention for event names and columns (EV-0319). Only
  consistency matters.
- The quality tool. Declared expectations (EV-0056) and computed metrics
  with anomaly detection (EV-0306) both work.
- Whether marts are wide entities or star-shaped, and whether dimensions
  carry surrogate keys. The sources disagree and neither argues it
  (EV-0307, EV-0308).
- The dashboard method, as long as one is committed to and the panels
  answer a named question (EV-0240).

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| Where does the quality rule live, and what does it stop? | `packs/data-analytics/guides/GD-DATA-001-quality-gate-placement.md` | Contract on public models, computed metrics behind them |
| What shape does the analytics model take? | `packs/data-analytics/guides/GD-DATA-002-model-shape.md` | Layered staging to marts, grain declared per fact |
| How is an experiment allowed to end? | `packs/data-analytics/guides/GD-DATA-003-experiment-stopping.md` | Fixed horizon, or no experiment at all |
| Where does the data sit? | `packs/data-analytics/guides/GD-DATA-004-storage-shape.md` | One managed warehouse |
| How are events named and validated? | `packs/data-analytics/guides/GD-DATA-005-event-contract.md` | Object-action convention plus review |

Level-three detail: `packs/data-analytics/refs/EXPERIMENT_STATS.md`,
`packs/data-analytics/refs/DATA_CONTRACT.md` and
`packs/data-analytics/refs/PRIVACY_IN_ANALYTICS.md`. Worked run:
`packs/data-analytics/exemplars/EX-DATA-001-gated-model-honest-experiment.md`.

## Failure modes and anti-patterns

- **The contract that never ran.** A schema file and a quality rule in
  the repository, and a pipeline that publishes regardless. D10.
- **Computing the check and reporting the win anyway.** Sample ratio
  mismatch detected, put in a footnote, decision taken. This is the
  failure this pack exists to stop (EV-0316).
- **Peeking at a fixed-horizon test.** Stopping the moment the line
  crosses, which is how the false positive rate leaves five per cent
  behind (EV-0313).
- **Learning the bug as a rule.** Constraint suggestion encodes whatever
  the data currently does, including the defect (EV-0306).
- **Semantic drift under a passing contract.** A column that changes
  from pence to pounds passes every shape check (EV-0057). No source
  found offers a gate. Treat it as unsolved and put the unit in the
  name.
- **Source columns copied forward.** An email address in a marts table
  because the source had one. B3.
- **Two models computing the same business number by different routes.**
  Whichever shape you chose, this is what it was built to stop.
- **The event catalogue explosion.** Identifiers, counters and variant
  names inside event names (EV-0319).
- **Causal language over observational data.** "The redesign lifted
  retention" from a before-and-after chart.
- **A surprisingly large effect believed.** It is evidence of a bug
  before it is evidence of a win (EV-0313).
- **The metric wall.** Every available series on one dashboard, with no
  named question (EV-0240).
- **Differential privacy as a badge.** The primitives assume a bounded
  contribution per user per partition and do not enforce it, so
  contribution limiting is the caller's job and getting it wrong voids
  the guarantee silently (EV-0321). Ask what the privacy unit is and
  what the implementation does that the proof does not cover (EV-0320).

## Open questions and counter-evidence

**The storage argument is a live contradiction and this pack takes a
side.** The lakehouse position paper argues the two-tier shape is broken
by duplication and staleness, with benchmark numbers answering the
performance objection (EV-0309). The counter-account reports most
warehouse customers holding under a terabyte and around ninety per cent
of queries scanning under 100 MB (EV-0311). Both are vendor sources
arguing for their own product and both are discounted. They are not
really disagreeing: one describes an estate that already has a lake, the
other describes everyone else. D5 assumes a venture is the second
population.

**Model shape is contested and neither side argues it.** Dimensional
practice keeps facts narrow and joins to conformed dimensions (EV-0308);
the transformation-tool guide lands on wide entities and does not
mention star schemas at all (EV-0307). The dimensional source has not
been substantially maintained since its authors wound down, and its
physical prescriptions assume hardware nobody runs. Grain-first and one
route to each business number survive both.

**Registry-enforced event schemas against convention plus review is
unmeasured.** Both are asserted, no comparison exists in the sources
found (EV-0318, EV-0319), and the choice rests on whether you own the
collection path, which is a fit argument and not an evidence one.

**Peeking is a genuine methodological standoff.** One peer-reviewed
position treats it as an operator error to correct (EV-0313), the other
as a stopping-rule property to fix in the statistic (EV-0312). D3 sides
with the first and names the second as the deliberate alternative.
Relatedly, the power cost of always-valid inference at venture sample
sizes is measured nowhere found, which is exactly the number D3 and D4
would need.

**The base rate is population-bound.** The figure of roughly eighty-five
to ninety per cent of ideas failing to move the target metric comes from
mature products at scale where the obvious wins are gone (EV-0313). A
young product may face a better prior. Use it to argue for humility,
never as a computed input.

**A proportionate quality gate for a two-person venture is unaddressed
by every source here.** All of them assume a data team. D9 and D10 are
written to be satisfiable by one file and one pipeline step, which is a
judgement, not a finding.

**The grain rule was promoted above its research grade, and has been put
back.** The research graded grain declaration a default; an earlier
draft of this pack bound it as B6, on the argument that a table whose
grain nobody stated cannot be audited. The ADR-0008 audit returned it to
a default as D11, because that argument names an auditing gap rather
than a serious or irreversible failure, and because its basis was an
estate decision. Nothing about how the work should be done changed.

**Refresh triggers.** Re-argue this pack on: a published comparison of
registry-enforced and convention-only event taxonomies; any measurement
of the sequential power penalty at sample sizes under one hundred
thousand units; a non-vendor account of warehouse working sets; a
successor to or replacement for the dimensional modelling source; a
change to UK data protection commencement or the ICO guidance
interpreting it (EV-0225, EV-0041).

## Evidence pointer

The seventeen sources behind this pack were frozen at
`packs/data-analytics/research/sources.fragment.json` and have since
been imported into `registry/evidence.json` as EV-0305 to EV-0321. Every
`EV-` id cited above resolves to a row there carrying that source's
version, licence, access date and review trigger. The rest are estate
rows this pack borrows: UK data protection (EV-0041, EV-0225), the
quality and contract rows from earlier research (EV-0056, EV-0057), the
event envelope and registry rows (EV-0138, EV-0139), the guardrail
tooling row (EV-0059) and the dashboard row (EV-0240). The synthesis is
in `packs/data-analytics/research/NOTES.md`, and the licence and
quotation sweep is at
`packs/data-analytics/research/provenance.fragment.json`.
