"""Benchmark runner: materialise fixtures into scratch repos and print task prompts.

Stdlib only. See benchmark/README.md for the full session flow.

Subcommands:
  materialise --fixture <name> --dest <dir> [--task <dir>]
      Copy benchmark/fixtures/<name> into dest (holdout material excluded),
      initialise a git repo there with an initial commit, apply the task's
      break.patch if one exists, then print the task prompt.
  prompt --task <dir>
      Print the prompt from the task's task.json and nothing else.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = BENCH_DIR / "fixtures"
HOLDOUT_MARKER = "holdout"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def load_task(task_dir):
    task_path = Path(task_dir)
    task_json = task_path / "task.json"
    if not task_json.is_file():
        fail(f"no task.json in {task_path}")
    try:
        with open(task_json, encoding="utf-8") as handle:
            return task_path, json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"could not read {task_json}: {exc}")


def ignore_holdout(directory, names):
    """shutil.copytree ignore filter: skip anything that is holdout material."""
    skipped = []
    for name in names:
        if HOLDOUT_MARKER in name.lower():
            skipped.append(name)
            continue
        full = Path(directory) / name
        if any(HOLDOUT_MARKER in part.lower() for part in full.parts):
            skipped.append(name)
    return set(skipped)


def run_git(dest, *args):
    cmd = [
        "git",
        "-c", "user.name=eos-benchmark",
        "-c", "user.email=benchmark@pattertech.invalid",
        "-C", str(dest),
    ] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed in {dest}: {result.stderr.strip()}")
    return result


def cmd_materialise(args):
    fixture = FIXTURES_DIR / args.fixture
    if not fixture.is_dir():
        fail(f"fixture not found: {fixture}")
    dest = Path(args.dest)
    if dest.exists() and any(dest.iterdir()):
        fail(f"destination is not empty: {dest}")

    shutil.copytree(fixture, dest, ignore=ignore_holdout, dirs_exist_ok=True)

    run_git(dest, "init")
    run_git(dest, "add", "-A")
    run_git(dest, "commit", "--allow-empty", "-m", "fixture: initial state")

    if args.task:
        task_path, task = load_task(args.task)
        patch = task_path / "break.patch"
        if patch.is_file():
            run_git(dest, "apply", str(patch.resolve()))
        prompt = task.get("prompt")
        if not prompt:
            fail(f"task.json in {task_path} has no prompt field")
        print(prompt)


def cmd_prompt(args):
    task_path, task = load_task(args.task)
    prompt = task.get("prompt")
    if not prompt:
        fail(f"task.json in {task_path} has no prompt field")
    print(prompt)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_mat = sub.add_parser("materialise", help="copy a fixture into a scratch dir and set it up")
    p_mat.add_argument("--fixture", required=True, help="fixture name under benchmark/fixtures/")
    p_mat.add_argument("--dest", required=True, help="destination directory (empty or absent)")
    p_mat.add_argument("--task", help="task directory containing task.json and optional break.patch")
    p_mat.set_defaults(func=cmd_materialise)

    p_prompt = sub.add_parser("prompt", help="print the task prompt only")
    p_prompt.add_argument("--task", required=True, help="task directory containing task.json")
    p_prompt.set_defaults(func=cmd_prompt)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
