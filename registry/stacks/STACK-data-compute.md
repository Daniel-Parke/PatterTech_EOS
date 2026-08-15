---
summary: Dated Python profile for local tabular, analytical SQL and dense-array work
type: stack
tags: [data, tooling]
status: active
review: 2026-11
sources: [EV-0566, EV-0567, EV-0568, EV-0569, EV-0570, EV-0571, EV-0572, EV-0573, EV-0574]
---

# Stack profile: local data compute

This is a dated starting point, not timeless Doctrine. It applies to new
single-machine Python work where the input is tabular or a dense numerical
array. Existing products keep their working ecosystem until a representative
probe shows that moving it buys enough to cover the semantic and migration
cost.

## Safe starting point

- Use Polars for suitable new columnar transformations, especially when a
  lazy plan can push work down and the product does not depend on a pandas
  index or a pandas-only library.
- Keep pandas where index semantics, an established extension, or an external
  interface is part of the contract.
- Cross into NumPy for dense arrays, solver interfaces and numerical kernels.
  Record dtype, layout, ownership, device, copies and numerical tolerance at
  that boundary.
- Consider Numba only after a profiler identifies a numerical hotspot. Measure
  compilation-inclusive first use and steady use separately against the same
  result oracle.
- Use DuckDB when local analytical SQL, joins, grouping or controlled spill is
  the clearer execution model. Do not treat it as a transactional service
  database by implication.
- Reach for Spark or another distributed engine only after representative
  evidence shows that the single-machine and out-of-core routes miss the
  stated capacity, latency or recovery objective.

## Interoperability boundaries

A dataframe-to-array or engine-to-engine move is an architectural boundary
once its copies, dtype conversion or ordering can affect correctness or peak
memory. A ruling records those facts rather than describing the move as a
mere optimisation. A pandas index is exported as a named column when it must
survive. Ordering is declared before comparing result hashes. Numerical
outputs use a stated tolerance unless byte identity is itself the contract.

## Versions actually exercised

The local probe on 2026-08-15 used Python 3.14.4 on Windows 11 with Polars
1.40.1, pandas 3.0.2, NumPy 2.4.4, Numba 0.65.1 and DuckDB 1.5.5. The two
scripts and their machine-readable receipt live under
`registry/stacks/probes/`. The tabular probe preserved an index explicitly and
matched Polars and DuckDB aggregates within tolerance. The acceleration probe
matched NumPy and Numba results while separating compilation from steady use.

These are executable compatibility observations, not a claim that one tool is
faster. Spark 4.2.0 was studied from its official documentation but was not
installed or exercised in this probe, so it is an untested distributed option.

## Review and departure

Re-run the relevant probe when a named package changes major version, the
target hardware or device changes, a solver boundary is introduced, a pandas
ecosystem dependency appears, or local execution misses a measured objective.
Engage the data-compute Wargames when the engine, representation, acceleration
or execution mode is genuinely under pressure. A venture may depart from this
profile through a recorded ruling; no package name here overrides an
applicable binding security, privacy or reproducibility floor.
