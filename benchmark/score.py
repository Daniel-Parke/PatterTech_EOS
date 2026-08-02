"""Benchmark scorer: run task criteria, extract metrics from a transcript, append to the ledger.

Stdlib only. See benchmark/README.md for the full flow and the run_meta.json contract.

Order of operations:
  1. Parse the transcript JSONL for tool use, tokens, timing and written files.
  2. Write run_meta.json into the scratch dir so criteria scripts can consume
     transcript-derived facts (operator_events, commands, files_written).
  3. Run every criteria script against the scratch dir.
  4. Append exactly one row to benchmark/results/ledger.json. Append only:
     a duplicate run_id is refused and nothing is ever rewritten.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
LEDGER_PATH = BENCH_DIR / "results" / "ledger.json"

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
READ_TOOLS = {"Read"}
COMMAND_TOOLS = {"Bash", "PowerShell", "Shell"}

# Process-mandated artefacts across BOTH variants: v1 (session logs, STATE,
# worklog, feedback, questions, queue rows) and v2 (task records, state.yaml).
# Counted uniformly so the ceremony comparison is fair.
CEREMONY_PATTERN = re.compile(
    r"(org[\\/]+logs|org[\\/]+tasks|STATE|state\.ya?ml|session[-_]?log"
    r"|resume[-_]?packet|WORKLOG|EOS_FEEDBACK|QUESTIONS|TASKS\.md"
    r"|org[\\/]+QUEUE)",
    re.IGNORECASE,
)


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def iter_tool_uses(node):
    """Yield every tool_use dict found anywhere inside a parsed JSONL record."""
    if isinstance(node, dict):
        if node.get("type") == "tool_use" and "name" in node:
            yield node
        for value in node.values():
            yield from iter_tool_uses(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_tool_uses(item)


def find_usage(node):
    """Yield every usage dict (token counts) found inside a record."""
    if isinstance(node, dict):
        if "usage" in node and isinstance(node["usage"], dict):
            yield node["usage"]
        for value in node.values():
            yield from find_usage(value)
    elif isinstance(node, list):
        for item in node:
            yield from find_usage(item)


def parse_timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_transcript(path):
    stats = {
        "files_read": 0,
        "files_written": 0,
        "written_paths": [],
        "written_lines": {},
        "commands": [],
        "operator_events": 0,
        "turns": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "first_ts": None,
        "last_ts": None,
    }
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"could not read transcript {path}: {exc}")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        ts = parse_timestamp(record.get("timestamp"))
        if ts is not None:
            if stats["first_ts"] is None:
                stats["first_ts"] = ts
            stats["last_ts"] = ts

        record_type = record.get("type") or record.get("role")
        if record_type == "assistant":
            stats["turns"] += 1

        for usage in find_usage(record):
            stats["tokens_in"] += int(
                usage.get("input_tokens", usage.get("tokens_in", 0)) or 0
            )
            # cached context is still context the run consumed; count it so
            # tokens_in reflects real context volume, uniformly per variant
            stats["tokens_in"] += int(
                usage.get("cache_read_input_tokens", 0) or 0
            ) + int(usage.get("cache_creation_input_tokens", 0) or 0)
            stats["tokens_out"] += int(
                usage.get("output_tokens", usage.get("tokens_out", 0)) or 0
            )

        for tool in iter_tool_uses(record):
            name = tool.get("name", "")
            tool_input = tool.get("input") or {}
            if name in READ_TOOLS:
                stats["files_read"] += 1
            elif name in WRITE_TOOLS:
                stats["files_written"] += 1
                path_value = tool_input.get("file_path") or tool_input.get("path")
                if path_value:
                    stats["written_paths"].append(path_value)
                    content = tool_input.get("content") or tool_input.get("new_string") or ""
                    line_count = len(str(content).splitlines())
                    stats["written_lines"][path_value] = (
                        stats["written_lines"].get(path_value, 0) + line_count
                    )
            elif name in COMMAND_TOOLS:
                command = tool_input.get("command")
                if command:
                    stats["commands"].append(str(command))
            elif name == "AskUserQuestion":
                stats["operator_events"] += 1

    return stats


def ceremony_lines(stats):
    total = 0
    for path_value, count in stats["written_lines"].items():
        if CEREMONY_PATTERN.search(path_value):
            total += count
    return total


def write_run_meta(scratch, stats):
    meta = {
        "operator_events": stats["operator_events"],
        "commands": stats["commands"],
        "files_written": stats["written_paths"],
    }
    meta_path = Path(scratch) / "run_meta.json"
    with open(meta_path, "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)
        handle.write("\n")
    return meta_path


def collect_criteria_scripts(task_dir, task):
    task_path = Path(task_dir)
    named = task.get("criteria")
    if named:
        # task.json schema: criteria is a list of {id, desc, script} objects
        # (script relative to the task dir); plain strings also accepted.
        scripts = []
        for entry in named:
            rel = entry.get("script") if isinstance(entry, dict) else entry
            if not rel:
                fail(f"criteria entry without script in {task_path}")
            scripts.append(task_path / rel)
    else:
        criteria_dir = task_path / "criteria"
        if not criteria_dir.is_dir():
            fail(f"no criteria directory or criteria list for task {task_path}")
        scripts = sorted(p for p in criteria_dir.iterdir() if p.is_file())
    for script in scripts:
        if not script.is_file():
            fail(f"criteria script not found: {script}")
    return scripts


def run_criteria(scripts, scratch):
    results = []
    for script in scripts:
        cmd = [sys.executable, str(script), str(scratch)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            results.append({"id": script.stem, "pass": False, "reason": "criteria script timed out"})
            continue
        try:
            payload = json.loads(proc.stdout.strip())
            results.append(
                {
                    "id": payload.get("id", script.stem),
                    "pass": bool(payload.get("pass", False)),
                    "reason": payload.get("reason", ""),
                }
            )
        except (json.JSONDecodeError, ValueError):
            reason = proc.stderr.strip() or "criteria script produced no parseable JSON"
            results.append({"id": script.stem, "pass": False, "reason": reason})
    return results


def append_ledger_row(row):
    if not LEDGER_PATH.is_file():
        fail(f"ledger not found: {LEDGER_PATH}")
    try:
        with open(LEDGER_PATH, encoding="utf-8") as handle:
            ledger = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"could not read ledger: {exc}")

    existing_ids = {r.get("run_id") for r in ledger.get("rows", [])}
    if row["run_id"] in existing_ids:
        fail(f"duplicate run_id refused: {row['run_id']}")

    ledger.setdefault("rows", []).append(row)

    fd, tmp_path = tempfile.mkstemp(dir=str(LEDGER_PATH.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(ledger, handle, indent=2)
            handle.write("\n")
        os.replace(tmp_path, LEDGER_PATH)
    except OSError as exc:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        fail(f"could not write ledger: {exc}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="task directory containing task.json")
    parser.add_argument("--scratch", required=True, help="scratch dir the session worked in")
    parser.add_argument("--transcript", required=True, help="session transcript JSONL")
    parser.add_argument("--variant", required=True, help="variant label, for example v1 or v2")
    parser.add_argument("--run-id", required=True, help="unique run identifier")
    parser.add_argument("--model", default="claude-fable-5", help="model id used for the run")
    parser.add_argument("--notes", default="", help="free-text notes for the ledger row")
    args = parser.parse_args(argv)

    task_path = Path(args.task)
    task_json = task_path / "task.json"
    if not task_json.is_file():
        fail(f"no task.json in {task_path}")
    with open(task_json, encoding="utf-8") as handle:
        task = json.load(handle)

    scratch = Path(args.scratch)
    if not scratch.is_dir():
        fail(f"scratch dir not found: {scratch}")

    stats = parse_transcript(args.transcript)

    write_run_meta(scratch, stats)

    scripts = collect_criteria_scripts(task_path, task)
    criteria = run_criteria(scripts, scratch)

    wall_clock_s = 0.0
    if stats["first_ts"] is not None and stats["last_ts"] is not None:
        wall_clock_s = (stats["last_ts"] - stats["first_ts"]).total_seconds()

    row = {
        "run_id": args.run_id,
        "task": task.get("id", task_path.name),
        "variant": args.variant,
        "ablation": None,
        "date": datetime.date.today().isoformat(),
        "model": args.model,
        "source": "fresh",
        "criteria": criteria,
        "metrics": {
            "files_read": stats["files_read"],
            "files_written": stats["files_written"],
            "ceremony_lines": ceremony_lines(stats),
            "tokens_in": stats["tokens_in"],
            "tokens_out": stats["tokens_out"],
            "wall_clock_s": wall_clock_s,
            "operator_events": stats["operator_events"],
            "turns": stats["turns"],
        },
        "notes": args.notes,
    }

    append_ledger_row(row)
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
