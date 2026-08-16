"""Deterministic local probe for the dated data-compute stack profile."""

from __future__ import annotations

import hashlib
import json
import platform
import time

import duckdb
import numpy as np
import pandas as pd
import polars as pl


def _hash_rows(rows) -> str:
    encoded = json.dumps(rows, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    frame = pd.DataFrame({
        "group": np.arange(20_000, dtype=np.int64) % 17,
        "value": np.arange(20_000, dtype=np.float64) / 7.0,
    })
    frame.index = pd.Index(np.arange(len(frame)) + 10_000, name="row_id")

    started = time.perf_counter_ns()
    polar = pl.from_pandas(frame.reset_index())
    converted_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    polar_rows = (
        polar.lazy()
        .filter(pl.col("value") >= 1_000)
        .group_by("group")
        .agg(pl.col("value").sum().alias("total"))
        .sort("group")
        .collect()
        .rows(named=True)
    )
    polars_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    duck_rows = duckdb.sql(
        "SELECT \"group\", SUM(value) AS total FROM frame "
        "WHERE value >= 1000 GROUP BY \"group\" ORDER BY \"group\""
    ).fetchall()
    duckdb_ns = time.perf_counter_ns() - started
    duck_rows = [
        {"group": int(group), "total": float(total)}
        for group, total in duck_rows
    ]

    array = polar.select("value").to_numpy()
    index_preserved_explicitly = (
        np.array_equal(polar["row_id"].to_numpy(), frame.index.to_numpy())
        and np.array_equal(
            polar["value"].to_numpy(),
            frame["value"].to_numpy(),
        )
    )
    result_match = all(
        left["group"] == right["group"]
        and np.isclose(left["total"], right["total"], rtol=1e-12, atol=1e-9)
        for left, right in zip(polar_rows, duck_rows, strict=True)
    )
    canonical_rows = [
        {
            "group": group,
            "total_numerator": sum(
                value for value in range(7_000, 20_000) if value % 17 == group
            ),
            "denominator": 7,
        }
        for group in range(17)
    ]
    expected_totals = {
        row["group"]: row["total_numerator"] / row["denominator"]
        for row in canonical_rows
    }
    expected_result_match = all(
        np.isclose(
            row["total"],
            expected_totals[row["group"]],
            rtol=1e-12,
            atol=1e-9,
        )
        for row in [*polar_rows, *duck_rows]
    )
    result_hash = _hash_rows(canonical_rows)
    print(json.dumps({
        "probe": "tabular-boundary",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "versions": {
            "polars": pl.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "duckdb": duckdb.__version__,
        },
        "rows": len(frame),
        "array": {"shape": list(array.shape), "dtype": str(array.dtype)},
        "index_preserved_explicitly": index_preserved_explicitly,
        "result_match": result_match,
        "expected_result_match": expected_result_match,
        "result_sha256": result_hash,
        "timings_ns": {
            "pandas_to_polars": converted_ns,
            "polars_lazy_query": polars_ns,
            "duckdb_query": duckdb_ns,
        },
        "timing_note": "One local observation only; not a comparative benchmark.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
