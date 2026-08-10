"""Gate computation tests: the aggregation, and the convention that
decided a release gate without ever being written down."""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

sys.path.insert(0, str(REPO / "benchmark"))
import gates  # noqa: E402


def _row(task, variant, run, **metrics):
    return {"run_id": run, "task": task, "variant": variant,
            "criteria": [{"id": "c1", "pass": True}],
            "metrics": {"ceremony_lines": 0, "tokens_in": 0,
                        "wall_clock_s": 0, "human_gates_pending": 0,
                        **metrics}}


def test_median_of_per_task_ratios_not_pooled_runs():
    """A heavy task with more runs must not dominate. Tasks are the
    unit of comparison, runs are not."""
    rows = [
        _row("light", "v1", "a1", ceremony_lines=10),
        _row("light", "v2", "b1", ceremony_lines=5),      # 50 per cent
        _row("heavy", "v1", "a2", ceremony_lines=100),
        _row("heavy", "v1", "a3", ceremony_lines=100),
        _row("heavy", "v1", "a4", ceremony_lines=100),
        _row("heavy", "v2", "b2", ceremony_lines=10),     # 90 per cent
        _row("heavy", "v2", "b3", ceremony_lines=10),
        _row("heavy", "v2", "b4", ceremony_lines=10),
    ]
    value, skipped, n = gates.reduction(rows, "ceremony_lines", "v1", "v2")
    assert n == 2 and skipped == []
    assert abs(value - 0.70) < 1e-9      # median of 0.50 and 0.90


def test_undefined_slot_decides_the_ceremony_gate():
    """Zero against zero is not a ratio, and which convention is used
    flips the verdict. The report published one and named neither."""
    rows = [
        _row("a", "v1", "a1", ceremony_lines=100),
        _row("a", "v2", "b1", ceremony_lines=30),          # 70 per cent
        _row("b", "v1", "a2", ceremony_lines=0),           # undefined
        _row("b", "v2", "b2", ceremony_lines=0),
    ]
    dropped, skipped, n = gates.reduction(rows, "ceremony_lines", "v1", "v2",
                                          undefined="drop")
    assert skipped == ["b"] and n == 1
    assert abs(dropped - 0.70) < 1e-9

    zeroed, skipped, n = gates.reduction(rows, "ceremony_lines", "v1", "v2",
                                         undefined="zero")
    assert skipped == [] and n == 2
    assert abs(zeroed - 0.35) < 1e-9


def test_compute_flags_a_convention_dependent_verdict():
    rows = [
        _row("a", "v1", "a1", ceremony_lines=100),
        _row("a", "v2", "b1", ceremony_lines=38),
        _row("b", "v1", "a2", ceremony_lines=0),
        _row("b", "v2", "b2", ceremony_lines=0),
    ]
    result = gates.compute(rows, "v1", "v2")
    ceremony = next(g for g in result["gates"] if g["metric"] == "ceremony_lines")
    assert ceremony["drop"]["passes"] is True
    assert ceremony["zero"]["passes"] is False
    assert ceremony["verdict_depends_on_convention"] is True


def test_superseded_rows_are_excluded(tmp_path):
    """A rewritten row's original is kept for the trail and must never
    be scored twice."""
    led = tmp_path / "ledger.json"
    led.write_text(json.dumps({"version": 1, "rows": [
        _row("a", "v1", "a1", ceremony_lines=100),
        {**_row("a", "v1", "a1#1", ceremony_lines=999),
         "superseded_by": "a1"},
    ]}), encoding="utf-8")
    assert [r["run_id"] for r in gates.load_rows(led)] == ["a1"]


def test_the_real_ledger_reproduces_the_published_figures():
    """The report's numbers are reproducible, and the ceremony gate does
    turn on the convention."""
    rows = gates.load_rows()
    result = gates.compute(rows)
    by_metric = {g.get("metric"): g for g in result["gates"] if "metric" in g}
    assert by_metric["ceremony_lines"]["verdict_depends_on_convention"] is True
    assert by_metric["ceremony_lines"]["drop"]["passes"] is True
    assert by_metric["ceremony_lines"]["zero"]["passes"] is False
    assert by_metric["tokens_in"]["drop"]["passes"] is False
    assert by_metric["wall_clock_s"]["drop"]["passes"] is False
    assert result["human_gates_pending"]["v1"] == 12
    assert result["human_gates_pending"]["v2-routed-once"] == 0
