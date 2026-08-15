---
id: WG-DATA-003
summary: How far should a measured numerical hotspot move from clear array code towards JIT, native or device acceleration?
kind: wargame
type: wargame
tags: [data, eos, perf, testing, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-COD-012, DOC-DATA-020, DOC-DATA-021]
gap_domain: numeric-acceleration
applies_when: [edits_source, calls_a_model]
engages_when: [has_profiled_numeric_kernel]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0563, EV-0569, EV-0570, EV-0571]
review: 2027-08
lifecycle: active
---

# WG-DATA-003: Which acceleration rung is earned?

## Decision question and stakes

A profiler has identified a numerical kernel that materially affects the
target. Decide whether to simplify or vectorise it, compile it just in time,
move it behind a native boundary, or execute it on another device. The fastest
steady-state number can still be the wrong decision if compilation, transfer,
numerical drift, packaging or maintenance dominates the real journey.

## Doctrines or coverage gap under pressure

- `DOC-COD-012` keeps the pipeline simple until evidence shows the simple loop
  is insufficient.
- `DOC-DATA-020` requires a representative baseline, environment and oracle.
- `DOC-DATA-021` promotes only one measured rung at a time.
- The uncovered domain is `numeric-acceleration`: no package or device is a
  timeless default.

## Preconditions and engagement triggers

The profiler must name the kernel, its share of end-to-end elapsed time, input
shape and invocation frequency. Record latency versus throughput objective,
first-use constraints, supported deployment platforms, packaging budget and a
numerical oracle with tolerances. Separate algorithmic work from code-generation
work.

Applicability is `edits_source` or `calls_a_model`. Engage only when
`has_profiled_numeric_kernel` is true. A slow application with no isolated
kernel does not engage this Wargame.

## Options

### A. Clear baseline and vectorised array operations

Retain ordinary code, improve the algorithm or data access, and use maintained
array primitives where they make the intent clearer. This has the lowest
packaging and first-use cost. It can leave performance on the table where the
kernel cannot be expressed efficiently with available primitives.

### B. Just-in-time compilation of the isolated kernel

Compile the hot function for the supported types and compare compile-inclusive
first use with steady state. This can remove interpreter overhead without a
separate build toolchain. Unsupported features, compilation delay and relaxed
floating-point options can erase or counterfeit the gain (EV-0570).

### C. Owned native extension or maintained native library

Put the kernel behind a narrow, tested ABI or library boundary. This can give
predictable compiled performance and reuse a mature implementation. It adds a
toolchain, platform builds, memory-safety and packaging obligations.

### D. Device or GPU execution

Move a batch of work to an accelerator and include transfer, allocation and
synchronisation in the measurement. This can win for sufficient parallel work
but loses on small batches, unsupported operations or deployment targets
without the device. Package routes also change over time, as the Numba CUDA
move demonstrates (EV-0571).

## Failure premises

### Premortem for A. Clear baseline and vectorised array operations

Assume A failed. The kernel remained the dominant cost, temporary arrays
inflated memory, or an algorithmic improvement was dismissed before it was
tested because compilation looked more sophisticated.

### Premortem for B. Just-in-time compilation of the isolated kernel

Assume B failed. Production traffic paid compilation on a latency-sensitive
first call, an unsupported path fell back or failed, or fast numerical options
changed the result outside tolerance while the benchmark checked only time.

### Premortem for C. Owned native extension or maintained native library

Assume C failed. Builds diverged across platforms, the ABI or dependency moved,
or boundary conversions consumed the saving. A fast kernel became a release
and security liability nobody owned.

### Premortem for D. Device or GPU execution

Assume D failed. Transfer and synchronisation dominated, device memory failed
on representative peaks, or numerical and ordering differences escaped a weak
oracle. The chosen package route then changed independently of the product.

## Decision rule

First remove avoidable work and establish A. Select B only when the isolated
kernel still misses the objective and both compile-inclusive and steady-state
measurements pass the numerical oracle. Select C when a maintained native
implementation or required predictable deployment outweighs its build cost.
Select D only when end-to-end measurement including transfer beats the leading
host route on supported hardware and a non-device fallback is named.

Move one rung at a time. Reject any option whose end-to-end improvement is
smaller than measurement variance or whose correctness, packaging and fallback
cost is not recorded.

## Safe default

Keep the clear measured baseline. Optimise the algorithm and use maintained
array primitives before introducing compilation, native code or a device.

## Cheapest discriminating test

Use the profiled kernel and representative small, typical and peak inputs.
Measure the unmodified baseline, first invocation and steady state under the
same environment. Record compile, conversion, transfer and allocation time,
peak memory, numerical difference and deployment artefact size. Run the oracle
with strict rules first; test relaxed arithmetic as a separate option.

## Fallback, exit and revisit

**Fallback `clear-host-baseline`:** keep or restore the ordinary host
implementation behind the same function boundary and use it when compilation,
native loading or the device is unavailable.

**Exit condition:** remove the acceleration when it fails tolerance, supported
platforms, first-use latency or the minimum measured end-to-end gain recorded
in the ruling.

**Revisit trigger:** repeat when the workload shape, target hardware,
compiler, acceleration package, numerical contract or deployment platform
changes.

## Counter-evidence and transfer limits

Maintainer performance examples are teaching material, not universal
thresholds. Steady-state microbenchmarks omit compilation and data movement.
Protocol support does not guarantee zero-copy or equivalent arithmetic
(EV-0569). A successful ruling applies to the measured kernel and environment,
not to the rest of the codebase and not to a named accelerator package for all
future versions.
