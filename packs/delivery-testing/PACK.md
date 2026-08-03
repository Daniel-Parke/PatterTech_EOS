---
summary: Delivery, testing and quality: what binds, what defaults, and which fork routes to which guide
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code, has_test_suite]
volatility: slow
review: 2028-02
sources: [EV-0006, EV-0007, EV-0009, EV-0015, EV-0016, EV-0017, EV-0018, EV-0019, EV-0090, EV-0091, EV-0092, EV-0093, EV-0094, EV-0105, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196]
type: guide
tags: [delivery, testing, ci]
review_by: 2028-02
---

# Delivery, testing and quality

This pack covers how a venture proves its code works: which double
stands in for a dependency, where the oracle comes from, when tests get
written, and how flakes and quality numbers are handled. It activates
on any change touching tests, doubles, gates or CI configuration, and
on any FIX, FEAT or REFACTOR in a repo that has a suite. The guides
carry the arguments, the refs carry the mechanics.

## Activation

Triggers, in order of confidence.

- **Paths**: `tests/`, `test/`, `spec/`, any `conftest.py`, files named
  `test_*` or `*_test.*`, any file whose name contains fake, stub, mock
  or double, CI workflow files, and the configuration blocks that hold
  coverage, mutation or retry settings.
- **Task types**: FIX, FEAT and REFACTOR always. Any task the router
  rules R2 or higher, because that tier already demands an independent
  oracle frozen before implementation (`kernel/POLICY_SPEC.md`).
- **Keywords, fallback only**: test, suite, flake, flaky, mock, fake,
  stub, double, contract test, oracle, coverage, mutation, quarantine,
  retry, fixture, snapshot.

Applicability predicates: `ships_code` and `has_test_suite`. Where
`has_test_suite` is false the pack still applies to the change that
creates the first suite, and nothing else here binds until one exists.
DOCS and MAINT tasks carry no behavioural test requirement at all.

Activation never moves a tier. The router rules the tier from declared
facts and derived signals; this pack says what the work must satisfy
once the tier is ruled. Nothing here authorises a guarded action: a
suite that would touch real money movement or production data is a
guarded class under `kernel/GUARD_SPEC.md`, and the answer is a
container or a verified fake, never the live service.

## Outcomes and non-goals

Outcomes worth the money:

- A red result means something is broken, and a green result means the
  behaviour under test still holds.
- Every double that stands in for something real has something proving
  it still matches that real thing.
- A defect that escaped once cannot escape again in silence.
- The cost of the suite is visible and argued, per change class.

Non-goals, stated so nobody optimises for them:

- A coverage percentage, a test count, or a fixed pyramid shape.
- A universal ordering rule for tests and code.
- Assurance about emergent whole-system behaviour. Contract tests check
  recorded interactions, never that the assembled system does its job
  (EV-0091).
- Proof of correctness. A suite raises the cost of being wrong.

## Binding requirements

Six. Each names the failure it prevents. Departing from one needs an
accepted ADR, not a recorded reason.

1. **The oracle is independent of the implementation under test.** The
   check that decides whether the change is correct is derived from the
   specification, the reproduction, an invariant or a reference, never
   read back off the code just written. Basis empirical-evidence,
   grade controlled: tests generated after faulty code detected roughly
   half the faults of tests generated independently, 14% against 25%
   (EV-0007), and coverage and mutation numbers stop being informative
   exactly when the code may already be wrong (EV-0009). Both results
   come from task-level programming problems and LLM suites, so the
   number is theirs and the principle is what carries. Prevents: the
   test learning the bug and then certifying it. See WG-DEL-006.
2. **A check is never weakened to make it pass.** No lowered floor, no
   skip, no deleted assertion, no added retry, no loosened tolerance in
   the change that the check caught. A gate believed wrong is escalated
   with evidence. Basis decision, carried from the v1 delivery doctrine
   and the constitution's three-strikes rule. Prevents: a suite that
   converges on whatever the code already does.
3. **Every double standing in for an external dependency has a contract
   suite that runs the same cases against the double and the real
   implementation, on a stated cadence.** Basis standard, from the
   contract-test practice in EV-0186 and the fidelity requirement in
   EV-0187. Prevents: silent drift, where the fake keeps answering a
   question the real service stopped answering months ago.
4. **Flake is a named state with an owner, never hidden behind
   retries.** Blocking gates run zero retries. A test that cannot be
   made deterministic this week is quarantined out of the blocking path
   with a named owner and an expiry date inside thirty days; an expired
   or unowned quarantine is a finding. Basis standard (EV-0015,
   EV-0195), and see WG-DEL-004 for the argument. Prevents: a green
   build that lies, and a quarantine queue nobody drains.
5. **Any number used as a gate states its threshold, its scope and its
   command.** Coverage percentage is never a universal gate. A mutation
   gate that does not state a number is not a gate: the tool default is
   to report and never fail (EV-0190). Basis decision, with EV-0009 and
   EV-0191 on why the numbers mislead when unqualified. Prevents:
   assertion theatre, and gates nobody set that everybody believes in.
6. **Whatever selection is in force, every test runs against every
   changeset at some point.** A selected subset may gate the merge; the
   remainder runs after it, or a full unselected run happens on a
   stated cadence. Basis standard (EV-0016, EV-0194). Prevents: a test
   that has silently not run for a year.

## Defaults

Overridable in a venture's lock-book with a recorded reason.

- **Double preference order**: real implementation, then a real
  dependency in a throwaway container, then a verified fake with a
  contract suite, then a narrow stub, and interaction mocking last
  (EV-0187, EV-0093). Reason: each step down the ladder buys speed and
  pays in fidelity, and the last step couples the test to how the code
  works. Argued in WG-DEL-005.
- **Test timing by change class**, and this is a default set rather
  than law:

  | Change class | Default timing |
  | --- | --- |
  | FIX | Failing reproduction first, kept forever |
  | FEAT at R2 | Oracle authored and frozen before implementation, same session permitted |
  | FEAT at R3 | Oracle authored by a separate session and frozen |
  | FEAT at R0 or R1 | Oracle from the spec, written before or beside the code, never after it |
  | REFACTOR | Behaviour pinned before structure moves |
  | DOCS, MAINT | No behavioural tests; link, snippet and schema checks only |

  Reason: the load-bearing property is independence, not ordering
  (EV-0007), and mandating more agent-written tests reshapes cost
  rather than quality (EV-0006, scoped to SWE-bench Verified runs). The
  test-timing ablation in P7 sets these cells from evidence per
  capability profile; inconclusive cells keep the conservative value
  above. Neither test-first nor end-stage testing is doctrine here.
  Argued in WG-DEL-007.
- **Mutation testing runs diff-scoped at review time**, with the
  conditional, relational and statement-deletion operators, not
  full-repo per commit (EV-0192, EV-0019, EV-0191). Reason: whole-repo
  runs cost more than they return, and coupling to real faults is
  concentrated in a few operators.
- **Test selection from the diff and the import graph pre-merge, the
  remainder post-merge** (EV-0016, EV-0194). Reason: the cheap version
  gets most of the benefit; a trained model is a scale optimisation.
- **Property tests are seeded and replayable in CI** (EV-0188,
  EV-0017). Reason: an unseeded property test in a blocking gate
  manufactures flake.
- **Contract verification gates deploys for services we own, and
  monitors services we do not** (EV-0193 against EV-0186). Reason: a
  gate you cannot act on is a gate you will learn to ignore.

## Preferences

Taste. Override freely, no reason needed.

- Assert what a user of the interface can see, over internals
  (EV-0092, EV-0090).
- Optimise for confidence per test rather than layer ratios (EV-0094),
  read against the flake cost of bigger tests (EV-0196).
- Where a published schema exists, generate conformance and negative
  cases from it rather than writing examples by hand (EV-0189).
- Keep one assertion idea per test, so a failure names itself.

## Decision map

| Fork | Guide |
| --- | --- |
| Which double stands in for this port | WG-DEL-005 |
| Where the oracle comes from, and who writes it | WG-DEL-006 |
| When tests get written relative to the code | WG-DEL-007 |
| What coverage floor, and how it moves | WG-DEL-001 |
| How much weight the end-to-end layer carries | WG-DEL-002 |
| What visual regression covers | WG-DEL-003 |
| What happens when a test flakes | WG-DEL-004 |

The first three live in `packs/delivery-testing/guides/`. The last four
are the v1 delivery wargames in `archive/v1/doctrine/delivery/wargames/`, carried
forward unchanged and re-graded by this pack's evidence rather than
rewritten. Mechanics that no fork depends on sit in
`packs/delivery-testing/refs/`.

## Failure modes and anti-patterns

- **The unverified hand-rolled fake.** Worse than a mock, because it
  looks trustworthy and drifts quietly (EV-0187, EV-0186).
- **Mocking your own collaborators.** A suite that passes while the
  assembled system is broken (EV-0185).
- **Retry as flake policy.** Teaches everyone that red sometimes means
  run it again (EV-0015, WG-DEL-004).
- **Quarantine as a graveyard.** No owner, no expiry, and a real
  regression sitting in it. Google reported a newly flaky test being a
  genuine production defect roughly one time in six (EV-0195).
- **Coverage as the goal.** Assertion-free tests raise the number and
  detect nothing (EV-0006, EV-0009).
- **Mutation score chased by volume.** Adding tests without adding
  oracles raises the score and proves little (EV-0191).
- **Containers in the inner loop.** Real infrastructure per assertion,
  where the cost buys nothing (EV-0093 read against EV-0196).
- **Unseeded property tests in a blocking gate.** Random red.
- **The test that asserts on the wall clock.** Time is a dependency;
  inject it.

## Open questions and counter-evidence

Named honestly, because the research did not resolve them.

1. **Gate or monitor on contract failure.** EV-0186 says investigate
   and do not break the build; EV-0193 makes the verification matrix a
   hard exit-code deploy gate. The default above routes on ownership,
   which is a judgement call rather than a finding.
2. **Verified fakes against real containers.** EV-0187 prefers fakes
   maintained by the API owner; EV-0093 prefers the real thing in a
   container. They agree only that a hand-written mock is worst. The
   split is partly a resource split: a monorepo can fund fakes that a
   small venture cannot.
3. **Bigger tests buy confidence at a flake rate.** EV-0196 found
   flakiness rising broadly with test size and dependency count across
   roughly 4.2 million tests, while EV-0093 and EV-0094 push work
   towards larger integrated tests. Both are right, and the exchange
   rate is unmeasured here.
4. **Quarantine suppresses signal as well as noise** (EV-0195). The
   thirty-day expiry in requirement 4 is our containment, not a
   validated number.
5. **Mutation testing pays off, but thinly.** EV-0191 found 73% of real
   faults coupled to at least one mutant, and also that the correlation
   weakens once suite size is controlled, with 27% of faults coupled to
   nothing. EV-0192's follow-up reports only about 38% of surfaced
   mutants leading to any change.
6. **The timing evidence is thin.** EV-0006 and EV-0007 are the best we
   have and both come from narrow agentic and task-level benchmarks.
   Nothing here should be read as a general finding about human
   test-first practice. The P7 ablation exists because of this gap.
7. **Selection quality is unmeasured.** EV-0194 publishes no
   missed-failure rate, and EV-0016 admits import-graph selection
   misses runtime coupling. Requirement 6 is the guard against both.
