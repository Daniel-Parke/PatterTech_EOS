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
activation_paths: [**/roadmap*, **/backlog*, **/specs/**, **/*brief*.md, **/*prd*.md, **/discovery/**, **/*acceptance*]
volatility: slow
review: 2028-06
sources: [EV-0010, EV-0059, EV-0074, EV-0075, EV-0153, EV-0403, EV-0404, EV-0405, EV-0406, EV-0407, EV-0408, EV-0409, EV-0410, EV-0411, EV-0412, EV-0413, EV-0414, EV-0415, EV-0416, EV-0417, EV-0418, EV-0419, EV-0420]
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

Two requirements bind. Each names its predicate, its evidence and the
failure it prevents.

The 2026-08 authority audit under ADR-0008 put one test to all eight
requirements this pack used to bind: a rule binds only where it prevents
a concrete failure that is serious or hard to reverse **and** its basis
is law, a standard, empirical evidence or a protected-set floor. Six
failed it and are now defaults. They keep their B numbers, because
`packs/product-discovery/CHECKS.md`, the guides, the refs and the
exemplar all cite them, and they sit under Defaults below. A default is
departed from in writing, never in silence.

Every `EV-` id points at a row in `registry/evidence.json` carrying that
source's version, licence, access date, maintenance state and review
trigger. The eighteen sources researched for this pack were imported as
EV-0403 to EV-0420, and every citation here uses the ledger id. The
frozen batch the import was made from stays at
`packs/product-discovery/research/sources.fragment.json`, and the
synthesis behind the pack is in
`packs/product-discovery/research/NOTES.md`. Nothing is cited that does
not resolve in the ledger.

**B6. Claims about people that a model produced are labelled
unverified.** `cites_user_claim`. A persona, segment or quotation
generated rather than observed is marked at the point of use, and it
never carries a decision on its own. Prevents the confidently wrong
segment: against two real survey datasets, no tested model beat the
strongest non-LLM baseline at the individual level, and on segment
targeting the models inflated between-segment gaps two to fourfold and
would have pointed a team at the wrong segment in half the US cases
(`EV-0413`). Scope note: that benchmark is
attitudinal survey prediction, not interview simulation or task
observation. Basis: empirical-evidence.

**B7. An experiment fixes its stopping rule, metric, segmentation and
sample before data arrives.** `runs_experiment`. All four are written
in the record before the change ships. Prevents the practices that are
wrong by construction, chiefly stopping at first significance and
reading small-sample results as directional
(`EV-0406`), and matches the asymmetric gate where
goal metrics drive the ship decision and guardrails block only on
significant harm (EV-0059). Basis: empirical-evidence.

Activation gives advice, never permission. Nothing here lowers a tier
floor in `kernel/POLICY_SPEC.md` or converts a manual-only action class
into an autonomous one under `kernel/GUARD_SPEC.md`. A BUILD verdict is
not an approval to ship.

## Defaults

Each applies unless the record states a reason to depart.

### Demoted from binding, 2026-08

Six rules that used to bind. Each still names the failure it prevents,
and each says which leg of the ADR-0008 test it failed. Numbers are
unchanged so the checks and guides that cite them still resolve.

**B1. A discovery record exists and names the decision it unblocks.**
`proposes_capability`. The record carries the fixed sections set out in
`packs/product-discovery/refs/DISCOVERY_RECORD.md`. Prevents the
proposal that cannot be wrong: the goals-signals-metrics ladder holds
that a proposal with no stated signal is untestable and that a metric
picked before its goal is a vanity metric by construction
(`EV-0410`). Basis: decision, on that ladder. Failed the basis leg: one
consultancy ladder, never evaluated.

**B2. The problem is stated without naming the proposed solution.**
`proposes_capability`. The problem section describes what a person
cannot do today and what it costs them, and it does not contain the
name of the requested feature. Prevents a solution wearing a problem's
clothes, which the discovery exit criteria exist to catch
(`EV-0403`). Basis: standard. Failed the seriousness leg: a badly framed
problem is rewritten, and the verdict below is where the cost lands.

**B3. Every signal names a threshold and a source that exists.**
`proposes_capability`. Each signal line carries the observation, the
number or state that would count as the signal firing, and the artefact
it will be read from. A source is a file, a table, a ticket export or a
named instrument that already exists. Prevents the readout that gets
invented after the fact (`EV-0410`). Basis: decision. Failed the basis
leg, same ladder as B1.

**B4. All four risks are retired explicitly, viability in writing.**
`proposes_capability`. Value, usability, feasibility and viability each
get a written answer, and none may be left blank
(`EV-0416`). Prevents the solo failure the source
itself predicts: with one operator holding all four, the two that are
interesting get tested and the other two get assumed, and viability is
the one that goes. Basis: decision. Failed the basis leg, and the audit
returned it to the grade the research gave it in the first place.

**B5. Every number carries its own provenance.** `cites_user_claim`. A
figure used to justify work names where it came from, and a figure whose
base cannot be reached is struck rather than softened. Prevents the
folklore statistic: the famous claim that 64 per cent of features are
rarely or never used traces to a 2002 keynote about four internal
applications and was repeated for two decades unchecked
(`EV-0419`). Basis: decision, and the reason this repo keeps an evidence
ledger at all. Failed the basis leg. Departing from it inside this
repository is still a governance matter, because the ladder in
`GOVERNANCE.md` is not this pack's to loosen.

**B8. The record ends in BUILD, TEST or KILL.**
`proposes_capability`. One of the three words, alone, with the reason
under it. Prevents the verdict that is really a deferral. Stopping at
the end of discovery counts as a successful discovery, which is what
makes kill part of the definition rather than an embarrassment
(`EV-0403`). Basis: standard. Failed the seriousness leg: a deferral is
the cheapest thing in this pack to reverse.

### Standing defaults

**D1. Depth is set by reversibility, not by the size of the request.**
An irreversible commitment earns a phase; a reversible change on a live
surface earns an instrument and a week. Reason: the four-to-eight-week
discovery box was calibrated for teams whose build step was the
expensive part (`EV-0403`), and boundaries are
discovered under change rather than designed in advance (EV-0153). See
`packs/product-discovery/guides/GD-DISC-001-discovery-depth.md`.

**D2. Elicit outcomes, not features.** Write what the person is trying
to achieve at a step of their job, in a form that could be measured.
Reason: an outcome statement survives a change of technology and a
feature request does not (`EV-0418`). Take the
elicitation and leave the arithmetic; see Preferences.

**D3. Carry more than one candidate solution before committing.**
Reason: the first idea is otherwise compared against nothing
(`EV-0415`). The specific count of three is a
convention, not a finding.

**D4. Say whether you are diverging or converging, and separate them in
time.** Reason: a team that converges while still diverging picks the
first idea and calls it a decision (`EV-0411`).

**D5. Prefer throughput of cheap reversible tests over accuracy of
ranking, where there is traffic to read.** Reason: across a large corpus
of randomised online experiments roughly a third of ideas moved the
target metric positively, a third were flat and a third were negative,
and expert judgement inside the team did not predict which
(`EV-0405`). Scope note: that population is very
high-traffic consumer search and portal surfaces where a powered test
finishes in days. Below the power floor the base rate is a prior about
idea quality, not a runnable method.

**D6. Give a model the structuring job on real human input, never the
origination job on invented input.** Reason: human discussion followed
by model synthesis of the transcript beat both unaided collaboration and
direct model generation (`EV-0412`), while simulated
respondents fail hardest on the segment question teams most want to ask
(`EV-0413`). Scope note: the first is a preprint
scored against a documentation standard, which rewards well-formed prose
and cannot detect a well-written requirement for the wrong thing.

**D7. Reason about the worst case of a small sample, not its average.**
Across random sets of five participants the share of known problems
found ranged from 99 per cent down to 55; ten raised the floor to about
80 and twenty to about 95 (`EV-0407`). Reason: you
draw one sample and cannot tell which one you drew. Scope note: one 2003
web application, usability defect finding rather than demand.

**D8. Recruit by frame, then by count.** Decide which ways of using the
product are in scope, including assisted and offline routes, before
deciding how many people to talk to (`EV-0404`).
Reason: the recruitment frame is what makes a discovery wrong. Scope
note: a public service must serve everyone, so a venture choosing a
niche is making a scoping decision and writes down who it excluded.

**D9. Write acceptance criteria in EARS clause order once the problem is
settled.** While a precondition, when a trigger, the named system shall
produce a response, one trigger at most and one system exactly
(`EV-0409`). Reason: a requirement that will not fit
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
  (`EV-0417`). The rest multiplies three subjective
  estimates into a precise-looking number with invisible error bars.
- **Opportunity solution trees as the drawing.** A useful way to see
  one outcome, its opportunities and their candidate solutions on one
  page (`EV-0415`). The drawing is a convenience; the
  three rules inside it are what do the work, and two of those are D2
  and D3 above.
- **Double diamond vocabulary.** Fine as shared language, empty as a
  method: it carries no criterion for when a diamond is finished
  (`EV-0411`).
- **Where the record lives.** One `discovery.md` per decision, beside
  the work, rather than a research wiki.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| How much discovery does this decision deserve? | `packs/product-discovery/guides/GD-DISC-001-discovery-depth.md` | Depth set by reversibility |
| Where does the evidence about users come from? | `packs/product-discovery/guides/GD-DISC-002-user-evidence-source.md` | Observation of real users; experiment only above the power floor |
| How do you choose between candidate opportunities? | `packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md` | Sequence by reversibility, test cheaply, do not score |
| When is the problem settled, and in what form do criteria go? | `packs/product-discovery/guides/GD-DISC-004-acceptance-criteria-form.md` | EARS clause order, after the problem is settled |

Level-three material sits in `packs/product-discovery/refs/`: the
discovery record shape and the sample-and-signal working rule. A worked
run is in `packs/product-discovery/exemplars/`, and the evaluation
criteria in `packs/product-discovery/CHECKS.md`.

## Failure modes and anti-patterns

- **The feature request restated as a problem.** "Users need an
  approvals inbox" is a solution with a verb in front of it. B2 exists
  for this one case.
- **Four weeks of discovery on something an agent could build and
  instrument in a day.** The phase length was priced for expensive
  builds (`EV-0403`).
- **A test at low traffic, reported with statistics.** Below the power
  floor the numbers are decoration, and the practices that manufacture
  false confidence are well catalogued
  (`EV-0406`).
- **Stopping the test when it first crosses significance.** Wrong by
  construction, not merely optimistic (`EV-0406`).
- **Invented personas doing real work.** A persona with no interview
  behind it is a hypothesis wearing a name and a photograph
  (`EV-0413`).
- **The unchecked headline number.** Any figure quoted without its base
  (`EV-0419`).
- **Prioritisation scores presented as findings.** Three subjective
  estimates multiplied together still have no error bars
  (`EV-0417`).
- **Effort smuggled into the value comparison.** Comparing
  opportunities by cost lets cheapness pose as value
  (`EV-0415`).
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
of this pack sits in Defaults and Preferences, and why the 2026-08 audit
left binding only the two requirements that rest on measurement.

**No prioritisation framework has controlled evidence.** RICE
(`EV-0417`) is one company's internal tool published
as a blog post with no evaluation against an alternative. The
outcome-driven opportunity score
(`EV-0418`) adds an importance rating to a difference
of two ratings on the same scale with no stated justification, needs 180
to 600 respondents, and every effectiveness claim comes from the firm
that sells it. Opportunity solution trees
(`EV-0415`) are coaching practice. None of the three
is refuted; none is supported either. The pack takes their elicitation
halves and refuses their arithmetic.

**Five users against worst-case five users.** The five-user convention
optimises expected problems found per pound across iterations
(`EV-0408`); the resampling study measures the
variance that expected value hides
(`EV-0407`). These are different objective functions
rather than contradictory data. D7 takes the worst case. Note also that
the five-user article is twenty-six years old, has never been revised,
and is routinely cited to justify five customer interviews, which is a
different activity from the usability defect finding it models.

**Spec-driven development is unproven at the cutoff.** EV-0074 and
EV-0075 present it as an established improvement. The registered report
that tests exactly that question had its protocol accepted and no
results collected at 2026-08-03 (`EV-0414`), and the
spec-kit repository calls itself experimental. D9 teaches EARS on its
own merits and borrows no authority from the spec-driven claim.

**The 80 per cent unused figure is direction, not magnitude.** The
instrumented telemetry version (`EV-0420`) is vendor
research with a commercial interest in the answer, no published
methodology for what counts as a feature or as used, a sample confined
to firms that bought product analytics, and seven years stale. Cite it
with the vendor label attached every time, or not at all.

**B4 no longer binds, and the argument for it is still good.** The four
risks were graded a default by the research, promoted here on
auditability rather than evidence, and returned to a default by the
2026-08 audit. The argument that made the promotion stands: with no
written viability answer there is no way to tell a finished discovery
from an abandoned one. It is now a default with that reason attached,
which means a record that skips viability says why.

**Nobody has repriced discovery against a near-zero build cost.** The
whole literature was written when building was the expensive step. No
source located addresses what discovery is for when an agent builds the
thing in an afternoon. EV-0010 is the nearest signal that intuitions
about agentic speed are unreliable, and EV-0153 the nearest structural
analogue.

**Two things this pack cannot answer.** Whether the one-third base rate
of `EV-0405` holds for agent-generated ideas, and at
what traffic level an experiment stops being theatre for a venture with
hundreds rather than millions of users. No data either way at the
cutoff. `packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md` gives a
working rule and labels it as a working rule.

**Refresh triggers.** Re-argue this pack on: results landing for
`EV-0414`; any independent controlled evaluation of a
prioritisation framework; a newer telemetry study of feature usage; a
revision of the GOV.UK discovery guidance; a current-model replication
of the synthetic-respondent benchmark.
