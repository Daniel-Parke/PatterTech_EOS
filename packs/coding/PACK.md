---
summary: How code is written and accepted in a venture repo, oracles, pinning, error paths and the merge gate
type: playbook
tags: [eos, delivery, testing]
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source, reviews_change, decides_merge]
activation_paths: [**/*.py, **/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.go, **/*.rs, **/*.java, **/*.rb, **/*.c, **/*.cpp, **/*.h, **/pyproject.toml, **/package.json, **/Cargo.toml]
volatility: slow
review: 2027-02
sources: [EV-0003, EV-0004, EV-0006, EV-0007, EV-0008, EV-0010, EV-0069, EV-0070, EV-0089, EV-0094, EV-0164, EV-0165, EV-0166, EV-0167, EV-0168, EV-0169, EV-0170, EV-0171, EV-0172, EV-0173, EV-0174, EV-0175, EV-0176, EV-0177, EV-0178, EV-0179, EV-0180, EV-0181, EV-0182, EV-0183]
---

# Coding pack

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
spikes on a throwaway branch that the checker refuses to merge, or for
prompt and configuration edits that touch no compiled or interpreted
source.

## Outcomes and non-goals

**Outcomes.** A change that lands has an executable statement of what
it was meant to do, written before it was accepted. Behaviour that
existed before the change still holds unless the change declared
otherwise. Failures reach the caller in a form the caller can act on.
A machine gate has read the diff. A human has looked where a human
being wrong would cost something real.

**Non-goals.** This pack does not own test strategy depth, coverage
targets or flake policy, which sit in the delivery-testing pack. It
does not own service boundaries or data topology, which sit in the
architecture pack. It does not own threat modelling or secret
handling, which sit in the security-privacy pack. It does not own
agent harness design, which sits in the agentic-development pack. It
does not set a house style: style questions are settled by the
project's style guide and its formatter, never by reviewer taste
(EV-0164).

## Binding requirements

Five requirements bind. A run that breaks one fails, whatever else it
achieved.

**B1. An oracle exists before the implementation is accepted.** Every
change carries an executable statement of intent appropriate to its
type, and that statement is authored and committed before the
implementation is accepted. A FIX starts from a failing reproduction.
Prevents the mutual-consistency failure: tests generated after faulty
code agree with the fault and roughly halve fault detection (EV-0007),
while surfacing the right test context cut regressions from 6.08 to
1.82 per cent (EV-0003). Scope note: those numbers are agent runs on
SWE-bench Verified, not a claim about human developers or about all
code. See `packs/coding/guides/GD-COD-001-oracle-strategy.md`.

**B2. Behaviour is pinned before structure moves.** No refactor of code
whose specification is missing or untrusted begins until a
characterisation or approval test captures current behaviour. Prevents
the silent behaviour change sold as a tidy-up, which is the failure
mode inherited and agent-written code both carry, because nobody can
say what the code was supposed to do (EV-0180, EV-0177). See
`packs/coding/guides/GD-COD-004-pin-then-change.md`.

**B3. The error path is handled, never discarded.** A bare catch-all, a
catch that swallows and continues, or a handler that logs and drops a
signalled failure is rejected. Every caught error is either handled,
translated into a declared failure, or re-raised. Prevents the failure
class that dominates production catastrophe: 92 per cent of the
catastrophic failures studied came from mishandling errors the software
had already signalled, and about a third were visible to plain
inspection (EV-0174). Scope note: that corpus was Java-heavy
distributed data systems in 2014, so the direction of attention
transfers and the exact proportion does not. See
`packs/coding/refs/ERROR_PATH.md`.

**B4. Distinguishable failures are declared and versioned.** The set of
failures a caller may tell apart is named in the interface
documentation, and it changes only with a version bump on that
interface. Wrapping an error makes that error part of the contract
(EV-0175); version numbers mean nothing until the public surface is
declared precisely (EV-0171). Prevents callers writing recovery against
a failure mode that quietly disappears in a patch release. See
`packs/coding/guides/GD-COD-003-failure-mode-contract.md`.

**B5. A diff-aware machine gate runs before every merge.** Security and
policy rules run against the diff, not the whole repository, and
blocking findings are separated from monitoring findings (EV-0070).
Repository health checks read the repo's actual state (EV-0069).
Prevents shipping generated code on trust: roughly 40 per cent of
generated programs in security-relevant scenarios contained a
vulnerability, and the rate varied with prompt and domain in ways the
author cannot see (EV-0181). Scope note: that was a 2021 model on
deliberately security-loaded prompts. The finding that survives is the
necessity of a gate, not the size of the number. Whole-repo-only gates
are themselves an anti-pattern: they produce alert fatigue and then get
turned off. See `packs/coding/refs/REVIEW_GATE.md`.

Guarded actions are outside review entirely. Deployment, deletion,
force-push, secret access, money movement and the rest are ruled by
`kernel/GUARD_SPEC.md` and its non-waivable floors. No review verdict,
machine or human, changes a guard verdict.

## Defaults

Each default applies unless the venture's lock-book overrides it with a
recorded reason.

**D1. Human review is scoped by risk, not applied as a blanket.** The
machine gate in B5 runs on everything. Human review is routed by the
tier that `kernel/POLICY_SPEC.md` rules for the task: R0 and R1 take
agent review plus sampled human review, R2 takes independent review at
acceptance, R3 always takes a human. Reason: review's measured product
is knowledge transfer and awareness rather than defect finding
(EV-0166), and a solo operator directing agents collects almost none of
that transfer, so blanket review buys ceremony. The reason a human
stays in the loop on high-risk changes is not defect yield, it is the
accountability gap: when an auto-approved change causes harm, no agent
is answerable for it, and that gap is named as unsolved by the strongest
argument for agent-led review (EV-0167), which is a preprint with no new
data and should be read as a hypothesis. Override by recording which
tier you moved and why. See
`packs/coding/guides/GD-COD-002-review-gate.md`.

**D2. Review approves on the health gradient.** Approve once the change
definitely improves overall code health even when it is imperfect, and
refuse only what definitely worsens it. One reviewer, one iteration,
small changes (EV-0164, EV-0165). Reason: the practice that makes
review affordable is keeping changes small, and the alternative bar of
perfection stalls the queue. Scope note: EV-0165 describes one company
with bespoke tooling and predates machine authorship.

**D3. Trunk-based flow.** Small changes merged to trunk at least daily,
branch lifetime measured in hours, three or fewer active branches, no
code freezes (EV-0168). Large changes ride behind feature flags or
branch by abstraction rather than a long branch (EV-0183). Reason: the
conditions are measurable and the association with delivery performance
is the best evidence available. Both sources are association or opinion
rather than causal evidence, and for a one-person venture the residue
that matters is merge cadence and the ban on freezes.

**D4. Monorepo per venture until tooling cost forces otherwise.** A
small repository gets the monorepo benefits free, because it is small
(EV-0172, EV-0173). Reason: the benefits at scale are bought with
bespoke tooling nobody at venture scale can fund, and the pain sits in
the middle sizes. Override when a component has its own release train
or its own consumers. See
`packs/coding/guides/GD-COD-005-repo-shape.md`.

**D5. Refactor when a pending change demands it.** Refactoring is
change-driven, not smell-driven: developers refactor to make a specific
pending change possible, and a smell-detector backlog is a poor model
of the work (EV-0177). Reason: backlog-driven tidying spends the budget
where no change is coming. Override for a documented decay signal you
have measured in your own repository.

**D6. A dumb pipeline before a clever one.** Prefer a fixed
localise-repair-validate loop over autonomous sophistication until the
simple pipeline is shown to fail; a fixed pipeline matched contemporary
agents at far lower cost (EV-0008). Reason: cost and reproducibility.

## Preferences

These are taste. Record them, do not gate on them, and override them
without asking.

- **Conventional Commits**, and only where release automation actually
  consumes the grammar. As decoration it is ceremony. With agent
  authors, normalise the message at merge rather than expecting every
  commit to comply, which the specification itself suggests (EV-0170).
- **Naming beyond concept selection.** Do not enforce naming
  uniformity. Two developers pick the same name about 7 per cent of the
  time, yet a chosen name is usually understood (EV-0176). Review which
  concepts a name encodes; leave the wording alone.
- **Duplication thresholds.** Instrument the direction in your own
  repository if you care. The published magnitudes of AI-era structural
  decay come from a vendor study with a non-random sample and causal
  attribution by timing, so treat them as a hypothesis worth measuring,
  never as fact (EV-0179).
- **Test volume.** Optimise for confidence per test rather than layer
  ratios (EV-0094). The delivery-testing pack owns this properly.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| Where does the oracle for this change come from? | `packs/coding/guides/GD-COD-001-oracle-strategy.md` | Test-first wherever an acceptance condition can be stated |
| Who reviews this change, and how hard? | `packs/coding/guides/GD-COD-002-review-gate.md` | Machine gate always, human scoped by risk tier |
| How do callers learn that a call failed? | `packs/coding/guides/GD-COD-003-failure-mode-contract.md` | Declared, versioned failure modes with the cause preserved |
| How do you change code nobody can specify? | `packs/coding/guides/GD-COD-004-pin-then-change.md` | Pin with a characterisation test, then change |
| One repository or several? | `packs/coding/guides/GD-COD-005-repo-shape.md` | Monorepo per venture |

## Failure modes and anti-patterns

- **Tests written after the code, by the same author, in the same
  session.** They encode the bug. This is the single strongest coding
  finding for agents (EV-0007).
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

**Sequencing evidence does not transfer between humans and agents.**
For humans, the active ingredient in test-driven development was
granularity and uniformity of work increments, not whether the test came
first (EV-0178, 82 observations, 39 professionals, short greenfield
tasks). For agents, sequencing is decisive because the test is the only
reliable oracle (EV-0003, EV-0004, EV-0007). Never cite the human
literature as evidence about agent practice, or the reverse. B1 rests on
the agent evidence and on regression protection, not on the human TDD
folklore.

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
