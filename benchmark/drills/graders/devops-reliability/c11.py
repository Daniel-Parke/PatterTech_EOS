#!/usr/bin/env python3
"""Criterion 11: the rollout aborts itself, and can be shown doing it.

Static half: the rollout plan declares at least one failure condition
with a metric and a threshold, and says somewhere that the action on
failure is to abort rather than to notify a human.

Dynamic half: the plan's own conditions are read, a metrics file is
synthesised that breaches every one of them, and the repository's
rollout evaluator is run against it. The answer has to be abort. The
metrics are built from the delivered conditions rather than from a
fixed list, so an agent that invents its own metric names is still
tested against its own plan.

Where the tree declares a failure condition but ships nothing that can
be dry-run here, the criterion is left unsettled: the plan may be
perfectly good and this machine simply cannot drive it.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, copy_tree, emit,  # noqa: E402
                     find_one, iter_files, load_structured, path_tokens,
                     run, scratch_dir)

CID = "c11"

PLAN_TOKENS = {"rollout", "rollouts", "canary", "deploy", "release",
               "promotion"}
METRIC_KEYS = ("metric", "metric_name", "metricname", "sli", "name", "query")
VALUE_KEYS = ("value", "threshold", "max", "maximum", "limit", "min",
              "minimum")
OPERATOR_KEYS = ("operator", "op", "comparison", "compare", "direction")
FAILURE_KEYS = ("failure", "abort", "analysis", "guard", "halt", "rollback")
ABORT_KEYS = ("on_failure", "onfailure", "failure_action", "failureaction",
              "failure_policy", "failurepolicy", "on_abort", "abort",
              "auto_abort", "autoabort", "automatic_abort", "action")
ABORT_VALUES = {"abort", "automatic", "auto", "true", "yes", "rollback",
                "halt", "stop"}
DECISIONS = {"abort", "promote", "hold", "pause", "notify", "fail",
             "rollback", "halt", "continue"}


def walk(node, key=None):
    yield key, node
    if isinstance(node, dict):
        for k, v in node.items():
            for pair in walk(v, str(k)):
                yield pair
    elif isinstance(node, list):
        for item in node:
            for pair in walk(item, key):
                yield pair


def conditions_in(node):
    """Every {metric, operator, threshold} triple anywhere in the plan."""
    found = []
    for _, value in walk(node):
        if not isinstance(value, dict):
            continue
        keys = {str(k).lower(): k for k in value}
        metric_key = next((keys[k] for k in METRIC_KEYS if k in keys), None)
        value_key = next((keys[k] for k in VALUE_KEYS if k in keys), None)
        if metric_key is None or value_key is None:
            continue
        metric, threshold = value[metric_key], value[value_key]
        if not isinstance(metric, str) or isinstance(threshold, bool):
            continue
        if not isinstance(threshold, (int, float)):
            continue
        operator_key = next((keys[k] for k in OPERATOR_KEYS if k in keys),
                            None)
        operator = str(value.get(operator_key, ">")) if operator_key else ">"
        found.append((metric, operator, float(threshold)))
    return found


def declares_abort(plan):
    for key, value in walk(plan):
        if key is None:
            continue
        low = str(key).lower().replace("-", "_")
        if low not in ABORT_KEYS and "abort" not in low:
            continue
        if isinstance(value, bool):
            if value:
                return "%s: true" % key
            continue
        if isinstance(value, str) and value.strip().lower() in ABORT_VALUES:
            return "%s: %s" % (key, value)
    return None


def has_failure_section(plan):
    for key, value in walk(plan):
        if key is None:
            continue
        low = str(key).lower()
        if any(token in low for token in FAILURE_KEYS) and value:
            if isinstance(value, (list, dict)) and conditions_in(value):
                return str(key)
    return None


def breach(operator, threshold):
    step = max(1.0, abs(threshold))
    if operator in ("<", "<=", "lt", "le", "below", "less"):
        return threshold - step
    if operator in ("==", "=", "eq", "equal"):
        return threshold
    if operator in ("!=", "ne"):
        return threshold + step
    return threshold + step


def evaluators(scratch):
    out = []
    for path in iter_files(scratch, suffixes={".py"}):
        rel = path.relative_to(scratch)
        if path_tokens(rel) & {"rollout", "canary", "promote", "promotion",
                               "analysis"}:
            out.append(rel)
    return sorted(out, key=lambda p: (len(p.parts), p.name))


def decision(output):
    for line in output.splitlines():
        word = line.strip().strip(".:").lower()
        if word in DECISIONS:
            return word
    lowered = output.lower()
    if "abort" in lowered:
        return "abort"
    if "promote" in lowered:
        return "promote"
    return None


def main():
    scratch = scratch_dir()

    plans = find_one(scratch, PLAN_TOKENS)
    if not plans:
        emit(CID, FAIL, "no rollout configuration in the tree")

    chosen, plan, notes = None, None, []
    for path in plans:
        doc, error = load_structured(path)
        if error:
            notes.append(error)
            continue
        if conditions_in(doc) or has_failure_section(doc):
            chosen, plan = path, doc
            break
        if chosen is None and isinstance(doc, dict):
            chosen, plan = path, doc
    if plan is None:
        emit(CID, FAIL, "no rollout configuration parses: %s"
                        % "; ".join(notes[:2]))

    where = chosen.relative_to(scratch).as_posix()
    section = has_failure_section(plan)
    conditions = conditions_in(plan)
    if not section or not conditions:
        emit(CID, FAIL,
             "%s declares no failure condition, so the canary has nothing "
             "to fail against" % where)

    abort = declares_abort(plan)
    if not abort:
        emit(CID, FAIL,
             "%s declares %d failure condition(s) under %r but never says "
             "the action is to abort, so a breach still waits for a human"
             % (where, len(conditions), section))

    metrics = {metric: breach(operator, threshold)
               for metric, operator, threshold in conditions}

    scripts = evaluators(scratch)
    if not scripts:
        emit(CID, UNSETTLED,
             "%s declares %d failure condition(s) and %s, but the tree has "
             "no evaluator this grader can dry-run, so the abort was not "
             "demonstrated" % (where, len(conditions), abort))

    work, copy = copy_tree(scratch, "drill-devops-c11-")
    try:
        metrics_file = copy / "drill-metrics.json"
        metrics_file.write_text(json.dumps(metrics, indent=1),
                                encoding="utf-8")
        problems = []
        for rel in scripts:
            attempts = (
                [sys.executable, rel.as_posix(), "--metrics",
                 metrics_file.name, "--config", where],
                [sys.executable, rel.as_posix(), "--metrics",
                 metrics_file.name],
                [sys.executable, rel.as_posix(), metrics_file.name],
            )
            for argv in attempts:
                code, output = run(argv, copy, timeout=120)
                if code is None:
                    problems.append("%s would not start" % rel.as_posix())
                    break
                answer = decision(output)
                if answer is None:
                    continue
                if answer in ("abort", "rollback", "halt", "fail"):
                    emit(CID, PASS,
                         "%s declares %d failure condition(s) and %s; a "
                         "dry-run of %s against metrics that breach all of "
                         "them answered %r"
                         % (where, len(conditions), abort, rel.as_posix(),
                            answer))
                problems.append(
                    "%s answered %r on metrics that breach every declared "
                    "condition (%s)"
                    % (rel.as_posix(), answer,
                       ", ".join("%s=%g" % kv for kv in
                                 sorted(metrics.items()))[:120]))
                break
            else:
                problems.append("%s never returned a decision this grader "
                                "could read" % rel.as_posix())
        emit(CID, FAIL, "; ".join(problems[:3]) or
             "no rollout evaluator produced a decision")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
