---
summary: Delivery, testing and quality: what binds, what defaults, and which fork routes to which guide
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code, has_test_suite]
activation_paths: [**/tests/**, **/test/**, **/*_test.py, **/test_*.py, **/*.test.ts, **/*.spec.ts, **/conftest.py, **/.github/workflows/**, **/*.ci.y*ml, **/fixtures/**, **/e2e/**]
volatility: slow
review: 2028-02
sources: [EV-0006, EV-0007, EV-0009, EV-0015, EV-0016, EV-0017, EV-0018, EV-0019, EV-0036, EV-0053, EV-0090, EV-0091, EV-0092, EV-0093, EV-0094, EV-0096, EV-0105, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196, EV-0480]
type: guide
tags: [delivery, testing, ci]
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
- A completeness percentage as the trigger for anything. Nothing in
  this pack fires when a project is 90 per cent done, because nothing
  we could find gates rigour that way.
- A universal ordering rule for tests and code.
- Assurance about emergent whole-system behaviour. Contract tests check
  recorded interactions, never that the assembled system does its job
  (EV-0091).
- Proof of correctness. A suite raises the cost of being wrong.

## Binding requirements

Six. Each names the failure it prevents. Departing from one needs an
accepted ADR, not a recorded reason.

All six were re-tested on 2026-08-10 against ADR-0008: a rule binds only
where it prevents a serious or hard-to-reverse failure and its basis is
law, a standard or measured evidence. One was narrowed, one was
restated, one number moved into the defaults, and the reason sits with
the rule in each case.

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
   test learning the bug and then certifying it. This says nothing about
   when the check is written; ordering is a default and lives in
   WG-DEL-007. See WG-DEL-006.
2. **A check is never weakened to make it pass.** No lowered floor, no
   skip, no deleted assertion, no added retry, no loosened tolerance in
   the change that the check caught. A gate believed wrong is escalated
   with evidence. Basis law: this is an article of the venture
   constitution in `kernel/templates/org/CONSTITUTION.tpl.md`, not a
   preference carried forward from v1, which is how it survives the
   authority audit unchanged. Prevents: a suite that converges on
   whatever the code already does.
3. **Every double standing in for a dependency outside the venture's
   control has a contract suite that runs the same cases against the
   double and the real implementation, on a stated cadence.** Outside
   the venture's control means a third-party API, a payment provider, a
   service another team ships. Basis standard, from the contract-test
   practice in EV-0186 and the fidelity requirement in EV-0187.
   Prevents: silent drift, where the fake keeps answering a question the
   real service stopped answering months ago, which nobody sees until
   production. Doubles for something inside the repository are a default
   below, because there the real thing is available and the drift shows
   up at the next integration rather than at a customer.
4. **Flake is a named state with an owner, never hidden behind
   retries.** Blocking gates run zero retries. A test that cannot be
   made deterministic this week is quarantined out of the blocking path
   with a named owner; an unowned quarantine is a finding. Basis
   standard (EV-0015, EV-0195); the mechanics are in
   `packs/delivery-testing/refs/FLAKE_AND_DETERMINISM.md`.
   Prevents: a green build that lies, and a quarantine queue nobody
   drains. The thirty-day expiry that used to sit inside this rule is
   now a default, because open question 4 below admits the number is our
   containment rather than a validated one, and a number we cannot
   defend should not need an ADR to move.
5. **A check named as a gate can actually fail, and states its
   threshold, its scope and its command.** A gate that cannot go red is
   documentation. A mutation gate with no number is the standard
   example: the tool default is to report and never fail (EV-0190).
   Coverage percentage is never a universal gate. Basis standard
   (EV-0190) with empirical support for why unqualified numbers mislead
   (EV-0009, EV-0191). Prevents: assurance that does not exist and that
   everybody believes in, which is the same failure whether it comes
   from a threshold nobody set or from a checklist nothing runs.
6. **Whatever selection is in force, every test runs against every
   changeset at some point.** A selected subset may gate the merge; the
   remainder runs after it, or a full unselected run happens on a
   stated cadence. Basis standard (EV-0016, EV-0194). Prevents: a test
   that has silently not run for a year.

The strongest available measurement behind requirement 1 is EV-0480.
Prompted with the buggy implementation, eleven frontier models produced
104.15 bug-revealing tests on average, against 304.08 prompted with the
correct implementation and 186.77 when the code was swapped for a
specification. So a contaminated context does not just bless the bug, it
suppresses the tests that would have caught anything. That row's licence
was recorded from a research packet rather than read at the source, so
it carries no observation date.

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
  | Invariants, money, security, personal data, irreversible operations, public contracts | Acceptance authored independently and frozen before implementation, at any tier |
  | FEAT at R2 | Oracle from the specification, frozen before implementation, same session permitted |
  | FEAT at R3 | Oracle authored by a separate session and frozen |
  | FEAT at R0 or R1 | Oracle from the spec, written before or beside the code, never read off it |
  | REFACTOR | Behaviour pinned before structure moves |
  | DOCS, MAINT | No behavioural tests; link, snippet and schema checks only |

  Reason: the load-bearing property is independence, not ordering
  (EV-0007), and mandating more agent-written tests reshapes cost
  rather than quality (EV-0006, scoped to SWE-bench Verified runs). The
  timing ablation ran on 2026-08-03 and settled the cells: all three
  timings passed six of six on three tasks, so timing did not separate
  quality on that work, while implement-then-harden cost about 65 per
  cent more tokens and 50 per cent more wall clock than the other two.
  The results are in `org/reports/V2_FINAL_REPORT.md`. Where a policy
  sets `test_timing` to `per-profile`, this table is what that resolves
  to; the capability-profile record decides the level, its expiry and
  what regresses it, and nothing else. Ours is
  `org/capability-profile.json`. So the cells stand on cost rather than
  on fault-finding, every arm passed, and nothing here says which timing
  catches more faults. Neither test-first nor end-stage testing is
  doctrine. The second row is unchanged by any of that, because it is a
  risk floor rather than a timing preference. Argued in WG-DEL-007.
- **Verification staged by risk and stability**, and this is a default
  set, not law. The floors are the law; the staging is argued. Stages,
  in the order they switch on:

  | Stage | What runs | Switched on by |
  | --- | --- | --- |
  | Risk floors | The acceptance-first row above, plus the guard's runtime floors | Day one, unconditionally |
  | Cheap executable checks | Build, types, lint, schema, smoke | Day one, before the first feature lane opens |
  | Contract tests | The boundary's cases, blocking for its neighbours | The moment that interface is declared stable |
  | Comprehensive harness | Regression breadth, derived from the map and the specifications | When the stability signals below fire |
  | Deletion | Tests that only protect retired structure | The same change that retires the structure |

  Executable is the operative word in the second row. A cheap tier that
  is a list in a document and not a command that exits non-zero buys
  nothing, and requirement 5 is the version of that with teeth.

  The harness is derived from the map and the specifications rather than
  from the code, authored or reviewed independently of the implementing
  agent, and mutation-checked before it blocks anything (EV-0191,
  EV-0192, EV-0105). Default stability signals, and these are starting
  values a venture overrides in its lock-book rather than measured
  thresholds: all journeys green on the acceptance spine, three
  consecutive integrations with no interface churn, and a flat trend in
  open defects over the same window.

  No percentage gates the harness. We found no standard, study or mature
  practice that gates rigour on a completeness figure: the precedents
  gate on consequence class and on measured behaviour, which is what an
  error budget does (EV-0096) and what per-practice maturity does
  (EV-0036). While the harness is deferred, name the deferral at the
  venture's regular review, because deferred breadth is a loan and
  nobody sees the interest until it is due. Reason for the whole staging
  being a default: tests attached to churning internals are rewritten
  with the churn, so deferring breadth is argued rather than proved, and
  the claim that deferral reduces waste without raising escaped defects
  is a hypothesis ADR-0006 labels as one.
- **Doubles for something inside the repository get a contract suite
  where the boundary crosses a lane or has a second consumer**, and a
  plain assertion otherwise. Reason: inside the repository the real
  implementation is available and drift surfaces at the next
  integration, so the full contract-suite cadence in requirement 3 is
  cost without the failure it prevents.
- **A quarantined test expires in thirty days.** An expired quarantine
  is a finding. Reason: containment has to end somewhere or the
  quarantine becomes the graveyard in the anti-pattern list. Thirty days
  is our number and not a measured one, which is why it is here and not
  in requirement 4. Override with a recorded reason and a date.
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
| Which double stands in for this port | `packs/delivery-testing/guides/WG-DEL-005-test-doubles.md` |
| Where the oracle comes from, and who writes it | `packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md` |
| What has to exist before work fans out, and when checks get written | `packs/delivery-testing/guides/WG-DEL-007-test-timing.md` |

Four more forks used to sit in this table, pointing at v1 wargames that
are not in the tree. Three are answered here instead: the coverage
floor is requirement 5, a floor per surface and never a universal gate;
layer weighting is the preference above, confidence per test rather
than a ratio; flake is requirement 4. Visual regression scope is
answered by no pack in this estate, so a venture that needs it decides
the scope and records it in its lock-book.

Mechanics: building and running a contract suite in
`packs/delivery-testing/refs/CONTRACT_SUITES.md`, flake sources and the
quarantine record in
`packs/delivery-testing/refs/FLAKE_AND_DETERMINISM.md`, and what
coverage, mutation score, property tests and selection are each worth
in `packs/delivery-testing/refs/QUALITY_SIGNALS.md`. A worked run is
`packs/delivery-testing/exemplars/EX-DEL-001-drifted-fake-and-a-lying-suite.md`.

## Failure modes and anti-patterns

- **The unverified hand-rolled fake.** Worse than a mock, because it
  looks trustworthy and drifts quietly (EV-0187, EV-0186).
- **Mocking your own collaborators.** A suite that passes while the
  assembled system is broken (EV-0185).
- **Retry as flake policy.** Teaches everyone that red sometimes means
  run it again (EV-0015).
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
6. **The timing evidence is thin, and our own ablation did not thicken
   it.** EV-0006 and EV-0007 are the best published results we have and
   both come from narrow agentic and task-level benchmarks. Nothing here
   should be read as a general finding about human test-first practice.
   Our own eighteen-run ablation on 2026-08-03 had every arm pass six of
   six, so it ranked cost and told us nothing about faults. The cells
   above rest on cost and on independence, and the fault question is
   still open.
7. **Staging by stability is argued, not measured.** No controlled
   comparison of building the comprehensive harness early against
   building it on stability signals exists that we could find. The
   signals in the default set are starting values chosen by us. The
   carrying cost of deferral is real, which is why the staging default
   asks for the deferral to be named at review rather than left silent
   until the signals fire.
8. **Selection quality is unmeasured.** EV-0194 publishes no
   missed-failure rate, and EV-0016 admits import-graph selection
   misses runtime coupling. Requirement 6 is the guard against both.

## Evidence pointer

Every source is a row in `registry/evidence.json` carrying version or
commit, licence, access date, applicability limits and a review
trigger. Cite ids, never re-record sources. The rows from this pack's
own sweep were imported as EV-0184 to EV-0196, and the frozen batch
they came from stays at
`packs/delivery-testing/research/sources.fragment.json`. The rest are
estate rows this pack borrows, chiefly the agent test-generation
results (EV-0006, EV-0007), the flake and selection rows (EV-0015,
EV-0016), the mutation rows (EV-0018, EV-0019, EV-0105) and the
contamination measurement (EV-0480). The synthesis is in
`packs/delivery-testing/research/NOTES.md`, and the licence and
quotation sweep is at
`packs/delivery-testing/research/provenance.fragment.json`. That sweep
confirmed no licence: 17 of the 33 ids this pack cites carry no licence
evidence, three sources are recorded all rights reserved and two
no-derivatives, and none of the five is quoted anywhere in the pack.
