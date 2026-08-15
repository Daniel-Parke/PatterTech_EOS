---
summary: Activation, outcomes and decision map for the product-discovery Doctrine and Wargames
type: playbook
tags: [eos, product, testing]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [proposes_capability, prioritises_work, cites_user_claim, runs_experiment, writes_acceptance_criteria]
activation_paths: [**/roadmap*, **/backlog*, **/specs/**, **/*brief*.md, **/*prd*.md, **/discovery/**, **/*acceptance*]
volatility: slow
review: none
sources: [EV-0010, EV-0059, EV-0074, EV-0075, EV-0153, EV-0403, EV-0404, EV-0405, EV-0406, EV-0407, EV-0408, EV-0409, EV-0410, EV-0411, EV-0412, EV-0413, EV-0414, EV-0415, EV-0416, EV-0417, EV-0418, EV-0419, EV-0420]
depends_on: []
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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B6"></a>
- `B6` to [DOC-DISC-001](doctrines/DOC-DISC-001-claims-about-people-that-a-model-produced-are-labelled-unverifie.md) (binding)
<a id="B7"></a>
- `B7` to [DOC-DISC-002](doctrines/DOC-DISC-002-an-experiment-fixes-its-stopping-rule-metric-segmentation-and-sa.md) (binding)
<a id="B1"></a>
- `B1` to [DOC-DISC-003](doctrines/DOC-DISC-003-a-discovery-record-exists-and-names-the-decision-it-unblocks.md) (default)
<a id="B2"></a>
- `B2` to [DOC-DISC-004](doctrines/DOC-DISC-004-the-problem-is-stated-without-naming-the-proposed-solution.md) (default)
<a id="B3"></a>
- `B3` to [DOC-DISC-005](doctrines/DOC-DISC-005-every-signal-names-a-threshold-and-a-source-that-exists.md) (default)
<a id="B4"></a>
- `B4` to [DOC-DISC-006](doctrines/DOC-DISC-006-all-four-risks-are-retired-explicitly-viability-in-writing.md) (default)
<a id="B5"></a>
- `B5` to [DOC-DISC-007](doctrines/DOC-DISC-007-every-number-carries-its-own-provenance.md) (default)
<a id="B8"></a>
- `B8` to [DOC-DISC-008](doctrines/DOC-DISC-008-the-record-ends-in-build-test-or-kill.md) (default)
<a id="D1"></a>
- `D1` to [DOC-DISC-009](doctrines/DOC-DISC-009-depth-is-set-by-reversibility-not-by-the-size-of-the-request.md) (default)
<a id="D2"></a>
- `D2` to [DOC-DISC-010](doctrines/DOC-DISC-010-elicit-outcomes-not-features.md) (default)
<a id="D3"></a>
- `D3` to [DOC-DISC-011](doctrines/DOC-DISC-011-carry-more-than-one-candidate-solution-before-committing.md) (default)
<a id="D4"></a>
- `D4` to [DOC-DISC-012](doctrines/DOC-DISC-012-say-whether-you-are-diverging-or-converging-and-separate-them-in.md) (default)
<a id="D5"></a>
- `D5` to [DOC-DISC-013](doctrines/DOC-DISC-013-prefer-throughput-of-cheap-reversible-tests-over-accuracy-of-ran.md) (default)
<a id="D6"></a>
- `D6` to [DOC-DISC-014](doctrines/DOC-DISC-014-give-a-model-the-structuring-job-on-real-human-input-never-the-o.md) (default)
<a id="D7"></a>
- `D7` to [DOC-DISC-015](doctrines/DOC-DISC-015-reason-about-the-worst-case-of-a-small-sample-not-its-average.md) (default)
<a id="D8"></a>
- `D8` to [DOC-DISC-016](doctrines/DOC-DISC-016-recruit-by-frame-then-by-count.md) (default)
<a id="D9"></a>
- `D9` to [DOC-DISC-017](doctrines/DOC-DISC-017-write-acceptance-criteria-in-ears-clause-order-once-the-problem.md) (default)
- source `preferences:001` to [DOC-DISC-018](doctrines/DOC-DISC-018-the-specific-numbers.md) (preference)
- source `preferences:002` to [DOC-DISC-019](doctrines/DOC-DISC-019-rice-reduced-to-its-confidence-multiplier.md) (preference)
- source `preferences:003` to [DOC-DISC-020](doctrines/DOC-DISC-020-opportunity-solution-trees-as-the-drawing.md) (preference)
- source `preferences:004` to [DOC-DISC-021](doctrines/DOC-DISC-021-double-diamond-vocabulary.md) (preference)
- source `preferences:005` to [DOC-DISC-022](doctrines/DOC-DISC-022-where-the-record-lives.md) (preference)

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
