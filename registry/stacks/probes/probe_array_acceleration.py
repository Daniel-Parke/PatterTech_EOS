"""Deterministic NumPy-to-Numba boundary probe for the dated stack profile."""

from __future__ import annotations

import hashlib
import json
import platform
import time

import numba
import numpy as np


@numba.njit(cache=False)
def compiled_score(values):
    total = 0.0
    for value in values:
        total += value * value + np.sin(value)
    return total


def main() -> None:
    values = np.linspace(-5.0, 5.0, 500_000, dtype=np.float64)

    started = time.perf_counter_ns()
    expected = float(np.sum(values * values + np.sin(values)))
    numpy_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    first = float(compiled_score(values))
    compile_inclusive_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    steady = float(compiled_score(values))
    steady_ns = time.perf_counter_ns() - started
    tolerance = 1e-8 * max(1.0, abs(expected))
    canonical = np.asarray([expected, first, steady], dtype=np.float64).tobytes()
    print(json.dumps({
        "probe": "array-acceleration",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "versions": {"numpy": np.__version__, "numba": numba.__version__},
        "elements": int(values.size),
        "dtype": str(values.dtype),
        "matches_tolerance": {
            "first": abs(first - expected) <= tolerance,
            "steady": abs(steady - expected) <= tolerance,
        },
        "tolerance": tolerance,
        "result_sha256": hashlib.sha256(canonical).hexdigest(),
        "timings_ns": {
            "numpy_vectorised": numpy_ns,
            "numba_compile_inclusive": compile_inclusive_ns,
            "numba_steady": steady_ns,
        },
        "timing_note": "One local observation only; compilation, hardware and workload decide the route.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
