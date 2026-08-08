"""Harness tests: the variant reaches the tree, and the tree stays clean.

The thing these guard is narrow and was missing entirely: that a
prepared scratch tree actually differs between v1 and v2, and that the
harness leaves nothing in it that the task's own criteria would read as
the session's work.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

HARNESS = REPO / "benchmark" / "harness.py"


def prepare(dest, task="T04-bug-fix", variant="v1", run_id="TEST-1"):
    proc = subprocess.run(
        [sys.executable, str(HARNESS), "prepare",
         "--task", str(REPO / "benchmark" / "tasks" / task),
         "--variant", variant, "--run-id", run_id, "--dest", str(dest)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc


def test_the_two_arms_get_different_process_files(tmp_path):
    """The whole point: a v1 tree and a v2 tree are not the same tree.

    For eight of the thirteen tasks they used to be byte-identical,
    because the fixture carries no process files and nothing placed
    any. A run labelled v1 and a run labelled v2 differed in the label
    and in nothing the agent could see.
    """
    for variant in ("v1", "v2"):
        assert prepare(tmp_path / variant, variant=variant).returncode == 0

    def tree(root):
        return {p.relative_to(root).as_posix()
                for p in root.rglob("*")
                if p.is_file() and ".git" not in p.parts}

    v1, v2 = tree(tmp_path / "v1"), tree(tmp_path / "v2")
    assert v1 != v2
    # The ceremony axis: v1 keeps a running log and a queue, v2 keeps
    # task records and a policy the router reads.
    assert "org/roles/PLAN.md" in v1 and "org/roles/PLAN.md" not in v2
    assert "org/QUEUE.md" in v1 and "org/QUEUE.md" not in v2
    assert "org/policy.json" in v2 and "org/policy.json" not in v1
    assert any(f.startswith("org/tasks/") for f in v2)
    # The work itself is identical in both arms.
    assert {f for f in v1 if f.startswith("app/")} == \
           {f for f in v2 if f.startswith("app/")}


def test_venture_content_is_identical_across_arms(tmp_path):
    """Only the process may differ, never the venture."""
    for variant in ("v1", "v2"):
        assert prepare(tmp_path / variant, variant=variant).returncode == 0
    for name in ("docs/VENTURE_BRIEF.md", "docs/LOCKBOOK.md"):
        a = (tmp_path / "v1" / name).read_text(encoding="utf-8")
        b = (tmp_path / "v2" / name).read_text(encoding="utf-8")
        assert a == b, name


def test_prepared_tree_is_clean_to_git(tmp_path):
    """Nothing the harness leaves behind may look like the session's work.

    run.json used to sit inside the tree. On an untouched T01 that made
    c3_scope fail with "changes outside docs/" and put c2_diff_budget
    at its whole ten-line budget before the agent started.
    """
    dest = tmp_path / "t01"
    assert prepare(dest, task="T01-doc-fix", variant="v1").returncode == 0
    proc = subprocess.run(["git", "-C", str(dest), "status", "--short"],
                          capture_output=True, text=True)
    assert proc.stdout.strip() == "", proc.stdout


def test_the_untouched_tree_fails_only_the_criterion_the_task_is_about(
        tmp_path):
    dest = tmp_path / "t01"
    assert prepare(dest, task="T01-doc-fix", variant="v1").returncode == 0
    (dest / "run_meta.json").write_text(json.dumps(
        {"operator_events": 0, "commands": [], "files_written": []}),
        encoding="utf-8")
    task = REPO / "benchmark" / "tasks" / "T01-doc-fix"
    verdicts = {}
    for script in sorted((task / "criteria").glob("*.py")):
        proc = subprocess.run([sys.executable, str(script), str(dest)],
                              capture_output=True, text=True)
        payload = json.loads(proc.stdout.strip().splitlines()[-1])
        verdicts[payload["id"]] = payload["pass"]
    # The dangling reference is the task; everything else starts clean.
    assert verdicts["c1_no_dangling"] is False
    assert verdicts["c2_diff_budget"] is True
    assert verdicts["c3_scope"] is True


def test_build_artefacts_in_a_fixture_do_not_reach_the_tree(tmp_path):
    """__pycache__ on disk is invisible to git and fatal to a diff budget."""
    fixture = REPO / "benchmark" / "fixtures" / "app-api"
    junk = fixture / "app" / "__pycache__"
    junk.mkdir(parents=True, exist_ok=True)
    marker = junk / "harness_test.cpython-314.pyc"
    marker.write_bytes(b"\x00\x01junk")
    try:
        dest = tmp_path / "clean"
        assert prepare(dest).returncode == 0
        assert list(dest.rglob("*.pyc")) == []
        assert list(dest.rglob("__pycache__")) == []
    finally:
        marker.unlink(missing_ok=True)
        try:
            junk.rmdir()
        except OSError:
            pass


def test_a_task_with_no_v2_counterpart_is_refused_rather_than_faked(tmp_path):
    """T09's fixture is a v1-shaped mini EOS with no v2 twin.

    Running it as v2 would score a slot that is not a comparison, and
    T09 is the 0/0 slot whose handling decides the ceremony gate.
    """
    proc = prepare(tmp_path / "t09", task="T09-doctrine", variant="v2")
    assert proc.returncode != 0
    assert "no v2 counterpart" in proc.stderr or \
           "measuring nothing" in proc.stderr


def test_run_metadata_names_which_placement_route_was_used(tmp_path):
    from benchmark import harness  # noqa: F401  (import path check)
    dest = tmp_path / "t04"
    assert prepare(dest).returncode == 0
    meta = json.loads((tmp_path / "t04.run.json").read_text(encoding="utf-8"))
    assert meta["surface"] == "overlaid"
    assert meta["fixture_declared"] == "app-api"
    assert meta["variant"] == "v1"

    dest2 = tmp_path / "t01"
    assert prepare(dest2, task="T01-doc-fix", variant="v2").returncode == 0
    meta2 = json.loads((tmp_path / "t01.run.json").read_text(encoding="utf-8"))
    assert meta2["surface"] == "paired"
    # The declared fixture is the v1 seed; v2 resolves to its counterpart.
    assert meta2["fixture_declared"] == "seed-v1-S"
    assert meta2["fixture_materialised"] == "seed-v2-S"


def test_the_grid_plan_covers_both_arms_and_records_its_seed(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(HARNESS), "grid", "--dest", str(tmp_path / "g"),
         "--force"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert proc.returncode == 0, proc.stderr
    plan = json.loads((tmp_path / "g" / "plan.json").read_text(
        encoding="utf-8"))
    assert plan["seed"]
    assert plan["failed"] == []
    variants = {r["variant"] for r in plan["runs"]}
    assert variants == {"v1", "v2"}
    tasks = {r["task"] for r in plan["runs"]}
    assert "T10-inception" not in tasks, "prose fixture cannot be prepared"
    # T09 runs on one arm only and must not appear as a v2 row.
    assert not [r for r in plan["runs"]
                if r["task"] == "T09-doctrine" and r["variant"] == "v2"]
