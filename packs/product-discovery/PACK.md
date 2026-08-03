---
summary: Deciding what to build and whether to build it, problem framing, evidence provenance, the discovery record and the kill verdict
type: playbook
tags: [eos, product, testing]
kind: rule
authority: binding
lifecycle: active
basis: decision
evidence_grade: observational
scope: estate
applies_when: [proposes_capability, prioritises_work, cites_user_claim, runs_experiment, writes_acceptance_criteria]
volatility: slow
review: 2027-08
sources: [EV-0010, EV-0059, EV-0074, EV-0075, EV-0153]
---

# Product discovery pack

This pack covers product discovery: how a request becomes a stated
problem, what evidence is allowed to settle it, and how the verdict to
build, test or kill gets recorded. It activates on any task that
proposes new capability, ranks work, cites a claim about users, or
writes acceptance criteria. Discovery here is a record and a verdict
rather than a phase, and kill is always one of the verdicts on offer.

## Activation

Load this pack when any of the following holds.

**Paths touched.** A roadmap, backlog or prioritisation file; a
requirements, spec, PRD or brief document; a discovery, research or
interview note; a persona or segment file; an experiment plan or
readout; a feature-request or intake queue.

**Task types.** SPIKE and any task that decides whether to build
something. Writing or revising acceptance criteria. Ranking or
re-ranking work. Reading research, support tickets or telemetry to
justify a change. Designing or reading out an experiment. Turning a
stakeholder request into a work item.

**Keywords, fallback only.** Discovery, requirement, user need, problem
statement, persona, interview, survey, roadmap, prioritise, backlog,
RICE, opportunity, MVP, hypothesis, A/B test, experiment, feature
request. Keywords are the weakest signal and never override the
predicates.

**Applicability predicates.** Every requirement below names the
predicate that turns it on.

| Predicate | True when |
| --- | --- |
| proposes_capability | the task would add or remove something a user can do |
| prioritises_work | the task orders two or more candidate pieces of work |
| cites_user_claim | the task asserts something about what people want, do or would pay for |
| runs_experiment | the task changes behaviour for some users to read a metric |
| writes_acceptance_criteria | the task states the conditions under which work is done |
| has_reachable_users | real users of this product can be contacted or observed |
| has_live_traffic | the surface is in front of users and instrumented |
| is_irreversible | undoing the change costs materially more than making it |

A task that trips a path trigger and satisfies no predicate loads
nothing beyond the first paragraph. A CHORE that renames a file in a
discovery directory is not discovery.

## Outcomes and non-goals

**Outcomes.** The problem being solved is written down in a form that
survives a change of implementation. Every claim used to justify work
can be traced to a thing that exists. The verdict is one of three
words, kill among them, and the observation that would overturn it is
named at the same time. Where an experiment settled the question, its
rules were fixed before its data arrived.

**Non-goals.** This pack does not own experiment statistics, event
taxonomy or metric definitions, which sit in the data-analytics pack.
It does not own pricing, packaging or willingness to pay, which sit in
the business-model-pricing pack. It does not own usability craft or
interface quality, which sit in the ui-ux pack. It does not own how the
work is then built or reviewed, which sits in the coding pack. It does
not carry a prioritisation formula, and the guides explain why.

## Binding requirements

Eight requirements bind. Each names its predicate, its evidence and the
failure it prevents. Where the basis is a decision rather than a
standard or a measurement, that is said plainly: it binds because the
estate ruled it, not because evidence compels it.

Every `EV-` id points at a row in `registry/evidence.json` carrying that
source's version, licence, access date, maintenance state and review
trigger. Every `FRAG-PRODUCT-DISCOVERY-` id points at a frozen row in
`packs/product-discovery/research/sources.fragment.json` that is not yet
imported into the ledger; the integrator assigns its final EV id at
import and rewrites the citations here. Nothing is cited that does not
resolve to one of those two files.

**B1. A discovery record exists and names the decision it unblocks.**
`proposes_capability`. The record carries the fixed sections set out in
`packs/product-discovery/refs/DISCOVERY_RECORD.md`. Prevents the
proposal that cannot be wrong: the goals-signals-metrics ladder holds
that a proposal with no stated signal is untestable and that a metric
picked before its goal is a vanity metric by construction
(`FRAG-PRODUCT-DISCOVERY-08`). Basis: decision, on that ladder.

**B2. The problem is stated without naming the proposed solution.**
`proposes_capability`. The problem section describes what a person
cannot do today and what it costs them, and it does not contain the
name of the requested feature. Prevents a solution wearing a problem's
clothes, which the discovery exit criteria exist to catch
(`FRAG-PRODUCT-DISCOVERY-01`). Basis: standard.

**B3. Every signal names a threshold and a source that exists.**
`proposes_capability`. Each signal line carries the observation, the
number or state that would count as the signal firing, and the artefact
it will be read from. A source is a file, a table, a ticket export or a
named instrument that already exists. Prevents the readout that gets
invented after the fact (`FRAG-PRODUCT-DISCOVERY-08`). Basis: decision.

**B4. All four risks are retired explicitly, viability in writing.**
`proposes_capability`. Value, usability, feasibility and viability each
get a written answer, and none may be left blank
(`FRAG-PRODUCT-DISCOVERY-14`). Prevents the solo failure the source
itself predicts: with one operator holding all four, the two that are
interesting get tested and the other two get assumed, and viability is
the one that goes. Basis: decision. The research graded this a default;
this pack promotes it, because "discovery is finished" is unauditable
otherwise. See Open questions.

**B5. Every number carries its own provenance.** `cites_user_claim`. A
figure used to justify work names where it came from, and a figure whose
base cannot be reached is struck rather than softened. Prevents the
folklore statistic: the famous claim that 64 per cent of features are
rarely or never used traces to a 2002 keynote about four internal
applications and was repeated for two decades unchecked
(`FRAG-PRODUCT-DISCOVERY-17`). Basis: decision, and the reason this
repo keeps an evidence ledger at all.

**B6. Claims about people that a model produced are labelled
unverified.** `cites_user_claim`. A persona, segment or quotation
generated rather than observed is marked at the point of use, and it
never carries a decision on its own. Prevents the confidently wrong
segment: against two real survey datasets, no tested model beat the
strongest non-LLM baseline at the individual level, and on segment
targeting the models inflated between-segment gaps two to fourfold and
would have pointed a team at the wrong segment in half the US cases
(`FRAG-PRODUCT-DISCOVERY-11`). Scope note: that benchmark is
attitudinal survey prediction, not interview simulation or task
observation. Basis: empirical-evidence.

**B7. An experiment fixes its stopping rule, metric, segmentation and
sample before data arrives.** `runs_experiment`. All four are written
in the record before the change ships. Prevents the practices that are
wrong by construction, chiefly stopping at first significance and
reading small-sample results as directional
(`FRAG-PRODUCT-DISCOVERY-04`), and matches the asymmetric gate where
goal metrics drive the ship decision and guardrails block only on
significant harm (EV-0059). Basis: empirical-evidence.

**B8. The record ends in BUILD, TEST or KILL.**
`proposes_capability`. One of the three words, alone, with the reason
under it. Prevents the verdict that is really a deferral. Stopping at
the end of discovery counts as a successful discovery, which is what
makes kill part of the definition rather than an embarrassment
(`FRAG-PRODUCT-DISCOVERY-01`). Basis: standard.

Activation gives advice, never permission. Nothing here lowers a tier
floor in `kernel/POLICY_SPEC.md` or converts a manual-only action class
into an autonomous one under `kernel/GUARD_SPEC.md`. A BUILD verdict is
not an approval to ship.

## Defaults

Each applies unless the record states a reason to depart.

**D1. Depth is set by reversibility, not by the size of the request.**
An irreversible commitment earns a phase; a reversible change on a live
surface earns an instrument and a week. Reason: the four-to-eight-week
discovery box was calibrated for teams whose build step was the
expensive part (`FRAG-PRODUCT-DISCOVERY-01`), and boundaries are
discovered under change rather than designed in advance (EV-0153). See
`packs/product-discovery/guides/GD-DISC-001-discovery-depth.md`.

**D2. Elicit outcomes, not features.** Write what the person is trying
to achieve at a step of their job, in a form that could be measured.
Reason: an outcome statement survives a change of technology and a
feature request does not (`FRAG-PRODUCT-DISCOVERY-16`). Take the
elicitation and leave the arithmetic; see Preferences.

**D3. Carry more than one candidate solution before committing.**
Reason: the first idea is otherwise compared against nothing
(`FRAG-PRODUCT-DISCOVERY-13`). The specific count of three is a
convention, not a finding.

**D4. Say whether you are diverging or converging, and separate them in
time.** Reason: a team that converges while still diverging picks the
first idea and calls it a decision (`FRAG-PRODUCT-DISCOVERY-09`).

**D5. Prefer throughput of cheap reversible tests over accuracy of
ranking, where there is traffic to read.** Reason: across a large corpus
of randomised online experiments roughly a third of ideas moved the
target metric positively, a third were flat and a third were negative,
and expert judgement inside the team did not predict which
(`FRAG-PRODUCT-DISCOVERY-03`). Scope note: that population is very
high-traffic consumer search and portal surfaces where a powered test
finishes in days. Below the power floor the base rate is a prior about
idea quality, not a runnable method.

**D6. Give a model the structuring job on real human input, never the
origination job on invented input.** Reason: human discussion followed
by model synthesis of the transcript beat both unaided collaboration and
direct model generation (`FRAG-PRODUCT-DISCOVERY-10`), while simulated
respondents fail hardest on the segment question teams most want to ask
(`FRAG-PRODUCT-DISCOVERY-11`). Scope note: the first is a preprint
scored against a documentation standard, which rewards well-formed prose
and cannot detect a well-written requirement for the wrong thing.

**D7. Reason about the worst case of a small sample, not its average.**
Across random sets of five participants the share of known problems
found ranged from 99 per cent down to 55; ten raised the floor to about
80 and twenty to about 95 (`FRAG-PRODUCT-DISCOVERY-05`). Reason: you
draw one sample and cannot tell which one you drew. Scope note: one 2003
web application, usability defect finding rather than demand.

**D8. Recruit by frame, then by count.** Decide which ways of using the
product are in scope, including assisted and offline routes, before
deciding how many people to talk to (`FRAG-PRODUCT-DISCOVERY-02`).
Reason: the recruitment frame is what makes a discovery wrong. Scope
note: a public service must serve everyone, so a venture choosing a
niche is making a scoping decision and writes down who it excluded.

**D9. Write acceptance criteria in EARS clause order once the problem is
settled.** While a precondition, when a trigger, the named system shall
produce a response, one trigger at most and one system exactly
(`FRAG-PRODUCT-DISCOVERY-07`). Reason: a requirement that will not fit
the template is usually a wish, a design decision, or two requirements
stuck together. Scope note: EARS was derived on airworthiness
regulations where the trigger set is closed. It constrains form only.
See
`packs/product-discovery/guides/GD-DISC-004-acceptance-criteria-form.md`.

## Preferences

These are taste. Record them, do not gate on them, override without
asking.

- **The specific numbers.** Four to eight weeks of discovery, five
  users, three candidate solutions, three to four interviews per
  revision, confidence tiers of 100, 80 and 50 per cent. None of these
  has evidence behind the exact value. They are conventions that
  happen to be widely shared, which is a different thing.
- **RICE, reduced to its confidence multiplier.** The one part worth
  keeping is being made to write down how much of the score is
  guesswork; its own author says the score is not a rule
  (`FRAG-PRODUCT-DISCOVERY-15`). The rest multiplies three subjective
  estimates into a precise-looking number with invisible error bars.
- **Opportunity solution trees as the drawing.** A useful way to see
  one outcome, its opportunities and their candidate solutions on one
  page (`FRAG-PRODUCT-DISCOVERY-13`). The drawing is a convenience; the
  three rules inside it are what do the work, and two of those are D2
  and D3 above.
- **Double diamond vocabulary.** Fine as shared language, empty as a
  method: it carries no criterion for when a diamond is finished
  (`FRAG-PRODUCT-DISCOVERY-09`).
- **Where the record lives.** One `discovery.md` per decision, beside
  the work, rather than a research wiki.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| How much discovery does this decision deserve? | `packs/product-discovery/guides/GD-DISC-001-discovery-depth.md` | Depth set by reversibility |
| Where does the evidence about users come from? | `packs/product-discovery/guides/GD-DISC-002-user-evidence-source.md` | Observation of real users; experiment only above the power floor |
| How do you choose between candidate opportunities? | `packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md` | Sequence by reversibility, test cheaply, do not score |
| When is the problem settled, and in what form do criteria go? | `packs/product-discovery/guides/GD-DISC-004-acceptance-criteria-form.md` | EARS clause order, after the problem is settled |

Level-three material sits in `packs/product-discovery/refs/`, a worked
run in `packs/product-discovery/exemplars/`, and the evaluation criteria
in `packs/product-discovery/CHECKS.md`.

## Failure modes and anti-patterns

- **The feature request restated as a problem.** "Users need an
  approvals inbox" is a solution with a verb in front of it. B2 exists
  for this one case.
- **Four weeks of discovery on something an agent could build and
  instrument in a day.** The phase length was priced for expensive
  builds (`FRAG-PRODUCT-DISCOVERY-01`).
- **A test at low traffic, reported with statistics.** Below the power
  floor the numbers are decoration, and the practices that manufacture
  false confidence are well catalogued
  (`FRAG-PRODUCT-DISCOVERY-04`).
- **Stopping the test when it first crosses significance.** Wrong by
  construction, not merely optimistic (`FRAG-PRODUCT-DISCOVERY-04`).
- **Invented personas doing real work.** A persona with no interview
  behind it is a hypothesis wearing a name and a photograph
  (`FRAG-PRODUCT-DISCOVERY-11`).
- **The unchecked headline number.** Any figure quoted without its base
  (`FRAG-PRODUCT-DISCOVERY-17`).
- **Prioritisation scores presented as findings.** Three subjective
  estimates multiplied together still have no error bars
  (`FRAG-PRODUCT-DISCOVERY-15`).
- **Effort smuggled into the value comparison.** Comparing
  opportunities by cost lets cheapness pose as value
  (`FRAG-PRODUCT-DISCOVERY-13`).
- **Discovery that cannot produce a kill.** If nobody has killed
  anything, the process is a queue with paperwork.
- **Believing you moved fast.** Experienced developers were 19 per cent
  slower with early-2025 tooling while believing they were 20 per cent
  faster, so self-reported speed is not evidence about a build estimate
  in a discovery record (EV-0010).

## Open questions and counter-evidence

**This domain has far weaker evidence than the engineering packs.** Most
of what circulates as discovery method is consultancy practice published
as blog posts and never independently evaluated. Two sources here are
controlled work that contradicts widely taught rules. That is why most
of this pack sits in Defaults and Preferences, and why only two of the
eight binding requirements rest on measurement.

**No prioritisation framework has controlled evidence.** RICE
(`FRAG-PRODUCT-DISCOVERY-15`) is one company's internal tool published
as a blog post with no evaluation against an alternative. The
outcome-driven opportunity score
(`FRAG-PRODUCT-DISCOVERY-16`) adds an importance rating to a difference
of two ratings on the same scale with no stated justification, needs 180
to 600 respondents, and every effectiveness claim comes from the firm
that sells it. Opportunity solution trees
(`FRAG-PRODUCT-DISCOVERY-13`) are coaching practice. None of the three
is refuted; none is supported either. The pack takes their elicitation
halves and refuses their arithmetic.

**Five users against worst-case five users.** The five-user convention
optimises expected problems found per pound across iterations
(`FRAG-PRODUCT-DISCOVERY-06`); the resampling study measures the
variance that expected value hides
(`FRAG-PRODUCT-DISCOVERY-05`). These are different objective functions
rather than contradictory data. D7 takes the worst case. Note also that
the five-user article is twenty-six years old, has never been revised,
and is routinely cited to justify five customer interviews, which is a
different activity from the usability defect finding it models.

**Spec-driven development is unproven at the cutoff.** EV-0074 and
EV-0075 present it as an established improvement. The registered report
that tests exactly that question had its protocol accepted and no
results collected at 2026-08-03 (`FRAG-PRODUCT-DISCOVERY-12`), and the
spec-kit repository calls itself experimental. D9 teaches EARS on its
own merits and borrows no authority from the spec-driven claim.

**The 80 per cent unused figure is direction, not magnitude.** The
instrumented telemetry version (`FRAG-PRODUCT-DISCOVERY-18`) is vendor
research with a commercial interest in the answer, no published
methodology for what counts as a feature or as used, a sample confined
to firms that bought product analytics, and seven years stale. Cite it
with the vendor label attached every time, or not at all.

**B4 is promoted above its research grade.** The four risks were graded
a default by the research and bind here. The reason is auditability
rather than evidence: with no written viability answer there is no way
to tell a finished discovery from an abandoned one. It is basis
decision and open to challenge.

**Nobody has repriced discovery against a near-zero build cost.** The
whole literature was written when building was the expensive step. No
source located addresses what discovery is for when an agent builds the
thing in an afternoon. EV-0010 is the nearest signal that intuitions
about agentic speed are unreliable, and EV-0153 the nearest structural
analogue.

**Two things this pack cannot answer.** Whether the one-third base rate
of `FRAG-PRODUCT-DISCOVERY-03` holds for agent-generated ideas, and at
what traffic level an experiment stops being theatre for a venture with
hundreds rather than millions of users. No data either way at the
cutoff. `packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md` gives a
working rule and labels it as a working rule.

**Refresh triggers.** Re-argue this pack on: results landing for
`FRAG-PRODUCT-DISCOVERY-12`; any independent controlled evaluation of a
prioritisation framework; a newer telemetry study of feature usage; a
revision of the GOV.UK discovery guidance; a current-model replication
of the synthetic-respondent benchmark.
