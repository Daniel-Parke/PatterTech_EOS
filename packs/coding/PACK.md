---
summary: Activation, outcomes and decision map for the coding Doctrine and Wargames
type: pack
tags: [eos, delivery, testing]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [edits_source, reviews_change, decides_merge]
activation_paths: [**/*.py, **/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.go, **/*.rs, **/*.java, **/*.rb, **/*.c, **/*.cpp, **/*.h, **/pyproject.toml, **/package.json, **/Cargo.toml]
volatility: slow
review: none
sources: [EV-0003, EV-0004, EV-0006, EV-0007, EV-0008, EV-0010, EV-0069, EV-0070, EV-0089, EV-0094, EV-0105, EV-0164, EV-0165, EV-0166, EV-0167, EV-0168, EV-0169, EV-0170, EV-0171, EV-0172, EV-0173, EV-0174, EV-0175, EV-0176, EV-0177, EV-0178, EV-0179, EV-0180, EV-0181, EV-0182, EV-0183, EV-0191, EV-0192, EV-0480]
display_name: Software Construction
category: engineering
id_namespace: COD
depends_on: [architecture]
---


# Software Construction

This pack governs how code is written and accepted inside a venture
repository: where the oracle for a change comes from, how behaviour is
pinned before structure moves, how failures reach callers, and what has
to pass before a change merges. It activates on any task that edits
source, tests or build configuration in a venture repo, and on any
review or merge decision about such a change.

## Activation

Load this pack when any of the following is true.

**Paths touched.** Source files in a venture repo, its test tree, its
build or packaging configuration, or its lint and static-analysis
configuration.

**Task types.** IMPLEMENT, FIX, REFACTOR and CHORE tasks against an
existing codebase. Review and merge decisions on those tasks. Any task
whose acceptance depends on code behaving as it did before.

**Keywords, fallback only.** Refactor, regression, flaky, error
handling, exception, swallow, review, merge, pull request, duplication,
trunk, branch. Keywords are the weakest signal and never override the
predicates below.

**Applicability predicates.**

- `edits_source`: the task will change files the build compiles or the
  interpreter loads.
- `reviews_change`: the task judges someone else's diff, human or agent.
- `decides_merge`: the task moves code onto a shared branch.

Do not load this pack for documentation-only changes, for greenfield
spikes on a throwaway branch that never merges, or for
prompt and configuration edits that touch no compiled or interpreted
source.

## Outcomes and non-goals

**Outcomes.** A change that lands has an executable statement of what
it was meant to do, written somewhere other than the code it judges,
and observed failing at least once. Behaviour that existed before the
change still holds unless the change declared otherwise. Failures reach
the caller in a form the caller can act on. A machine gate has read the
diff. A human has looked where a human being wrong would cost something
real.

**Non-goals.** This pack does not own test strategy depth, coverage
targets or flake policy, which sit in the delivery-testing pack. It
does not own service boundaries or data topology, which sit in the
architecture pack. It does not own threat modelling or secret
handling, which sit in the security-privacy pack. It does not own
agent harness design, which sits in the agentic-development pack. It
does not set a house style: style questions are settled by the
project's style guide and its formatter, never by reviewer taste
(EV-0164).

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-COD-001](doctrines/DOC-COD-001-the-oracle-that-judges-a-change-is-authored-independently-of.md) (binding), [DOC-COD-002](doctrines/DOC-COD-002-a-gate-oracle-is-observed-failing-before-its-green-result.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-COD-003](doctrines/DOC-COD-003-behaviour-is-pinned-before-structure-moves.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-COD-004](doctrines/DOC-COD-004-the-error-path-is-handled-never-discarded.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-COD-005](doctrines/DOC-COD-005-on-a-published-interface-distinguishable-failures-are.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-COD-006](doctrines/DOC-COD-006-a-diff-aware-machine-gate-runs-before-every-merge.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-COD-007](doctrines/DOC-COD-007-human-review-is-scoped-by-risk-not-applied-as-a-blanket.md) (default)
<a id="D2"></a>
- `D2` to [DOC-COD-008](doctrines/DOC-COD-008-review-approves-on-the-health-gradient.md) (default)
<a id="D3"></a>
- `D3` to [DOC-COD-009](doctrines/DOC-COD-009-trunk-based-flow.md) (default)
<a id="D4"></a>
- `D4` to [DOC-COD-010](doctrines/DOC-COD-010-monorepo-per-venture-until-tooling-cost-forces-otherwise.md) (default)
<a id="D5"></a>
- `D5` to [DOC-COD-011](doctrines/DOC-COD-011-refactor-when-a-pending-change-demands-it.md) (default)
<a id="D6"></a>
- `D6` to [DOC-COD-012](doctrines/DOC-COD-012-a-dumb-pipeline-before-a-clever-one.md) (default)
<a id="D7"></a>
- `D7` to [DOC-COD-013](doctrines/DOC-COD-013-write-the-oracle-before-the-implementation-wherever-the.md) (default)
<a id="D8"></a>
- `D8` to [DOC-COD-014](doctrines/DOC-COD-014-cap-the-size-of-a-work-package-and-keep-packages-of-a.md) (default)
<a id="D9"></a>
- `D9` to [DOC-COD-015](doctrines/DOC-COD-015-declare-distinguishable-failures-on-internal-interfaces-too.md) (default)
- source `preferences:001` to [DOC-COD-016](doctrines/DOC-COD-016-conventional-commits.md) (preference)
- source `preferences:002` to [DOC-COD-017](doctrines/DOC-COD-017-naming-beyond-concept-selection.md) (preference)
- source `preferences:003` to [DOC-COD-018](doctrines/DOC-COD-018-duplication-thresholds.md) (preference)
- source `preferences:004` to [DOC-COD-019](doctrines/DOC-COD-019-test-volume.md) (preference)

## What the ordering demotion costs

Until 2026-08-10 B1 required the oracle to be committed before the
implementation was accepted. ADR-0006 dropped that. Test-first was doing
three jobs at once and only one of them was the order, so the other two
are bought back by name rather than quietly lost.

**The free proof that a check can fail.** Red then green demonstrated,
at no cost, that the new test was capable of going red. B1's second
clause buys that back. A seeded fault or a diff-scoped mutation run is
more expensive than watching one test go red, and it is stronger,
because it tests the whole oracle set rather than the one test just
added (EV-0191, EV-0192, EV-0105).

**The enforced cadence of small, even steps.** That, and not the
sequencing, is what carried the measured benefit in the human literature
(EV-0178). A red-green cycle enforced it automatically; a queue of work
packages does not. D8 replaces it with a stated cap, which somebody has
to police.

## Decision map

| Fork | Wargame | Default |
| --- | --- | --- |
| Where does the oracle for this change come from? | `packs/coding/wargames/WG-COD-001-oracle-strategy.md` | From the specification, in a context that never held the implementation |
| Who reviews this change, and how hard? | `packs/coding/wargames/WG-COD-002-review-gate.md` | Machine gate always, human scoped by risk tier |
| How do callers learn that a call failed? | `packs/coding/wargames/WG-COD-003-failure-mode-contract.md` | Declared, versioned failure modes with the cause preserved |
| How do you change code nobody can specify? | `packs/coding/wargames/WG-COD-004-pin-then-change.md` | Pin with a characterisation test, then change |
| One repository or several? | `packs/coding/wargames/WG-COD-005-repo-shape.md` | Monorepo per venture |

Level-three detail: which oracle each change type needs and how
independence is proved, `packs/coding/references/ORACLES.md`; what counts as a
handled error, `packs/coding/references/ERROR_PATH.md`; what the machine gate
contains, `packs/coding/references/REVIEW_GATE.md`. A worked run of the pack
on one defect is
`packs/coding/examples/EX-COD-001-webhook-silent-failure.md`, and what
a reviewer or a script can verify is `packs/coding/CHECKS.md`.

## Failure modes and anti-patterns

- **An oracle read back off the code it judges.** Same author, same
  session, implementation already in context. It encodes the bug. This
  is the single strongest coding finding for agents (EV-0007), and it is
  the failure B1 exists for.
- **A green check nobody has seen go red.** If it has never failed, it
  is an instrument nobody has calibrated. Reverting the change is the
  cheap test; mutation on the diff is the general one (EV-0192).
- **Observational prints presented as tests.** Agent test-writing
  frequency is similar in runs that resolve and runs that do not, and
  the output is mostly prints rather than assertions, so "the agent
  wrote tests" is not evidence that an oracle exists (EV-0006).
- **Approved files treated as a specification.** They lock in current
  behaviour including current bugs, and approvals rot into reflexive
  stamps (EV-0180, EV-0094).
- **A gate that scans the whole repository on every run.** The backlog
  of pre-existing findings drowns the new ones, and the gate gets
  disabled (EV-0070).
- **Contract ceremony on internals.** Schema and version discipline on
  a module with one caller buys rigidity and no coordination.
- **Buying a fix with fresh duplication.** Copying a block to avoid
  touching a shared path is the most common way a small fix degrades
  structure (EV-0179, direction only).
- **Believing you were faster.** Experienced developers were 19 per
  cent slower with early-2025 tooling while believing they were 20 per
  cent faster, so self-reported speed is not evidence of anything
  (EV-0010).
- **Long-lived branches with a code freeze at the end.** Every
  condition of trunk-based flow broken at once (EV-0168).

## Open questions and counter-evidence

**Ordering is not the ingredient, in either population.** For humans,
the active ingredient in test-driven development was granularity and
uniformity of work increments, not whether the test came first (EV-0178,
82 observations, 39 professionals, short greenfield tasks). For agents,
prompting for more tests across the 500 tasks of SWE-bench Verified
moved test-writing behaviour a great deal and the number of tasks
resolved not at all (EV-0006). What the agent evidence isolates is
independence: tests generated after faulty code detect roughly half the
faults of independently generated ones (EV-0007). So B1 binds
independence and demonstrated failure, and D7 keeps ordering as a
default, because writing the oracle first is the cheapest route to
independence rather than a virtue in itself.

Until 2026-08-10 this pack read the same evidence as making sequencing
decisive for agents, and said so here. That was a misreading and
ADR-0006 corrects it. The strongest measurement of the contamination
itself is EV-0480: prompted with the buggy implementation, eleven
frontier models produced 104.15 bug-revealing tests on average, against
304.08 prompted with the correct implementation, and 186.77 when the
code was replaced by a specification. Read in both directions, seeing
the wrong code costs about two thirds of the suite's bug-finding power
against seeing the right code, and about 44 per cent against seeing the
specification. That row's licence was recorded from a research packet
rather than read at the source, so it carries no observation date.

**Is machine-assisted coding degrading codebases.** One vendor study of
623 million changes reports refactoring down about 70 per cent,
duplication up about 81 per cent and error-masking constructs up about
47 per cent (EV-0179). It is vendor-run, non-random, with its method
behind a form and causal attribution inferred from timing. The 2025
DORA survey finds delivery outcomes flat rather than worse (EV-0169).
Structural decay is plausible and unproven. The pack instruments the
direction and refuses to bind on the magnitudes.

**Whether human review still pays at all.** The explicit argument that
agents supersede human inspection is a preprint with no new data
(EV-0167). Its concessions are the usable part: hallucinated approvals,
unsolved prompt injection, weak architectural judgement, and the
accountability gap. D1 takes the concessions seriously and refuses the
headline. If a peer-reviewed replacement arrives, D1 is the first thing
to re-argue.

**The review evidence base is old and narrow.** The best case study of
review at scale predates machine authorship entirely (EV-0165), and its
source guidance is now an archived read-only repository (EV-0164). The
health-gradient rule transfers; the ownership and readability machinery
does not.

**Benchmark numbers are population-bound.** The 94.3 per cent figure
for a test-driven agent workflow was reached on SWE-bench Verified with
human-written tests supplied (EV-0004). It says that resolving given
tests is nearly solved. It says nothing about writing the tests, or
about arbitrary production diffs.

**Practice corpora ossify.** A long-lived practice corpus encodes
assumptions about what models cannot do, and scaffolding should be
stripped as models improve (EV-0089 via EV-0182). This pack is due for
that treatment at its review date.

**Refresh triggers.** Re-argue this pack on: a successor to or
un-archive of the source behind EV-0164; a peer-reviewed replacement
for EV-0167; the next annual DORA report; an independent replication of
the EV-0179 structural metrics; a current-model replication of the
EV-0181 scenario battery.

## Evidence pointer

Every source is a row in `registry/evidence.json` carrying version or
commit, licence, access date, applicability limits and a review
trigger. Cite ids, never re-record sources. The rows from this pack's
own sweep were imported as EV-0164 to EV-0183, and the frozen batch
they came from stays at `packs/coding/research/sources.fragment.json`.
The rest are estate rows this pack borrows, chiefly the agent-run
results (EV-0003 to EV-0008), the productivity trial (EV-0010), the
gate tooling (EV-0069, EV-0070) and the mutation rows the
delivery-testing pack owns (EV-0191, EV-0192, EV-0105). The synthesis
and the disagreements behind this file are in
`packs/coding/research/NOTES.md`, and the licence and quotation sweep
is at `packs/coding/research/provenance.fragment.json`. That sweep
confirmed no licence: 29 of the 40 ids this pack cites carry no
licence evidence, which is a number to work down rather than a defect
in the prose.
