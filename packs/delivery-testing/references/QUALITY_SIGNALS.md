---
summary: What coverage, mutation score, property tests and test selection actually tell you, and what they cost
kind: fact
scope: estate
sources: [EV-0009, EV-0016, EV-0017, EV-0018, EV-0019, EV-0094, EV-0105, EV-0188, EV-0189, EV-0190, EV-0191, EV-0192, EV-0194]
volatility: fast
review: 2027-03
type: example
tags: [delivery, testing, ci]
---

# Quality signals, and what each one is worth

Reference material for binding requirement 5 and the defaults in the
pack body.

## Coverage

Coverage says which lines ran. It says nothing about whether anything
was checked while they ran. It is a floor mechanism, useful for
catching whole modules nobody exercised, and useless as a target. The
estate's position is a measured floor per surface that only ratchets
upwards, set from the first honest measurement rather than from an
aspiration. A ratchet moves in the change that earned the movement,
never because a number happened to rise.

Two limits worth carrying. Coverage of a suite whose oracle came from
the implementation is informative only while the code is assumed
correct (EV-0009). And past roughly 70% the return per point falls off
for application code, on maintainer experience rather than controlled
evidence (EV-0094). Coverage percentage is never a universal gate in
this estate.

## Mutation score

Mutation score is detected mutants over valid mutants. It measures
whether the suite notices when behaviour changes, which is the thing
coverage cannot see (EV-0018).

The primary evidence: 73% of real faults were coupled to at least one
mutant across 357 real faults in five Java projects, and mutant
detection correlated with real-fault detection independently of
coverage (EV-0191). The same paper carries the caveat: control for
suite size and the correlation weakens, and 27% of real faults coupled
to no mutant at all. A high score bought by adding volume rather than
oracles proves very little. Meta's deployment reports the same
direction, with engineers accepting 73% of mutation-guided generated
tests (EV-0105).

Making it affordable (EV-0192, EV-0019):

- Mutate the diff, not the repository.
- Skip lines with no statement coverage.
- Suppress lines that carry no interesting behaviour.
- Prefer the operators that couple most often: conditional replacement,
  relational replacement, statement deletion (EV-0191).
- Surface a few high-quality mutants in review rather than a score in a
  nightly report. Even then only about 38% of surfaced mutants lead to
  any change (EV-0192).

Gates: the tool reports and never fails until somebody sets a number.
The JavaScript runner defaults its reporting bands to 80 and 60 and its
break threshold to null (EV-0190). Those bands carry no published
justification, so a venture that wants a mutation gate picks and
records its own number and its own scope.

## Property-based testing

Declare the domain of valid inputs and the invariant that must hold,
and let the tool generate, shrink and replay (EV-0017, EV-0188). It
pays wherever a checkable invariant exists: parsers, encoders, money
arithmetic, state machines, round trips.

Two configuration decisions that decide whether it belongs in a
blocking gate:

- **Seeds.** The seed is printed and can be pinned. Unseeded generation
  in a blocking gate manufactures flake; a constant seed trades away
  the exploration that motivates the technique. The usual settlement is
  a pinned seed in the gate and a wider unseeded run on a schedule.
- **Persistence.** A failing case is stored and replayed as a regression
  case, so a property failure becomes an example test forever.

Where a service publishes an OpenAPI or GraphQL schema, the schema is
already a machine-readable property specification, and conformance plus
negative-path cases can be generated from it with a reproducer per
finding (EV-0189). The limit is exact: a wrong-but-well-described API
passes.

## Test selection

Selection is a cost control, never a correctness mechanism.

- The cheap version is a git diff plus the import graph, which is
  built into modern runners and needs no service or history (EV-0016).
- The mature version adds a floor and a settlement run: tests that are
  new, changed, recently failed or recently flaky are always selected
  whatever any model says, a confidence setting trades detection
  against time, the policy is scored on historical builds before anyone
  trusts it, and the unselected remainder runs after merge (EV-0194).
- The machine-learning layer is a scale optimisation. The floor and the
  settlement run are the parts that matter, and both are available
  without a vendor.

Import-graph selection misses runtime coupling through configuration,
environment and generated code (EV-0016), which is why binding
requirement 6 exists.
