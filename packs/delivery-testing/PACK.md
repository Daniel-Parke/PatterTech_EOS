---
summary: Activation, outcomes and decision map for the delivery-testing Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [ships_code, has_test_suite]
activation_paths: [**/tests/**, **/test/**, **/*_test.py, **/test_*.py, **/*.test.ts, **/*.spec.ts, **/conftest.py, **/.github/workflows/**, **/*.ci.y*ml, **/fixtures/**, **/e2e/**]
volatility: slow
review: none
sources: [EV-0006, EV-0007, EV-0009, EV-0015, EV-0016, EV-0017, EV-0018, EV-0019, EV-0036, EV-0053, EV-0090, EV-0091, EV-0092, EV-0093, EV-0094, EV-0096, EV-0105, EV-0184, EV-0185, EV-0186, EV-0187, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0193, EV-0194, EV-0195, EV-0196, EV-0480]
type: guide
tags: [delivery, testing, ci]
depends_on: [coding]
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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-COD-001](../coding/doctrines/DOC-COD-001-the-oracle-that-judges-a-change-is-authored-independently-of-the.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-DEL-001](doctrines/DOC-DEL-001-a-check-is-never-weakened-to-make-it-pass.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-DEL-002](doctrines/DOC-DEL-002-every-double-standing-in-for-a-dependency-outside-the-ventures-c.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-DEL-003](doctrines/DOC-DEL-003-flake-is-a-named-state-with-an-owner-never-hidden-behind-retries.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-DEL-004](doctrines/DOC-DEL-004-a-check-named-as-a-gate-can-actually-fail-and-states-its-thresho.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-DEL-005](doctrines/DOC-DEL-005-whatever-selection-is-in-force-every-test-runs-against-every-cha.md) (binding)
- source `defaults:001` to [DOC-DEL-006](doctrines/DOC-DEL-006-double-preference-order.md) (default)
- source `defaults:002` to [DOC-DEL-007](doctrines/DOC-DEL-007-test-timing-by-change-class.md) (default)
- source `defaults:003` to [DOC-DEL-008](doctrines/DOC-DEL-008-verification-staged-by-risk-and-stability.md) (default)
- source `defaults:004` to [DOC-DEL-009](doctrines/DOC-DEL-009-doubles-for-something-inside-the-repository-get-a-contract-suite.md) (default)
- source `defaults:005` to [DOC-DEL-010](doctrines/DOC-DEL-010-a-quarantined-test-expires-in-thirty-days.md) (default)
- source `defaults:006` to [DOC-DEL-011](doctrines/DOC-DEL-011-mutation-testing-runs-diff-scoped-at-review-time.md) (default)
- source `defaults:007` to [DOC-DEL-012](doctrines/DOC-DEL-012-test-selection-from-the-diff-and-the-import-graph-pre-merge-the.md) (default)
- source `defaults:008` to [DOC-DEL-013](doctrines/DOC-DEL-013-property-tests-are-seeded-and-replayable-in-ci.md) (default)
- source `defaults:009` to [DOC-DEL-014](doctrines/DOC-DEL-014-contract-verification-gates-deploys-for-services-we-own-and-moni.md) (default)
- source `preferences:001` to [DOC-DEL-015](doctrines/DOC-DEL-015-assert-what-a-user-of-the-interface-can-see-over-internals-ev-00.md) (preference)
- source `preferences:002` to [DOC-DEL-016](doctrines/DOC-DEL-016-optimise-for-confidence-per-test-rather-than-layer-ratios-ev-009.md) (preference)
- source `preferences:003` to [DOC-DEL-017](doctrines/DOC-DEL-017-where-a-published-schema-exists-generate-conformance-and-negativ.md) (preference)
- source `preferences:004` to [DOC-DEL-018](doctrines/DOC-DEL-018-keep-one-assertion-idea-per-test-so-a-failure-names-itself.md) (preference)

### Later evidence-led admissions

These records were admitted after the frozen source migration.
Their own metadata is canonical; this map does not restate it.

- [WG-DEL-008](guides/WG-DEL-008-incident-hotfix.md) (Wargame)

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
