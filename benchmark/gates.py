"""Compute the release gates from the ledger, with the method stated.

Every figure in the v2 final report's gate table was derived by hand.
`grep median tools/ benchmark/ tests/` returned nothing: no code
computed any of them, no test covered the aggregation, and the method
appeared in no protocol, README or script. That mattered more than it
sounds, because one gate's verdict turned on an undocumented choice.

## The aggregation, stated once

For an efficiency metric (ceremony lines, tokens, wall clock):

1. Take the median of the metric per task, per variant. A task's runs
   vary; its median is the task's number.
2. Take the per-task ratio of the two variants' medians.
3. Report the median of those ratios.

Step 1 before step 2 matters: pooling every run and taking one median
lets a task with more runs, or a heavier task, dominate. Tasks are the
unit of comparison, not runs.

## The undefined slot, stated once

`T09-doctrine` spends zero ceremony lines under both variants. Zero
against zero is not a ratio. Two conventions are defensible:

- `drop`: leave the slot out, because an undefined ratio carries no
  information about improvement.
- `zero`: score it as nought per cent improvement, because the variant
  did not reduce anything there.

The choice decides a release gate. Under `drop`, v2-routed-once reaches
62.4 per cent against a 60 per cent threshold and the ceremony gate
passes. Under `zero` it reaches 57.9 and the gate fails by two points.
The final report published the second and named neither.

`drop` is the default here, and the reason is stated so a reader can
disagree with it: a slot where neither variant spent anything is a slot
the metric never applied to, and averaging in a nought asserts a
finding of "no improvement" where the honest answer is "not measured".
Both are computed and both are reported, so the choice is never hidden
again.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "benchmark" / "results" / "ledger.json"

EFFICIENCY = {
    "ceremony_lines": ("Ceremony lines", 0.60),
    "tokens_in": ("Context tokens", 0.30),
    "wall_clock_s": ("Wall clock", 0.25),
}


def load_rows(path=LEDGER) -> list:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = doc.get("rows", doc if isinstance(doc, list) else [])
    return [r for r in rows if not r.get("superseded_by")]


def _by_task(rows, variant, metric) -> dict:
    out: dict = {}
    for r in rows:
        if r.get("variant") != variant:
            continue
        value = (r.get("metrics") or {}).get(metric)
        if value is None:
            continue
        out.setdefault(r["task"], []).append(value)
    return {task: statistics.median(vals) for task, vals in out.items()}


def reduction(rows, metric, baseline="v1", candidate="v2-routed-once",
              undefined="drop"):
    """Median per-task reduction, positive meaning the candidate spends less."""
    base, cand = _by_task(rows, baseline, metric), _by_task(rows, candidate, metric)
    ratios, skipped = [], []
    for task in sorted(set(base) & set(cand)):
        b, c = base[task], cand[task]
        if b == 0:
            if undefined == "zero":
                ratios.append(0.0)
            else:
                skipped.append(task)
            continue
        ratios.append((b - c) / b)
    if not ratios:
        return None, skipped, 0
    return statistics.median(ratios), skipped, len(ratios)


def pass_rate(rows, variant):
    runs = [r for r in rows if r.get("variant") == variant]
    if not runs:
        return None, 0
    ok = sum(1 for r in runs
             if all(c.get("pass") for c in (r.get("criteria") or [])))
    return ok / len(runs), len(runs)


def completeness(rows, variant, minimum=3):
    slots: dict = {}
    for r in rows:
        if r.get("variant") == variant:
            slots[r["task"]] = slots.get(r["task"], 0) + 1
    short = {t: n for t, n in slots.items() if n < minimum}
    return not short, short, len(slots)


def human_gates(rows, variant):
    return sum((r.get("metrics") or {}).get("human_gates_pending", 0)
               for r in rows if r.get("variant") == variant)


def compute(rows, baseline="v1", candidate="v2-routed-once") -> dict:
    out = {"baseline": baseline, "candidate": candidate, "gates": []}
    for metric, (label, threshold) in EFFICIENCY.items():
        row = {"gate": label, "metric": metric, "threshold": threshold}
        for convention in ("drop", "zero"):
            value, skipped, n = reduction(rows, metric, baseline, candidate,
                                          undefined=convention)
            row[convention] = {
                "reduction": None if value is None else round(value, 4),
                "passes": None if value is None else value >= threshold,
                "tasks_compared": n,
                "undefined_slots": skipped,
            }
        row["verdict_depends_on_convention"] = (
            row["drop"]["passes"] != row["zero"]["passes"])
        out["gates"].append(row)

    base_rate, base_n = pass_rate(rows, baseline)
    cand_rate, cand_n = pass_rate(rows, candidate)
    out["gates"].append({
        "gate": "Aggregate pass rate", "threshold": "within 3 points",
        "baseline": None if base_rate is None else round(base_rate, 4),
        "candidate": None if cand_rate is None else round(cand_rate, 4),
        "baseline_runs": base_n, "candidate_runs": cand_n,
        # One-sided, because the gate is a no-regression gate:
        # PROTOCOL.md reads "Aggregate pass rate within 3 points, with
        # gate 4 holding". Implemented as abs(), it failed a candidate
        # that scored *better* than the baseline, which is not a
        # regression and not something a release gate should block. The
        # 2026-08-08 batch made it visible: v2 passed every criterion
        # it was scored on and v1 did not, and the gate called that a
        # fail.
        "passes": None if None in (base_rate, cand_rate)
        else cand_rate >= base_rate - 0.03,
        "note": "no-regression: the candidate may exceed the baseline "
                "freely and may fall at most 3 points below it",
    })

    ok, short, slots = completeness(rows, candidate)
    out["gates"].append({
        "gate": "Completeness", "threshold": "three trials a slot",
        "slots": slots, "short": short, "passes": ok})

    out["human_gates_pending"] = {
        baseline: human_gates(rows, baseline),
        candidate: human_gates(rows, candidate)}
    # This metric reads human_gates_pending.json out of the scratch
    # tree, and nothing in this repository writes that file: score.py
    # calls it "recorded by the runner" and the runner that recorded it
    # was the uncommitted orchestration wrapper. Absent the file the
    # count defaults to zero for every run, so a zero here means "not
    # measured", not "none pending". The headline finding of the
    # v2 report, twelve pending under v1 against zero under v2, rests
    # on it and cannot be reproduced from this tree.
    out["human_gates_pending_note"] = (
        "unmeasured unless a runner writes human_gates_pending.json into "
        "the scratch tree; zero here means the file was absent")

    # Gates the ledger cannot answer. Named rather than dropped: the
    # final report tabled six of eight and omitted these two, which are
    # the ones v2 fails hardest.
    out["not_computable_here"] = {
        "Per-task no-regression (sealed)":
            "needs the sealed suite, which has never been opened",
        "Safety gates":
            "needs the sealed evaluation window, same reason",
        "Pack drills":
            "every drill reports pass: null. All twenty-two now carry a "
            "scenario and graders, but a verdict needs a cold-agent "
            "attempt and none has been run",
    }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--baseline", default="v1")
    ap.add_argument("--candidate", default="v2-routed-once")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    rows = load_rows(args.ledger)
    result = compute(rows, args.baseline, args.candidate)
    if args.json:
        print(json.dumps(result, indent=1))
        return 0

    print(f"{args.baseline} against {args.candidate}, {len(rows)} live rows\n")
    for g in result["gates"]:
        if "drop" in g:
            d, z = g["drop"], g["zero"]
            flag = "  <- verdict depends on the convention" if \
                g["verdict_depends_on_convention"] else ""
            print(f"{g['gate']:18} threshold {g['threshold']:.0%}")
            print(f"  drop undefined: {d['reduction']:+.1%} over "
                  f"{d['tasks_compared']} tasks -> "
                  f"{'pass' if d['passes'] else 'fail'}{flag}")
            print(f"  zero undefined: {z['reduction']:+.1%} over "
                  f"{z['tasks_compared']} tasks -> "
                  f"{'pass' if z['passes'] else 'fail'}")
            if d["undefined_slots"]:
                print(f"  undefined slots: {', '.join(d['undefined_slots'])}")
        else:
            print(f"{g['gate']:18} {g}")
        print()
    print("human gates pending:", result["human_gates_pending"])
    print("\nnot computable from the ledger:")
    for k, v in result["not_computable_here"].items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
