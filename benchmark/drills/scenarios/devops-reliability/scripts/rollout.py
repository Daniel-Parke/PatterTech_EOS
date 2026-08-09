#!/usr/bin/env python3
"""Decide whether a canary step may go forward.

    python scripts/rollout.py --metrics metrics.json
    python scripts/rollout.py --metrics metrics.json --config deploy/rollout.json

`metrics.json` is a flat object of metric name to number, the numbers
being whatever the dashboard is showing for the canary right now. The
plan in `deploy/rollout.json` may declare `failure_conditions`, each of
them `{"metric": ..., "operator": ..., "value": ...}`. If any of them is
true the script prints the plan's `on_failure` action; otherwise it
prints `promote`.

Exit code is 0 when the answer is promote and 1 when it is anything
else, so a pipeline step can just look at the code.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "deploy" / "rollout.json"

OPERATORS = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


def load(path, what):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        sys.exit("cannot read %s: %s" % (what, exc))


def breaches(config, metrics):
    """Every declared failure condition the metrics currently trip."""
    tripped = []
    for condition in config.get("failure_conditions") or []:
        metric = condition.get("metric")
        operator = OPERATORS.get(condition.get("operator", ">"))
        threshold = condition.get("value")
        if metric is None or operator is None or threshold is None:
            sys.exit("failure condition is not usable: %r" % (condition,))
        if metric not in metrics:
            continue
        if operator(metrics[metric], threshold):
            tripped.append("%s %s %s (saw %s)" % (
                metric, condition.get("operator", ">"), threshold,
                metrics[metric]))
    return tripped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", required=True,
                        help="JSON file of metric name to number")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG),
                        help="the rollout plan (default deploy/rollout.json)")
    args = parser.parse_args(argv)

    config = load(args.config, "the rollout plan")
    metrics = load(args.metrics, "the metrics")

    conditions = config.get("failure_conditions") or []
    if not conditions:
        print("promote")
        print("no failure conditions are declared in the plan, so there is "
              "nothing to check")
        return 0

    tripped = breaches(config, metrics)
    if not tripped:
        print("promote")
        print("%d failure condition(s) checked, none tripped"
              % len(conditions))
        return 0

    action = str(config.get("on_failure", "notify"))
    print(action)
    for line in tripped:
        print("tripped: %s" % line)
    return 0 if action == "promote" else 1


if __name__ == "__main__":
    raise SystemExit(main())
