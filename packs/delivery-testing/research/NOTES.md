---
summary: Research synthesis for the delivery, testing and quality pack, covering test doubles, mutation practice, property-based testing, contract maturity, flake policy and test selection
type: example
tags: [eos]
---

# Delivery, testing and quality: research synthesis

Cutoff 2026-08-03. Thirteen new sources in `sources.fragment.json`, plus
the existing ledger rows cited inline. The pack authors WG-DEL-005,
WG-DEL-006 and WG-DEL-007.

## The one thing the evidence agrees on

Tests are only worth what their oracle is worth. EV-0006 finds agent
test volume is uncorrelated with task success because most agent tests
are prints rather than assertions. EV-0007 finds tests written after
faulty code detect roughly half the faults of tests written
independently, because the test learns the bug. EV-0009 finds coverage
and mutation numbers are informative when the code is assumed correct
and unreliable when it may already be wrong. FRAG-08 finds mutation
score correlates with real fault detection independently of coverage,
but that the correlation goes weak once suite size is controlled. Every
one of these says the same thing from a different angle: quantity
signals are gameable, independence of the check from the thing checked
is what actually buys detection.

## Pattern one: test doubles by preference order

The Google position (FRAG-04) is a strict ladder. Real implementation
when it is fast, deterministic and simply wired. Otherwise a fake, which
must hold fidelity to the API contract so the same input gives the same
output and the same state change. Otherwise narrow stubbing to force a
state. Interaction testing last, because it exposes implementation
detail. The fake belongs to the team that owns the real thing, and one
identical contract suite runs against both, which is exactly the
mechanism Fowler names in FRAG-03.

Fits when the dependency is yours or has a maintained fake, and when the
suite must stay fast enough to run per commit. Trade-off: a verified
fake is a second implementation to maintain, and the contract suite is a
third artefact. Anti-pattern: an unverified hand-rolled fake, which is
strictly worse than a mock because it looks trustworthy and drifts
silently.

## Pattern two: real dependencies, no doubles

Testcontainers (EV-0093) argues the opposite default for infrastructure:
run the real database in a throwaway container, because any fake behaves
slightly differently and shared environments drift. Playwright best
practice (EV-0090) splits the difference, using real code paths but
mocking third parties at the network layer.

Fits for datastores, brokers and anything with dialect-level behaviour a
fake cannot reproduce. Trade-off: Docker everywhere, slower runs, and no
faithful emulation of managed cloud services. Anti-pattern: containers
in the inner loop of a unit suite, where the cost per assertion buys
nothing.

## Pattern three: mockist, expectation-driven

FRAG-02 sets out the fork honestly. Behaviour verification asserts on
calls made, which couples the test to how the unit works, so internal
refactoring breaks tests that ought to pass. The mockist reply, which
Fowler records without refuting, is that expectations drive interface
discovery and localise failures precisely.

Fits at genuine trust boundaries where the call itself is the observable
behaviour, for example that a payment was captured exactly once. Trade-
off: brittle under refactor. Anti-pattern: mocking your own internal
collaborators, which produces a suite that passes while the system is
broken.

## Disagreements worth carrying, not resolving

1. Fowler (FRAG-03) says a contract failure triggers investigation and
   should not break the build. Pact (FRAG-10, EV-0091) makes the
   verification matrix a hard deploy gate with an exit code. Both are
   defensible: the difference is whether the contract is a monitor of a
   third party you cannot fix, or a release check on services you own.
   The pack should route on ownership, not pick a winner.
2. Google (FRAG-04) prefers verified fakes; Testcontainers (EV-0093)
   prefers the real thing; they agree only that a hand-written mock is
   worst. The split is a resource split, since Google can fund fakes
   that a small venture cannot.
3. FRAG-13 finds flakiness rises with test size and dependency count,
   while EV-0093 and EV-0094 push work towards larger integrated tests
   for confidence. Confidence is bought at a flake rate. Say so.
4. Quarantine (FRAG-12) suppresses noise but also suppresses signal: the
   same source reports a previously stable test turning flaky was a real
   production defect roughly one time in six.
5. FRAG-11 sells a trained model for test selection; EV-0016 gets most
   of the benefit from a git diff and an import graph. Machine learning
   here is a scale optimisation, not a requirement.

## Mutation testing, as practice rather than a score

FRAG-08 is the load-bearing primary evidence: 73% of real faults coupled
to at least one mutant, correlation with real fault detection holding
independently of coverage, conditional and relational replacement and
statement deletion coupling most often. It also carries its own limit,
27% of faults coupled to nothing and a weak correlation once size is
controlled. FRAG-09 shows how it becomes affordable: mutate the diff
only, skip uncovered lines, suppress arid lines, filter by context, and
surface a few mutants in review rather than a score in a report. Even
then only about 38% of surfaced mutants lead to a change. EV-0105 is the
industrial echo at Meta, EV-0018 and EV-0019 the tool mechanics, and
FRAG-07 shows the gate is opt-in: `break` defaults to null, so Stryker
reports forever unless someone sets a number.

Decision rule: mutation testing belongs on changed code, at review time,
with an operator subset, and its gate number is a pack decision that no
tool ships for you.

## Property-based testing

EV-0017 covers Hypothesis. FRAG-05 shows the same three affordances in
the JavaScript stack, generation, shrinking and seeded replay, with
determinism as a configuration choice. FRAG-06 goes further: an OpenAPI
or GraphQL schema is already a machine-readable property specification,
so conformance and negative-path testing can be generated rather than
written, with a curl reproducer per finding.

Fits wherever a checkable invariant exists: parsers, encoders, money
arithmetic, state machines, and any interface with a published schema.
Anti-pattern: property tests over CRUD with no invariant, and unseeded
properties in a blocking pipeline, which manufacture flake.

## What the pack should bind, default and prefer

Binding requirements, machine-checkable and refusable:

- Every fake or stub standing in for an external dependency has a
  contract suite that runs the same cases against the double and the
  real implementation, on a named cadence (FRAG-03, FRAG-04).
- Flake is a first-class reported state, never hidden by blanket retries
  (EV-0015, FRAG-12). Quarantine requires a named owner and an expiry.
- Tests for a change are written independently of the implementation
  under test, not derived from it after the fact (EV-0007).
- A full unselected run happens on a stated cadence whatever selection
  is in force (EV-0016, FRAG-11).
- Any mutation gate states its threshold explicitly, because the tool
  default is no gate at all (FRAG-07).

Defaults, overridable with a recorded reason:

- Double preference order: real, then verified fake, then stub, then
  mock (FRAG-04), with containers as the real option for infrastructure
  (EV-0093).
- Mutation testing runs diff-scoped at review time, not per commit
  full-repo (FRAG-09, EV-0019).
- Selection by import graph or diff pre-merge, remainder post-merge
  (EV-0016, FRAG-11).
- Property tests seeded and replayable in CI (FRAG-05, EV-0017).

Preferences, stated and not enforced:

- Assert user-visible behaviour over internals (EV-0092, EV-0090).
- Contract gates on services we own, contract monitors on services we do
  not (FRAG-03 versus FRAG-10).
- Confidence per test over layer ratios (EV-0094), read against the
  flake cost in FRAG-13.

## Licence care

FRAG-04 is CC BY-NC-ND 4.0, so paraphrase only, no adapted excerpts. The
three Fowler pages and both Google Testing Blog posts carry no reuse
licence, so principles may be extracted but text may not be lifted.
FRAG-11 documents a proprietary commercial product, so it informs the
shape of a rule and must never be a dependency.
